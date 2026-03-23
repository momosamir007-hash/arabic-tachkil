import pyarabic.araby as araby

# A simple lexicon-based sentiment analyzer for Arabic
POSITIVE_WORDS = {
    'رائع', 'جميل', 'ممتاز', 'جيد', 'شكرا', 'حب', 'سعيد', 'نجاح', 'فوز', 'روعة',
    'مبدع', 'مفيد', 'راقي', 'لطيف', 'عظيم', 'خير', 'بطل', 'كريم', 'صدق', 'بارك'
}

NEGATIVE_WORDS = {
    'سيء', 'قبيح', 'فشل', 'حزن', 'غضب', 'مرض', 'خبيث', 'كره', 'صعب', 'خطأ',
    'ظلم', 'كذب', 'شر', 'بشع', 'ضعيف', 'مؤلم', 'خوف', 'خسارة', 'فوضى', 'حرام'
}

def analyze_sentiment_lexicon(text: str) -> dict:
    if not text.strip():
        return {"sentiment": "neutral", "score": 0.0}
    
    # Normalize and tokenize
    normalized = araby.strip_tashkeel(text)
    words = araby.tokenize(normalized)
    
    pos_score = 0
    neg_score = 0
    
    for word in words:
        if word in POSITIVE_WORDS:
            pos_score += 1
        elif word in NEGATIVE_WORDS:
            neg_score += 1
            
    total = pos_score + neg_score
    if total == 0:
        return {"sentiment": "neutral", "score": 0.0, "text": text}
    
    score = (pos_score - neg_score) / total
    
    if score > 0.1:
        label = "positive"
    elif score < -0.1:
        label = "negative"
    else:
        label = "neutral"
        
    return {
        "sentiment": label,
        "score": score,
        "pos_count": pos_score,
        "neg_count": neg_score,
        "text": text
    }
