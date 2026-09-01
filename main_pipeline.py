import json
from db_integration import save_prediction_to_db
from NER import extract_involved_countries
from categorization import categorize_event
from test_logic import get_indic_sentiment

def process_geopolitics_headline(headline):
    # 1. NER Engine call karo (NER.py se aaya)
    entities = extract_involved_countries(headline)
    
    # 2. Categorization Engine call karo (categorization.py se aaya)
    category = categorize_event(headline)
    
    # 3. Sentiment & Override Engine call karo (test_logic.py se aaya)
    sentiment_data = get_indic_sentiment(headline)
    
    # 4. Final Aggregated Dictionary build karo
    final_output = {
        "headline_text": headline,
        "entities_detected": entities,
        "event_category": category,
        "base_vader_score": sentiment_data["vader_base_score"],
        "base_vader_sentiment": sentiment_data["vader_base_sentiment"],
        "final_indic_sentiment": sentiment_data["final_indic_sentiment"]
    }
    
    return final_output


