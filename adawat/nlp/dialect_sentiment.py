# adawat/nlp/dialect_sentiment.py
"""تحديد اللهجة العربية وتحليل المشاعر"""

# ============================================
# محاولة استيراد المكتبات المتاحة
# ============================================
BACKEND = None

try:
    from camel_tools.dialectid import DialectIdentifier
    from camel_tools.sentiment import SentimentAnalyzer
    # اختبار فعلي للنموذج
    _test_did = DialectIdentifier.pretrained()
    BACKEND = "camel"
    del _test_did
except Exception:
    try:
        from transformers import pipeline
        BACKEND = "transformers"
    except ImportError:
        BACKEND = None

# ============================================
# تحديد اللهجة
# ============================================
def detect_dialect(text):
    """تحديد اللهجة العربية"""
    if not text or not text.strip():
        return {'error': 'لا يوجد نص', 'status': 'error'}

    if BACKEND == "camel":
        return _dialect_camel(text)
    elif BACKEND == "transformers":
        return _dialect_transformers(text)
    else:
        return {
            'error': 'لا توجد مكتبة متاحة لتحديد اللهجة',
            'install': 'pip install transformers torch',
            'status': 'error'
        }


def _dialect_camel(text):
    """تحديد اللهجة باستخدام CAMeL Tools"""
    try:
        did = DialectIdentifier.pretrained()
        predictions = did.predict([text])
        return {
            'text': text,
            'dialect': str(predictions[0].top),
            'backend': 'camel',
            'status': 'success'
        }
    except Exception as e:
        return {'error': str(e), 'status': 'error'}


def _dialect_transformers(text):
    """تحديد اللهجة باستخدام Hugging Face Transformers"""
    try:
        classifier = pipeline(
            "text-classification",
            model="CAMeL-Lab/bert-base-arabic-camelbert-da-did"
        )
        result = classifier(text[:512])  # حد أقصى 512 حرف

        # ترجمة رمز اللهجة
        DIALECT_NAMES = {
            'AE': 'إماراتية 🇦🇪',
            'BH': 'بحرينية 🇧🇭',
            'DZ': 'جزائرية 🇩🇿',
            'EG': 'مصرية 🇪🇬',
            'IQ': 'عراقية 🇮🇶',
            'JO': 'أردنية 🇯🇴',
            'KW': 'كويتية 🇰🇼',
            'LB': 'لبنانية 🇱🇧',
            'LY': 'ليبية 🇱🇾',
            'MA': 'مغربية 🇲🇦',
            'MSA': 'فصحى 📖',
            'OM': 'عمانية 🇴🇲',
            'PL': 'فلسطينية 🇵🇸',
            'QA': 'قطرية 🇶🇦',
            'SA': 'سعودية 🇸🇦',
            'SD': 'سودانية 🇸🇩',
            'SY': 'سورية 🇸🇾',
            'TN': 'تونسية 🇹🇳',
            'YE': 'يمنية 🇾🇪',
        }
        label = result[0]['label']
        score = round(result[0]['score'] * 100, 2)
        return {
            'text': text,
            'dialect': label,
            'dialect_name': DIALECT_NAMES.get(label, label),
            'confidence': f"{score}%",
            'backend': 'transformers',
            'status': 'success'
        }
    except Exception as e:
        return {'error': str(e), 'status': 'error'}


# ============================================
# تحليل المشاعر
# ============================================
SENTIMENT_AR = {
    'positive': 'إيجابي 😊',
    'negative': 'سلبي 😞',
    'neutral': 'محايد 😐',
    'LABEL_0': 'سلبي 😞',
    'LABEL_1': 'محايد 😐',
    'LABEL_2': 'إيجابي 😊',
}


def analyze_sentiment(text):
    """تحليل المشاعر في النص العربي"""
    if not text or not text.strip():
        return [{'error': 'لا يوجد نص', 'status': 'error'}]

    if BACKEND == "camel":
        return _sentiment_camel(text)
    elif BACKEND == "transformers":
        return _sentiment_transformers(text)
    else:
        return [{
            'error': 'لا توجد مكتبة متاحة لتحليل المشاعر',
            'install': 'pip install transformers torch',
            'status': 'error'
        }]


def _sentiment_camel(text):
    """تحليل المشاعر باستخدام CAMeL Tools"""
    try:
        sa = SentimentAnalyzer.pretrained()
        sentences = [s.strip() for s in text.strip().split('\n') if s.strip()]
        predictions = sa.predict(sentences)
        return [
            {
                'text': sent,
                'sentiment': pred,
                'sentiment_ar': SENTIMENT_AR.get(pred, pred),
                'backend': 'camel',
                'status': 'success'
            }
            for sent, pred in zip(sentences, predictions)
        ]
    except Exception as e:
        return [{'error': str(e), 'status': 'error'}]


def _sentiment_transformers(text):
    """تحليل المشاعر باستخدام Hugging Face Transformers"""
    try:
        classifier = pipeline(
            "text-classification",
            model="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"
        )
        sentences = [s.strip() for s in text.strip().split('\n') if s.strip()]
        results = []
        for sentence in sentences:
            result = classifier(sentence[:512])
            label = result[0]['label']
            score = round(result[0]['score'] * 100, 2)
            results.append({
                'text': sentence,
                'sentiment': label,
                'sentiment_ar': SENTIMENT_AR.get(label, label),
                'confidence': f"{score}%",
                'backend': 'transformers',
                'status': 'success'
            })
        return results
    except Exception as e:
        return [{'error': str(e), 'status': 'error'}]
