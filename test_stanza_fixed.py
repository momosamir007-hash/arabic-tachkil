import stanza

def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("Retrying Stanza Sentiment Analysis without 'quiet' in download...")

try:
    # stanza.download('ar', processors='tokenize,sentiment', quiet=True) # THIS FAILED
    stanza.download('ar', processors='tokenize,sentiment') 
    nlp = stanza.Pipeline('ar', processors='tokenize,sentiment', quiet=True)
    text = "هذا مشروع رائع جداً!"
    doc = nlp(text)
    for i, sentence in enumerate(doc.sentences):
        log(f"Sentence {i}: sentiment value = {sentence.sentiment}")
except Exception as e:
    log(f"Stanza Error: {e}")

log("Finished Stanza Test 2.")
