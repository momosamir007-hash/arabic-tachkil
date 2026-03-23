from typing import Dict, Any, List
import shutil
try:
    import stanza
    from farasa.segmenter import FarasaSegmenter
    from farasa.ner import FarasaNamedEntityRecognizer
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False

JAVA_AVAILABLE = shutil.which("java") is not None

_stanza_pipe = None
_farasa_segmenter = None
_farasa_ner = None

def stanza_analyze(text: str) -> Dict[str, Any]:
    """Analyze text using Stanford Stanza."""
    global _stanza_pipe
    if not ADVANCED_AVAILABLE:
        return {"error": "Stanza not installed"}
    
    try:
        if _stanza_pipe is None:
            # Note: This might download models on first run (~200MB)
            stanza.download('ar', processors='tokenize,mwt,lemma,pos,depparse')
            _stanza_pipe = stanza.Pipeline('ar', processors='tokenize,mwt,lemma,pos,depparse', quiet=True)
        
        doc = _stanza_pipe(text)
        results = []
        for sent in doc.sentences:
            for word in sent.words:
                results.append({
                    "text": word.text,
                    "lemma": word.lemma,
                    "pos": word.pos,
                    "head": word.head,
                    "deprel": word.deprel
                })
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

def farasa_segment(text: str) -> List[str]:
    """Segment Arabic text using Farasa."""
    global _farasa_segmenter
    if not ADVANCED_AVAILABLE:
        return [text]
    
    try:
        if _farasa_segmenter is None:
            _farasa_segmenter = FarasaSegmenter(interactive=True)
        return _farasa_segmenter.segment(text).split()
    except Exception:
        return text.split()

def stanza_ner(text: str) -> List[Dict[str, str]]:
    """Named Entity Recognition using Stanza."""
    global _stanza_pipe
    if not ADVANCED_AVAILABLE:
        return []
    
    try:
        if _stanza_pipe is None:
            stanza.download('ar', processors='tokenize,ner')
            _stanza_pipe = stanza.Pipeline('ar', processors='tokenize,ner', quiet=True)
        elif 'ner' not in _stanza_pipe.processors:
            # Add NER to existing pipeline if possible or just download
            stanza.download('ar', processors='tokenize,ner')
            _stanza_pipe = stanza.Pipeline('ar', processors='tokenize,ner', quiet=True)
            
        doc = _stanza_pipe(text)
        results = []
        for ent in doc.ents:
            results.append({"word": ent.text, "tag": ent.type})
        return results
    except Exception as e:
        return [{"word": "Error", "tag": str(e)}]

def farasa_ner(text: str) -> List[Dict[str, str]]:
    """Named Entity Recognition using Farasa, with Stanza fallback."""
    global _farasa_ner
    
    # Check Java for Farasa
    if JAVA_AVAILABLE and ADVANCED_AVAILABLE:
        try:
            if _farasa_ner is None:
                _farasa_ner = FarasaNamedEntityRecognizer(interactive=True)
            ner_output = _farasa_ner.recognize(text)
            results = []
            for item in ner_output.split():
                if '/' in item:
                    word, tag = item.rsplit('/', 1)
                    if tag != 'O':
                        results.append({"word": word, "tag": tag})
            if results: return results
        except Exception:
            pass # Fallback to Stanza
            
    # Fallback to Stanza NER
    return stanza_ner(text)
