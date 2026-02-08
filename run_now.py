from modules.news_fetcher import fetch_rss_news, filter_by_interests
from modules.ai_handler import summarize_news
from modules.learning_engine import fetch_daily_learning
from modules.pdf_generator import generate_daily_pdf
from modules.slack_bot import send_daily_digest

def run_once():
    print("--- INITIATING AI INTELLIGENCE CYCLE (MANUAL MOCK RUN) ---")
    
    # 1. Fetch
    print("Fetching news...")
    news_data = fetch_rss_news()
    
    # 2. Filter
    print("Filtering news...")
    news_roundup = filter_by_interests(news_data)
    
    # 3. Summarize
    print("Generating AI Summaries...")
    ai_report = summarize_news(news_roundup)
    
    # 4. Learning
    print("Fetching learning content...")
    learning_item = fetch_daily_learning()
    
    # 5. PDF
    print("Generating PDF...")
    pdf_path = generate_daily_pdf(ai_report, learning_item)
    
    # 6. Send
    print("Sending to Slack...")
    send_daily_digest(ai_report, learning_item, pdf_path)
    print("--- CYCLE COMPLETE ---")

if __name__ == "__main__":
    run_once()
