import random
import json
import os

def select_article_of_the_day(candidates):
    """
    Selects one high-quality piece for Section C.
    """
    if not candidates:
        return {
            "title": "No Scholarship Found Today",
            "link": "https://ssrn.com/en/",
            "summary": "Check SSRN manually.",
            "source": "System"
        }
    
    # For now, random selection from the filtered 'Scholarship' feeds
    selected = random.choice(candidates)
    return selected

tips_list_fallback = [
    {"title": "Legal Principle: Stare Decisis", "content": "Stare decisis means 'to stand by things decided.' It ensures consistency in case law."},
    {"title": "Legal Principle: Mens Rea", "content": "Mens rea refers to the 'guilty mind' or criminal intent necessary to be convicted of a crime."},
    {"title": "Legal Principle: Habeas Corpus", "content": "Habeas corpus protects against unlawful detention, requiring a prisoner be brought before a court."},
    {"title": "Legal Principle: Force Majeure", "content": "Force majeure frees parties from liability when an extraordinary event prevents contract performance."}
]

def load_legal_tips():
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'legal_tips.json')
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) and len(data) > 0 else tips_list_fallback
    except Exception as e:
        print(f"Error loading legal_tips.json: {e}")
    return tips_list_fallback

def get_legal_tip():
    """
    Fetches a random tip from the JSON file (or fallback if missing).
    """
    tips = load_legal_tips()
    return random.choice(tips)

def fetch_daily_learning():
    """
    Orchestrates the daily learning content.
    Currently selects a legal tip.
    """
    return get_legal_tip()

if __name__ == "__main__":
    print(fetch_daily_learning())
