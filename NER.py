import nltk
import pycountry
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
from nltk import word_tokenize, pos_tag, ne_chunk

def extract_involved_countries(text):
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    ner_tree = ne_chunk(tagged_tokens)
    
    raw_countries = []
    
    # NLP Engine Extraction
    for chunk in ner_tree:
        if hasattr(chunk, 'label'):
            if chunk.label() in ['GPE', 'LOCATION', 'ORGANIZATION', 'PERSON']:
                entity_name = ' '.join(c[0] for c in chunk)
                try:
                    # Pycountry filter karega ki inme se actual country kaunsi hai
                    if pycountry.countries.lookup(entity_name):
                        raw_countries.append(entity_name)
                except LookupError:
                    pass
                    
    # String-Based Bypass (NLP Blindspot Fix)
    if "USA" in tokens or "US" in tokens or "U.S.A." in tokens:
        raw_countries.append("USA")
    if "UK" in tokens or "U.K." in tokens:
        raw_countries.append("UK")
    if "UAE" in tokens or "U.A.E." in tokens:
        raw_countries.append("UAE")
                
    unique_countries = list(set(raw_countries))
    
    if len(unique_countries) > 0:
        return ", ".join(unique_countries)
    else:
        return "Global/Unknown"

# Ek complex geopolitical headline
test_headline = "The International Botanical Conference commenced this week with scientists gathering to discuss biodiversity preservation. Researchers presented numerous papers on the effects of minor temperature variations on alpine flora. A team from Brazil showcased their latest findings regarding the migratory patterns of specific butterfly species in the Amazon basin. Another group from Germany detailed a new statistical model for predicting forest canopy growth rates. The presentations were highly technical, focusing primarily on data collection methodologies and calibration of environmental sensors. Afternoon workshops involved hands-on demonstrations of soil analysis software and drone-based mapping techniques."

# Function call karo
extracted_countries = extract_involved_countries(test_headline)

# Output print karo
# print(f"Headline: {test_headline}")
print(f"Involved Countries Found: {extracted_countries}")