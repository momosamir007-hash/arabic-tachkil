import asmai.sentiment as sentiment
try:
    print("Testing Asmai Sentiment...")
    text = "هذا مشروع رائع جداً!"
    res = sentiment.analyze(text)
    print(f"Result for '{text}': {res}")
    
    text = "هذا سيء جدا"
    res = sentiment.analyze(text)
    print(f"Result for '{text}': {res}")
except Exception as e:
    print(f"Asmai Error: {e}")
