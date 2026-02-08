import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from config import SCHEDULE_TIME
from modules.news_fetcher import fetch_rss_news, filter_by_interests
from modules.ai_handler import summarize_news
from modules.learning_engine import fetch_daily_learning
from modules.slack_bot import send_daily_digest
from modules.pdf_generator import generate_daily_pdf

def job_function():
    print(f"[{datetime.now()}] Starting daily digest job...")
    
    # 1. Fetch News
    print("Fetching news...")
    news_data = fetch_rss_news()
    
    # 2. Process/Filter News
    print("Filtering news...")
    news_roundup = filter_by_interests(news_data)
    
    # 3. AI Summarization (CRITICAL STEP - Was missing)
    # This generates the actual text for the report and PDF
    print("Generating AI Summaries...")
    ai_report = summarize_news(news_roundup)
    
    # 3. Fetch Learning Content
    print("Fetching learning content...")
    learning_item = fetch_daily_learning()
    
    # 4. Generate PDF Newspaper
    print("Generating PDF Morning Edition...")
    pdf_path = generate_daily_pdf(ai_report, learning_item)
    
    # 5. Send to Slack
    print("Sending to Slack...")
    send_daily_digest(ai_report, learning_item, pdf_path)
    print(f"[{datetime.now()}] Job finished.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    
    # Parse HH:MM from config
    hour, minute = map(int, SCHEDULE_TIME.split(":"))
    
    # Schedule the job
    scheduler.add_job(job_function, 'cron', hour=hour, minute=minute)
    
    print(f"Bot started. Waiting for {SCHEDULE_TIME} daily trigger...")
    print("Press Ctrl+C to exit.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
