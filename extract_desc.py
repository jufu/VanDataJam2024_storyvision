import pandas as pd
import spacy

def extract_adj_adv(text):
    """
    Extract adjectives and adverbs from the text using spaCy.
    
    Args:
        text (str): The input text to process.
        
    Returns:
        list: List of adjectives and adverbs found in the text.
    """
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.pos_ in ['ADJ', 'ADV']]
