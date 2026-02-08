import feedparser
from config import RSS_FEEDS
import time

def fetch_rss_news():
    """
    Fetches news from RSS feeds and organizes them by Category.
    Returns: dict { "Category": [ {title, link, summary, published}, ... ] }
    """
    categorized_news = {}

    print("--- Fetching Raw Feed Data ---")
    
    for category, feeds in RSS_FEEDS.items():
        print(f"Processing Category: {category}...")
        categorized_news[category] = []
        
        seen_links = set() # Per category deduplication

        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                # Sort by published date if available, new first
                if isinstance(feed.entries, list):
                    # Simple cap of 15 articles per feed to keep it fresh
                    entries = feed.entries[:15]
                    
                    for entry in entries:
                        if entry.link in seen_links:
                            continue
                        seen_links.add(entry.link)
                        
                        categorized_news[category].append({
                            'title': entry.title,
                            'link': entry.link,
                            'summary': getattr(entry, 'summary', ''),
                            'published': getattr(entry, 'published', 'N/A')
                        })
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")

        print(f"  > Collected {len(categorized_news[category])} items for {category}.")

    return categorized_news

def filter_by_interests(news_data):
    """
    Filters news based on user interests.
    Currently a pass-through as interests are pre-defined in RSS_FEEDS.
    """
    print("  > Passing through news (Interest filtering is implicit in RSS list)...")
    return news_data
