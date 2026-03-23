from .lexicon_sentiment import analyze_sentiment_lexicon
from typing import Dict, Any, List
try:
    import stanza
    STANZA_AVAILABLE = True
except ImportError:
    STANZA_AVAILABLE = False

_sentiment_pipe = None

def get_sentiment(text: str) -> Dict[str, Any]:
    """Analyze sentiment using Lexicon-based approach as primary, Stanza as secondary (if available)."""
    # Use lexicon-based as it is more reliable for Arabic in the current environment
    return analyze_sentiment_lexicon(text)
