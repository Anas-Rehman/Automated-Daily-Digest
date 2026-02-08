from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
import time

def create_header_blocks(part_num=1, total_parts=1):
    date_str = datetime.now().strftime("%A, %d %B %Y")
    subtitle = ""
    if total_parts > 1:
        subtitle = f" | Part {part_num} of {total_parts}"
        
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📰 THE DAILY INTELLIGENCE{subtitle}",
                "emoji": True
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*{date_str}* | _Curated by AI_"
                }
            ]
        },
        {"type": "divider"}
    ]

from modules.slack_utils import clean_slack_markdown

def paginate_report(ai_report):
    """
    Splits the full report into 'Pages' (lists of blocks) that fit Slack limits.
    Each Page is a list of Slack blocks ready to send.
    """
    pages = []
    current_page_blocks = []
    current_char_count = 0
    
    for category, raw_summary in ai_report.items():
        # Clean the summary for Slack formatting
        summary = clean_slack_markdown(raw_summary)

        # Create blocks for this section
        section_blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": category.upper(),
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": summary
                }
            },
            {"type": "divider"}
        ]
        
        # Calculate size
        section_len = len(category) + len(summary) + 100 
        
        if current_char_count + section_len > 2000:
            # Setup current page to finish
            if current_page_blocks:
                pages.append(current_page_blocks)
            
            # Start new page
            current_page_blocks = []
            current_char_count = 0
            
        # Add to current page
        current_page_blocks.extend(section_blocks)
        current_char_count += section_len
        
    # Add the final page
    if current_page_blocks:
        pages.append(current_page_blocks)
        
    return pages

def send_daily_digest(ai_report, learning_item=None, pdf_path=None):
    if not SLACK_BOT_TOKEN:
        print("Error: SLACK_BOT_TOKEN is missing.")
        return

    client = WebClient(token=SLACK_BOT_TOKEN)
    
    # 1. Paginate
    pages = paginate_report(ai_report)
    
    # 2. Add Learning Content to the last page or as a new page
    if learning_item:
        learning_block = [
            {"type": "divider"},
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🎓 CONCEPT OF THE DAY",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{learning_item.get('title', 'Daily Tip')}*\n{learning_item.get('content', '')}"
                }
            }
        ]
        
        # Check if we can fit it on the last page
        if pages and len(str(pages[-1])) + len(str(learning_block)) < 3000: # Rough estimation
            pages[-1].extend(learning_block)
        else:
            pages.append(learning_block)

    total_pages = len(pages)
    
    print(f"--- Dispatching {total_pages} Pages to Slack ---")

    for i, page_blocks in enumerate(pages):
        part_num = i + 1
        
        # Add Header to first block of each page
        final_blocks = create_header_blocks(part_num, total_pages) + page_blocks
        
        try:
            client.chat_postMessage(
                channel=SLACK_APP_TOKEN, 
                blocks=final_blocks,
                text=f"Daily Intelligence | Part {part_num}/{total_pages}"
            )
            print(f"  > Sent Part {part_num}")
            time.sleep(1) # Rate limit safety
        except SlackApiError as e:
            print(f"  > Error sending Part {part_num}: {e.response['error']}")
            # Fallback for this specific part
            if 'invalid_blocks' in str(e):
                print("    > Retrying as plain text...")
                fallback_text = f"**PART {part_num}/{total_pages}**\n\n"
                # Extract text from blocks roughly
                for block in page_blocks:
                    if block['type'] == 'section':
                        fallback_text += block['text']['text'] + "\n\n"
                
                client.chat_postMessage(
                    channel=SLACK_APP_TOKEN,
                    text=fallback_text
                )

    # 3. Upload PDF Newspaper
    if pdf_path:
        print(f"--- Uploading PDF: {pdf_path} ---")
        try:
            response = client.files_upload_v2(
                channel=SLACK_APP_TOKEN,
                file=pdf_path,
                title="📰 Morning Edition Newspaper",
                initial_comment="Here is your Morning Edition PDF! 📄"
            )
            print("  > PDF Upload successful.")
            
            # Send explicit link as separate message - REMOVED TO PREVENT DOUBLE POSTING
            # The files_upload_v2 already posts the file to the channel with the initial_comment.
            
            file_info = response.get("file")
            if not file_info:
                # Fallback: sometimes v2 returns 'files' list?
                files = response.get("files")
                if files and len(files) > 0:
                    file_info = files[0]

            if file_info:
                print("  > File Info Found. ID:", file_info.get("id"))
                # We don't need to post the permalink separately anymore.
            else:
                print("  > Error: No 'file' or 'files' in response object.")
                print("  > Full Response:", response)
                
        except SlackApiError as e:
            print(f"  > Error uploading PDF: {e.response['error']}")
