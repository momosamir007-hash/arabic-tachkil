import stanza
try:
    print("Checking Stanza...")
    stanza.download('ar', processors='tokenize,sentiment', quiet=True)
    nlp = stanza.Pipeline('ar', processors='tokenize,sentiment', quiet=True)
    doc = nlp("هذا رائع")
    print(f"Stanza Sentiment Result: {doc.sentences[0].sentiment}")
except Exception as e:
    print(f"Stanza Error: {e}")

try:
    print("\nChecking Farasa...")
    from farasa.segmenter import FarasaSegmenter
    segmenter = FarasaSegmenter(interactive=True)
    res = segmenter.segment("الاختبار")
    print(f"Farasa Segment Result: {res}")
except Exception as e:
    print(f"Farasa Error: {e}")
