import pyarabic.number
import pyarabic.araby as araby
from typing import List

def number_to_words(text: str) -> str:
    text = text.strip()
    if not text: return ""
    try:
        ar = pyarabic.number.ArNumbers()
        return ar.int2str(text)
    except Exception as e:
        return f"Error converting number '{text}': {str(e)}"

def extract_numbered_phrases(text: str) -> str:
    if not text.strip(): return ""
    wordlist = araby.tokenize(text)
    taglist = pyarabic.number.detect_numbers(wordlist)
    text_output: List[str] = []
    opened = False
    for word, tag in zip(wordlist, taglist):
        if tag in ('DI', 'DB'):
            if not opened:
                text_output.append("<mark class='number'>")
                opened = True   
            text_output.append(word)
        else:
            if opened:
                text_output.append("</mark>")
                opened = False
            text_output.append(word)
    if opened: text_output.append("</mark>")
    return " ".join(text_output).replace("</mark> <mark class='number'>", " ")
