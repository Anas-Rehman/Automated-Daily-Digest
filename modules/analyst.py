from newspaper import Article
import nltk

# Ensure NLTK data is present (idempotent)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

def analyze_and_summarize(url, sentence_limit=10):
    """
    Visits the URL, extracts the full article text, and generates a deep summary.
    Returns:
        title (str)
        summary (str): A multi-sentence executive summary.
        text (str): The full text (optional)
        top_image (str): URL to main image
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # NLP processing (Keyword extraction + Summarization)
        article.nlp()
        
        # We want a "PhD Professor" level detail, so we take a longer summary
        # If the generated summary is too short, we might take the first few paragraphs manually.
        summary = article.summary
        
        # Fallback if nlp() returns nothing
        if not summary or len(summary) < 50:
            # Take the first 1500 chars roughly (~3 paragraphs)
            summary = article.text[:1500] + "..."
            
        return {
            "title": article.title,
            "summary": summary,
            "top_image": article.top_image,
            "authors": article.authors,
            "publish_date": str(article.publish_date)
        }

    except Exception as e:
        print(f"Error analyzing {url}: {e}")
        return None

if __name__ == "__main__":
    # Test on a heavy article
    url = "https://www.reuters.com/world/asia-pacific/"
    print(analyze_and_summarize(url))
