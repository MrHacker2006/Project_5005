import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')

analyzer = SentimentIntensityAnalyzer()


# Threat aur Rival lists global scope mein rakho
threat_keywords = ["missile", "border", "attack", "sanctions", "troops"]
rival_entities = ["rival", "pakistan", "china"]


ally_entities = ["japan", "usa", "russia", "israel", "france"]
strategic_keywords = ["treaty", "sign", "counter", "pact", "agreement", "defense"]


def get_indic_sentiment(text):
    # 1. Base score nikalo
    vader_scores = analyzer.polarity_scores(text)
    base_compound = vader_scores['compound']
    
    # 2. Base Threshold Apply karo
    if base_compound >= 0.05:
        base_sentiment = "Positive"
    elif base_compound <= -0.05:
        base_sentiment = "Negative"
    else:
        base_sentiment = "Neutral"
        
    # 3. Custom Override Logic Apply karo
    text_lower = text.lower()
    is_threat = any(word in text_lower for word in threat_keywords)
    is_rival = any(entity in text_lower for entity in rival_entities)

    # Naya Positive Logic Check
    has_ally = any(entity in text_lower for entity in ally_entities)
    is_strategic = any(word in text_lower for word in strategic_keywords)
    has_india = "india" in text_lower
    
    india_context_sentiment = base_sentiment
    
    if is_threat and is_rival:
        india_context_sentiment = "Negative (Security Threat for India)"

    # Rule 2: Positive Override (India ki strategic partnerships)
    elif has_india and (has_ally or is_strategic):
        india_context_sentiment = "Positive (Strategic Advantage for India)"
        
    # 4. Structured Dictionary Return karo (Database friendly format)
    return {
        "vader_base_score": base_compound,
        "vader_base_sentiment": base_sentiment,
        "final_indic_sentiment": india_context_sentiment
    }


# Ab tum kisi bhi string ko pass karke structured output le sakte ho
dummy_news = "China successfully tests new border attack drones."

final_result = get_indic_sentiment(dummy_news)

print("--- NLP Engine Output ---")
print(f"Base Sentiment: {final_result['vader_base_sentiment']} (Score: {final_result['vader_base_score']})")
print(f"Indic Output:   {final_result['final_indic_sentiment']}")