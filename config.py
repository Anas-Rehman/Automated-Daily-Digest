import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Slack Configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_CHANNEL_ID") # Variable name in code is APP_TOKEN but maps to Channel ID
BYTEZ_API_KEY = os.environ.get("BYTEZ_API_KEY")

# -------------------------------------------------------------------------
# S O U R C E   L I S T
# -------------------------------------------------------------------------

RSS_FEEDS = {
    "⚖️ International Law": [
        "https://www.jurist.org/news/feed/",
        "http://opiniojuris.org/feed/",
        "https://www.justsecurity.org/feed/",
        "https://news.un.org/feed/subscribe/en/news/topic/law-and-crime-prevention/feed/rss.xml"
    ],
    "🌍 International Relations": [
        "https://foreignpolicy.com/feed/",
        "https://www.worldpoliticsreview.com/feed/",
        "https://apnews.com/politics.rss",
        "https://www.politico.eu/feed/",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best",
        "https://www.economist.com/international/rss.xml",
        # User Provided List (Selected High-Impact Global/Political)
        "https://foreignpolicy.com/feed/",
        "https://www.rollingstone.com/politics/feed/",
        "https://www.newsmax.com/rss/Politics/1/",
        "https://www.npr.org/rss/rss.php?id=1014",
        "https://www.cbsnews.com/latest/rss/politics",
        "https://www.politico.com/rss/politicopicks.xml",
        "https://www.realclearpolitics.com/index.xml",
        "https://www.thenation.com/subject/politics/feed/"
    ],
    "🇵🇰 National & Political (Pakistan)": [
        "https://www.dawn.com/feeds/pakistan",
        "https://tribune.com.pk/feed/pakistan",
        "https://www.geo.tv/rss/pakistan"
    ],
    "💻 Tech & Innovation": [
        "https://news.ycombinator.com/rss", # HackerNews
        "http://feeds.arstechnica.com/arstechnica/index",
        "https://techcrunch.com/feed/"
    ]
}
SCHEDULE_TIME = "12:00"

