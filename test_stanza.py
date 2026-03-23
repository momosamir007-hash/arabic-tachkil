import stanza

def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("Testing Stanza Sentiment Analysis...")

try:
    stanza.download('ar', processors='tokenize,sentiment', quiet=True)
    nlp = stanza.Pipeline('ar', processors='tokenize,sentiment', quiet=True)
    text = "هذا مشروع رائع جداً!"
    doc = nlp(text)
    for i, sentence in enumerate(doc.sentences):
        log(f"Sentence {i}: sentiment value = {sentence.sentiment}")
    
    text = "مرض خبيث"
    doc = nlp(text)
    for i, sentence in enumerate(doc.sentences):
        log(f"Sentence {i} (neg): sentiment value = {sentence.sentiment}")
except Exception as e:
    log(f"Stanza Error: {e}")

log("Finished Stanza Test.")
