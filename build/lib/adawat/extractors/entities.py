from typing import List
import pyarabic.araby as araby
import pyarabic.named
import maskouk.collocations as colloc

def extract_named_entities(text: str) -> str:
    if not text.strip(): return ""
    wordlist = araby.tokenize(text)
    taglist = pyarabic.named.detect_named(wordlist)
    text_output: List[str] = []
    opened = False
    for word, tag in zip(wordlist, taglist):
        if tag in ("named", 'NI', 'NB'):
            if not opened:
                text_output.append("<mark class='named'>")
                opened = True   
            text_output.append(word)
        else:
            if opened:
                text_output.append("</mark>")
                opened = False
            text_output.append(word)
    if opened: text_output.append("</mark>")
    return " ".join(text_output).replace("</mark> <mark class='named'>", " ")

def show_collocations(text: str) -> str:
    if not text.strip(): return ""
    coll = colloc.CollocationClass(True)
    text = coll.lookup4long_collocations(text)
    wordlist = araby.tokenize(text)
    vocalized_list, taglist = coll.lookup(wordlist)
    text_output: List[str] = []
    opened = False
    for word, tag in zip(vocalized_list, taglist):
        if tag in ("CB", "CI"):
            if not opened:
                text_output.append("<mark class='coll'>")
                opened = True   
            text_output.append(word)
        else:
            if opened:
                text_output.append("</mark>")
                opened = False
            text_output.append(word)
    if opened: text_output.append("</mark>")
    return " ".join(text_output).replace("</mark> <mark class='coll'>", " ")

def extract_all_entities(text: str) -> str:
    return text
