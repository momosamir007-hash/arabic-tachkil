import pyarabic.araby as araby
from typing import List, Dict

def generate_affixes(text: str) -> List[Dict[str, str]]:
    if not text.strip(): return []
    words = araby.tokenize(text)
    result_list = []
    for word in words:
        my_list = [word + araby.FATHA, word + araby.DAMMA, word + araby.KASRA]
        result_list.extend([{'affixed': oneword, 'standard': oneword} for oneword in my_list])
    return result_list
