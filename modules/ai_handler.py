import os
import requests
import json
import time
import re
# Ensure you have a config.py file with BYTEZ_API_KEY defined, 
# or replace this import with your actual key string.
try:
    from config import BYTEZ_API_KEY
except ImportError:
    BYTEZ_API_KEY = "YOUR_API_KEY_HERE"

def strip_thinking(text):
    """
    Removes internal monologue (<think> tags) and separates content 
    from headers/metadata.
    """
    if not text:
        return ""

    # 0. Aggressive <think> cleanup
    if '</think>' in text:
        text = text.split('</think>')[-1].strip()

    # Extracts content after the '--- CUT HERE ---' separator.
    separator = "--- CUT HERE ---"
    if separator in text:
        parts = text.split(separator)
        if len(parts) > 1:
            return parts[-1].strip()
            
    # Fallback: Header Search
    match_header = re.search(r'(⚖️|🌍|💻|🇵🇰).*', text, re.IGNORECASE)
    if match_header:
        # Check if the line after the header is "meta"
        content = text[match_header.start():]
        lines = content.split('\n')
        # If line 1 matches "I will now...", skip it
        if len(lines) > 1 and re.match(r'^\s*(I will|Here is|Note:)', lines[1], re.IGNORECASE):
            return '\n'.join([lines[0]] + lines[2:]).strip()
        return content.strip()
    
    return text.strip()

def generate_section_summary(category, articles):
    if not articles: 
        return None

    # 1. Prepare Content
    news_content = ""
    for idx, article in enumerate(articles[:20]): 
        # Safety: Escape curly braces in titles to prevent f-string errors
        title = article['title'].replace('{', '{{').replace('}', '}}')
        link = article['link'].replace('{', '{{').replace('}', '}}')
        news_content += f"{idx+1}. {title} - {link}\n"

    prompt = f"""
ROLE: Senior Intelligence Analyst & Research Director.
SECTION: {category}

Task: Produce a HIGH-DENSITY Daily Intelligence Digest based on the raw data below.

1.  **STRATEGY - "BITE-SIZED BUT EXHAUSTIVE"**:
    -   Explain in detail and cover every story
    -   **Completeness**: You must capture EVERY major argument, conflicting viewpoint, and geopolitical implication. 
    -   **Density**: No fluff or filler words. Every sentence must deliver a new fact, argument, or insight.

2.  **STRUCTURE**: 
    -   Write in punchy, high-impact paragraphs.
    -   **The Argument**: Explicitly state the conflict (e.g., "Proponents argue X, while critics warn of Y").
    -   **The Context**: Briefly cite the history or precedent without rambling.

3.  **CITATIONS**: Embed links naturally in the text.
    -   Start: "Per <URL|The New York Times>, ..."
    -   End: "...(via <URL|Reuters>)."

BEAUTY & FORMATTING GUIDE (Strict Slack Syntax):
1.  **Headers**: Use emojis. No H1/H2 tags (#).
2.  **Bold**: Use SINGLE asterisks (*), NOT double (**). 
3.  **Links**: Use strict Slack syntax: <URL|Source Name>. 
    -   Correct: <https://example.com|Read Source>
    -   Wrong: [Read Source](https://example.com)
    -   Wrong: https://example.com

CRITICAL OUTPUT RULES:
-   Output MUST be dense. Maximum information in minimum space.
-   Do NOT output your internal "<think>" process.
-   Output ONLY the final response.

RAW DATA:
{news_content}
"""

    # 2. Call Bytez API
    MODELS = [
        "anthropic/claude-opus-4-6" ,
        "Qwen/Qwen3-8B" , 
        "Qwen/Qwen3-4B-Thinking-2507",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "anthropic/claude-opus-4-5", 
        "openai/gpt-oss-20b" ,
        "meta-llama/Meta-Llama-3.1-8B-Instruct"
    ]

    if not BYTEZ_API_KEY:
        return "⚠️ Bytez API Key Missing"

    for model in MODELS:
        retries = 0
        max_retries = 3
        
        while retries <= max_retries:
            try:
                print(f"🤖 Brainstorming {category} with {model} (Attempt {retries+1})...")
                
                url = f"https://api.bytez.com/models/v2/{model}"
                headers = {
                    "Authorization": BYTEZ_API_KEY,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "messages": [
                        {
                            "role": "system", 
                            "content": "You are a news generation engine. You enable information flow. You do not converse. You do not plan. You only output the final article text." 
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "params": {
                        "temperature": 0.3 
                    }
                }

                # Intense timeout for Deep Research Papers
                response = requests.post(url, headers=headers, json=payload, timeout=300)
                
                if response.status_code == 200:
                    data = response.json()
                    if "output" in data and data["output"]:
                        # 1. Extract Main Content
                        raw_output = data["output"]["content"]
                        
                        # 2. Apply Strip Logic (Safety Net)
                        return strip_thinking(raw_output)
                    else:
                        print(f"  > Empty output from {model}. Moving to next model...")
                        break 

                elif response.status_code == 429:
                    print("  > Rate limited (429). Sleeping 60s before retry...")
                    time.sleep(60)
                    retries += 1
                    continue 

                else:
                    print(f"  > Error from {model} ({response.status_code}): {response.text}")
                    break 

            except Exception as e:
                print(f"  > Exception with {model}: {e}")
                break 
            
        print("  > Triggering Fallback to next model...")

    return "⚠️ Analysis Failed: All models in hierarchy failed to respond."


def summarize_news(categorized_news):
    """
    Orchestrates the summarization for ALL categories.
    Returns dict: { "Category": "Summary String" }
    """
    ai_report = {}
    
    print("--- Generating AI Magazine Content ---")
    for category, articles in categorized_news.items():
        if articles:
            summary = generate_section_summary(category, articles)
            if summary:
                ai_report[category] = summary
                
                # SAFETY: 10s sleep to prevent Token Rate Limiting (TPM) on Deep Dives
                print("  > 10s Token Cooldown...")
                time.sleep(10)
        else:
            ai_report[category] = "No major updates in this sector today."
            
    return ai_report
