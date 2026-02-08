import re

def clean_slack_markdown(text):
    """
    Converts standard Markdown into Slack's specific 'mrkdwn' format.
    1. Bold: **text** -> *text*
    2. Links: [text](url) -> <url|text>
    3. Headers: ### text -> *text*
    """
    # 1. Links: [text](url) -> <url|text>
    # Note: Regex needs to be careful not to break existing <url|text> if AI did it right.
    # We look for [text](url) pattern specifically.
    link_pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    text = re.sub(link_pattern, r'<\2|\1>', text)
    
    # 2. Bold: **text** -> *text*
    bold_pattern = r'\*\*([^*]+)\*\*'
    text = re.sub(bold_pattern, r'*\1*', text)
    
    # 3. Headers: ### text -> *text* (Make them bold)
    header_pattern = r'###\s*(.+)'
    text = re.sub(header_pattern, r'*\1*', text)

    return text
