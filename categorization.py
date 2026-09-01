def categorize_event(text):
    # Text ko lowercase karo taaki case-sensitivity ka error na aaye
    text_lower = text.lower()
    
    # Geopolitics ki 4 main categories aur unke high-impact keywords ka map
    category_map = {
        "Defense & Security": ["missile", "troops", "border", "attack", "navy", "military", "nuclear", "war", "defense", "treaty", "weapon"],
        "Economy & Trade": ["trade", "gdp", "tariff", "tax", "export", "import", "sanctions", "economy", "market", "currency", "business"],
        "Diplomacy & Politics": ["summit", "meet", "diplomat", "embassy", "election", "vote", "minister", "president", "alliance", "treaty"],
        "Infrastructure & Tech": ["space", "satellite", "cyber", "hack", "infrastructure", "corridor", "technology"]
    }
    
    # Har category ka score track karne ke liye dictionary (sabko 0 se start karo)
    scores = {category: 0 for category in category_map}
    
    # Text mein keywords dhoondho aur count badhao
    for category, keywords in category_map.items():
        for word in keywords:
            # Agar keyword text mein hai, toh us category ka score +1 karo
            if word in text_lower:
                scores[category] += 1
                
    # Sabse highest score nikal lo
    max_score = max(scores.values())
    
    # Agar koi bhi keyword match nahi hua (max_score 0 hai)
    if max_score == 0:
        return "General Geopolitics"
        
    # Tie-breaker logic: List comprehension se woh saari categories nikalo jinka score max_score ke barabar hai
    top_categories = [cat for cat, score in scores.items() if score == max_score]
    
    # Agar ek se zyada category tie ho rahi hai, toh 'Mixed' return karo
    if len(top_categories) > 1:
        return "Mixed / Multi-Domain"
    else:
        return top_categories[0]


# Test Cases
headline_1 = "India and Japan sign a new defense treaty to counter threats in Asia."
headline_2 = "US imposes heavy trade tariffs and new sanctions on China."
headline_3 = "Global summit fails as no agreement is reached."
headline_4 = "Military conducts cyber attack on trade corridor." # Tie case

print(f"Headline 1: {categorize_event(headline_1)}")
print(f"Headline 2: {categorize_event(headline_2)}")
print(f"Headline 3: {categorize_event(headline_3)}")
print(f"Headline 4 (Tie): {categorize_event(headline_4)}")