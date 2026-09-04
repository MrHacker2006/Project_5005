import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')

analyzer = SentimentIntensityAnalyzer()

threat_keywords = ["missile", "border", "attack", "sanctions", "troops"]
rival_entities = ["rival", "pakistan", "china"]
ally_entities = ["japan", "usa", "russia", "israel", "france"]
strategic_keywords = ["treaty", "sign", "counter", "pact", "agreement", "defense"]

def get_indic_sentiment(text):
    # 1. Text ko sentences mein tod do
    sentences = nltk.sent_tokenize(text)
    
    sentence_scores = []
    india_context_sentiment = None
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        
        # 2. Har sentence ka alag polarity score nikalo
        score = analyzer.polarity_scores(sentence)
        sentence_scores.append(score['compound'])
        
        # 3. Sentence-level Override Logic checks
        is_threat = any(word in sentence_lower for word in threat_keywords)
        is_rival = any(entity in sentence_lower for entity in rival_entities)
        has_ally = any(entity in sentence_lower for entity in ally_entities)
        is_strategic = any(word in sentence_lower for word in strategic_keywords)
        has_india = "india" in sentence_lower
        
        if is_threat and is_rival:
            india_context_sentiment = "Negative (Security Threat for India)"
        elif has_india and (has_ally or is_strategic):
            india_context_sentiment = "Positive (Strategic Advantage for India)"
            
    # 4. Average formula completely hata do. Extreme Sentiment Dominance apply karo.
    if sentence_scores:
        max_positive = max(sentence_scores)
        max_negative = min(sentence_scores)
        
        # Jo score zero se zyada door hai (intensity mein bada hai), use final base score banao
        if abs(max_negative) > max_positive:
            base_compound = max_negative
        else:
            base_compound = max_positive
    else:
        base_compound = 0.0
    
    # 5. Base Threshold ko widen karo (0.10) taaki academic text trigger na ho
    if base_compound >= 0.10:
        base_sentiment = "Positive"
    elif base_compound <= -0.10:
        base_sentiment = "Negative"
    else:
        base_sentiment = "Neutral"
        
    if india_context_sentiment is None:
        india_context_sentiment = base_sentiment

    # Structured Dictionary Return karo
    return {
        "vader_base_score": round(base_compound, 4),
        "vader_base_sentiment": base_sentiment,
        "final_indic_sentiment": india_context_sentiment
    }

# Ab tum kisi bhi string ko pass karke structured output le sakte ho
dummy_news = "The ongoing economic summit in Geneva highlighted several emerging market trends. Delegates from Pakistan presented a new proposal regarding agricultural exports and water management systems. The session was largely focused on sustainable farming and increasing crop yields in arid environments. Several European nations praised the initiative and offered technological support for irrigation projects. However, the afternoon session took a completely different turn due to unexpected global news. A massive cyber attack severely crippled the banking infrastructure in eastern Europe, causing widespread financial panic. Analysts believe this coordinated digital strike was executed by an independent hacker syndicate."


final_result = get_indic_sentiment(dummy_news)

print("--- NLP Engine Output ---")
print(f"Base Sentiment: {final_result['vader_base_sentiment']} (Score: {final_result['vader_base_score']})")
print(f"Indic Output:   {final_result['final_indic_sentiment']}")