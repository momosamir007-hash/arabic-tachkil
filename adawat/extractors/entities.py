from typing import List
import pyarabic.araby as araby
import pyarabic.named
import maskouk.collocations as colloc

def extract_named_entities(text: str) -> str:
    """Extract named entities and wrap them in <mark class='named'> tags."""
    if not text.strip():
        return ""
    wordlist = araby.tokenize(text)
    taglist = pyarabic.named.detect_named(wordlist)
    
    text_output: List[str] = []
    opened = False
    for word, tag in zip(wordlist, taglist):
        is_named = tag in ("named", 'NI', 'NB')
        if is_named and not opened:
            text_output.append("<mark class='named'>")
            opened = True
        elif not is_named and opened:
            text_output.append("</mark>")
            opened = False
        text_output.append(word)
        
    if opened:
        text_output.append("</mark>")
        
    return " ".join(text_output).replace("</mark> <mark class='named'>", " ")

def show_collocations(text: str) -> str:
    """Show collocations and wrap them in <mark class='coll'> tags."""
    if not text.strip():
        return ""
    coll = colloc.CollocationClass(True)
    text = coll.lookup4long_collocations(text)
    wordlist = araby.tokenize(text)
    vocalized_list, taglist = coll.lookup(wordlist)
    
    text_output: List[str] = []
    opened = False
    for word, tag in zip(vocalized_list, taglist):
        is_coll = tag in ("CB", "CI")
        if is_coll and not opened:
            text_output.append("<mark class='coll'>")
            opened = True
        elif not is_coll and opened:
            text_output.append("</mark>")
            opened = False
        text_output.append(word)
        
    if opened:
        text_output.append("</mark>")
        
    return " ".join(text_output).replace("</mark> <mark class='coll'>", " ")

def extract_all_entities(text: str) -> str:
    return text
