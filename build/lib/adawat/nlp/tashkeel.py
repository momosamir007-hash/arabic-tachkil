import pyarabic.araby as araby
import mishkal.tashkeel as ArabicVocalizer
from adawat.config import CACHE_PATH
from typing import Dict, Any, List

def tashkeel(text: str, lastmark: bool = True) -> str:
    if not text.strip(): return ""
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=CACHE_PATH)
    if not lastmark or str(lastmark) == "0":
        vocalizer.disable_last_mark()
    return vocalizer.tashkeel(text)

def reduce_tashkeel(text: str) -> str:
    if not text.strip(): return ""
    return araby.reduce_tashkeel(text)

def tashkeel_suggest(text: str, lastmark: bool = True) -> List[Dict[str, Any]]:
    if not text.strip(): return []
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=CACHE_PATH)
    if not lastmark or str(lastmark) == "0":
        vocalizer.disable_last_mark()
    return vocalizer.tashkeel_ouput_html_suggest(text)

def assistant_tashkeel(text: str) -> str:
    if not text.strip(): return ""
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path=CACHE_PATH)
    return vocalizer.assistanttashkeel(text)

def compare_tashkeel(text: str) -> Dict[str, Any]:
    return {"html": text, "stats": {}}
