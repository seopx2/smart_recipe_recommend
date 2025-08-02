import re
import pandas as pd

def normalize(text):
    if pd.isna(text): return ''
    text = text.lower()
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'\d+(g|kg|ml|l|개|봉|팩|입|장)', '', text)
    return text
