from typing import Dict, Any, List
try:
    from camel_tools.dialectid import DialectIdentifier
    CAMEL_AVAILABLE = True
except ImportError:
    CAMEL_AVAILABLE = False

_identifier = None

def identify_dialect(text: str) -> Dict[str, Any]:
    """Identify Arabic dialect using Camel Tools."""
    global _identifier
    if not CAMEL_AVAILABLE:
        return {"error": "Camel Tools not installed", "dialect": "unknown"}
    
    if not text.strip():
        return {"dialect": "unknown"}

    try:
        if _identifier is None:
            # Note: Requires 'dialectid-did-multi-task' or similar model
            _identifier = DialectIdentifier.pretrained()
        
        predictions = _identifier.predict([text])[0]
        # Return top dialect and confidence
        top_dialect = predictions.top
        confidence = predictions.scores[top_dialect]
        
        # Human readable names mapping if needed
        return {
            "dialect": top_dialect,
            "confidence": f"{confidence:.2f}",
            "text": text
        }
    except Exception as e:
        if "camel_tools" in str(e) or "ImportError" in str(e):
            return {"error": "تتطلب هذه الميزة تثبيت camel-tools و Java بشكل صحيح على النظام.", "dialect": "غير متاح"}
        return {"error": str(e), "dialect": "error"}
