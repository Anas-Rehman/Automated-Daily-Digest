from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

# Ensure necessary NLTK data is downloaded for Sumy
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def generate_summary(text, sentences_count=2, language="english"):
    """
    Generates a generic summary using LSA.
    Since RSS feeds often provide a summary/description, this is a fallback 
    or utility if we fetch full article content (which is harder without scraping).
    
    For this 'Free' version, we will primarily rely on RSS descriptions to avoid 
    heavy scraping/blocking issues, but this function is ready for full text.
    """
    try:
        if not text:
            return "No content to summarize."
            
        parser = PlaintextParser.from_string(text, Tokenizer(language))
        stemmer = Stemmer(language)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(language)

        summary_sentences = summarizer(parser.document, sentences_count)
        return " ".join([str(s) for s in summary_sentences])
    except Exception as e:
        return f"Could not summarize: {str(e)}"

# Helper to clean HTML tags if RSS description is raw HTML
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()
