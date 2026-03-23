import stanza
import stanza.resources.common as common

def log(msg):
    with open("debug_log.txt", "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

log("Checking available processors for Arabic 'ar'...")

try:
    resources = common.load_resources_json()
    if 'ar' in resources:
        ar_models = resources['ar']
        log(f"Available processors for 'ar': {list(ar_models.keys())}")
        if 'sentiment' in ar_models:
            log(f"Sentiment models for 'ar': {ar_models['sentiment']}")
        else:
            log("Sentiment NOT found for 'ar' in resources.")
except Exception as e:
    log(f"Resource check Error: {e}")
