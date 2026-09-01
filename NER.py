import nltk
import numpy
import pycountry
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
from nltk import word_tokenize, pos_tag, ne_chunk

def extract_involved_countries(text):
    # Breaking the text into words
    tokens = word_tokenize(text)

    # For tagging each word with Parts of Speech
    tagged_tokens = pos_tag(tokens)

    # For creating Named Entities tree using Tagged tokens
    ner_tree = ne_chunk(tagged_tokens)

    countries = []

    for chunk in ner_tree:
        if hasattr(chunk , 'label'):

            if chunk.label() == 'GPE':

                entity_name = ' '.join(c[0] for c in chunk)

                #Strict Validation Factor

                try:
                    if pycountry.countries.lookup(entity_name):

                        if entity_name not in countries:
                            countries.append(entity_name)
                except LookupError:
                    pass

    if len(countries) > 0:
        return ", ".join(countries)
    else:
        return "Global/Unknown"

# Ek complex geopolitical headline
test_headline = "India and Japan sign a new defense treaty to counter threats in Asia."

# Function call karo
extracted_countries = extract_involved_countries(test_headline)

# Output print karo
print(f"Headline: {test_headline}")
print(f"Involved Countries Found: {extracted_countries}")

    


