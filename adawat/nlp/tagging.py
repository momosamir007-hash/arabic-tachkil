import re
from collections import Counter
from typing import List, Dict, Tuple
import pyarabic.araby as araby
import naftawayh.wordtag

def word_tagging(text: str) -> List[Dict[str, str]]:
    """Classify words and return tags."""
    if not text.strip():
        return []
    tagger = naftawayh.wordtag.WordTagger()
    word_list = araby.tokenize(text)
    list_result = []
    for word in word_list:
        tag = 't' if tagger.is_stopword(word) else ''
        if not tag:
            if tagger.is_noun(word):
                tag += 'n'
            if tagger.is_verb(word):
                tag += 'v'
        list_result.append({'word': word, 'tag': tag})
    return list_result

def chunk_split(text: str) -> List[str]:
    """Split text into chunks."""
    return [text]

def get_bigrams(text: str) -> List[str]:
    """Get sorted bigram frequencies."""
    words = araby.tokenize(text)
    if len(words) < 2:
        return []
    bigrams_list = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    counts = Counter(bigrams_list)
    return [f"{item} {counts[item]}" for item in sorted(counts)]

def inverse_rhyme_sort(text: str) -> List[str]:
    """Sort words by rhyme (reverse character order)."""
    word_list = araby.tokenize(text)
    if not word_list:
        return []
    inter_list = [word[::-1] for word in word_list]
    inter_list.sort()
    return [word[::-1] for word in inter_list]

def segment_language(text: str) -> List[Tuple[str, str]]:
    """Segment text into Arabic and Latin parts."""
    tokens = re.split(r'([^\u0600-\u06ff\s\d\?\,\:\!\(\)\.\-]+)', text)
    result = []
    for token in tokens:
        if not token:
            continue
        if re.search(r'[\u0600-\u06ff]', token):
            result.append(('arabic', token))
        elif token.strip():
            result.append(('latin', token.strip()))
    return result
