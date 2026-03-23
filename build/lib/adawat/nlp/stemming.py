from typing import List, Dict, Any
import tashaphyne.stemming
import qalsadi.analex
import asmai.anasem
import sylajone.anasyn as arasyn
from adawat.config import CACHE_PATH

def light_stemmer(text: str) -> List[Dict[str, str]]:
    if not text.strip(): return []
    result = []
    als = tashaphyne.stemming.ArabicLightStemmer()
    word_list = als.tokenize(text)
    for word in word_list:
        als.segment(word)
        affix_list = als.get_affix_list()
        for affix in affix_list:
            result.append({
                'word': word, 'prefix': affix.get('prefix', ''),
                'stem': affix.get('stem', ''), 'suffix': affix.get('suffix', ''),
                'root': affix.get('root', ''), 'type': '-'
            })
    return result

def full_stemmer(text: str, lastmark: bool = True) -> List[Any]:
    if not text.strip(): return []
    analyzer = qalsadi.analex.Analex(cache_path=CACHE_PATH)
    if str(lastmark) == "0" or not lastmark:
        analyzer.disable_syntax_lastmark()
    analyzer.set_debug(False)
    analyzer.set_limit(100)
    analyzer.disable_allow_cache_use()    
    anasynt = arasyn.SyntaxAnalyzer()
    anasem = asmai.anasem.SemanticAnalyzer()    
    result = analyzer.check_text(text)
    result, _ = anasynt.analyze(result)
    result = anasem.analyze(result)            
    return anasynt.decode(result)
