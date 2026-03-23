def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("Starting test_log.py...")

try:
    import asmai.sentiment as sentiment
    log("Asmai imported successfully.")
    text = "رائع"
    res = sentiment.analyze(text)
    log(f"Asmai Result: {res}")
except Exception as e:
    log(f"Asmai Error: {e}")

try:
    import stanza
    log("Stanza imported successfully.")
    # Don't download for now, just check if it can be initialized
    log("Stanza version: " + str(stanza.__version__))
except Exception as e:
    log(f"Stanza Error: {e}")

log("Finished test_log.py.")
