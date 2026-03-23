# test_dialect.py
from adawat.nlp.dialect_sentiment import detect_dialect, analyze_sentiment, BACKEND

print(f"Backend: {BACKEND}")

# اختبار اللهجة
tests = [
    "كيفاش راك لاباس",  # جزائرية
    "إيش لونك وش أخبارك",  # سعودية
    "إزيك عامل إيه",  # مصرية
    "هذا كتاب مفيد جداً",  # فصحى
    "شلونك شخبارك",  # عراقية/كويتية
    "كيفك شو عم تعمل",  # لبنانية/سورية
]

print("\n=== تحديد اللهجة ===")
for t in tests:
    result = detect_dialect(t)
    if result['status'] == 'success':
        name = result.get('dialect_name', result['dialect'])
        print(f" '{t}' → {name}")
    else:
        print(f" ❌ {result['error']}")

# اختبار المشاعر
print("\n=== تحليل المشاعر ===")
sentiment_tests = "الفيلم رائع جداً\nالخدمة سيئة للغاية\nالجو معتدل اليوم"
results = analyze_sentiment(sentiment_tests)
for r in results:
    if r['status'] == 'success':
        print(f" '{r['text']}' → {r['sentiment_ar']}")
    else:
        print(f" ❌ {r['error']}")
