# adawat/nlp/dialect_sentiment.py
"""تحديد اللهجة العربية وتحليل المشاعر"""
import logging

logger = logging.getLogger(__name__)

# ============================================
# اكتشاف المكتبة المتاحة
# ============================================
BACKEND = None

# المحاولة 1: CAMeL Tools
try:
    from camel_tools.dialectid import DialectIdentifier
    # اختبار فعلي - هنا تظهر المشكلة
    _did = DialectIdentifier.pretrained()
    BACKEND = "camel"
    del _did
    logger.info("Using CAMeL Tools backend")
except Exception as e:
    logger.warning(f"CAMeL Tools غير متاح: {e}")

# المحاولة 2: Transformers
if BACKEND is None:
    try:
        from transformers import pipeline as hf_pipeline
        BACKEND = "transformers"
        logger.info("Using Transformers backend")
    except ImportError:
        logger.warning("Transformers غير مثبتة")

# المحاولة 3: لا شيء
if BACKEND is None:
    logger.error("لا توجد مكتبة متاحة لتحديد اللهجة وتحليل المشاعر")

# ============================================
# أسماء اللهجات
# ============================================
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

SENTIMENT_AR = {
    'positive': 'إيجابي 😊',
    'negative': 'سلبي 😞',
    'neutral': 'محايد 😐',
    'LABEL_0': 'سلبي 😞',
    'LABEL_1': 'محايد 😐',
    'LABEL_2': 'إيجابي 😊',
}

# ============================================
# تحديد اللهجة
# ============================================
def detect_dialect(text):
    """تحديد اللهجة العربية"""
    if not text or not text.strip():
        return {
            'error': 'لا يوجد نص',
            'status': 'error'
        }

    if BACKEND == "camel":
        return _dialect_camel(text)
    elif BACKEND == "transformers":
        return _dialect_transformers(text)
    else:
        return _no_backend_error("تحديد اللهجة")


def _dialect_camel(text):
    try:
        did = DialectIdentifier.pretrained()
        predictions = did.predict([text])
        label = str(predictions[0].top)
        return {
            'text': text,
            'dialect': label,
            'dialect_name': DIALECT_NAMES.get(label, label),
            'backend': 'camel',
            'status': 'success'
        }
    except Exception as e:
        # إذا فشل CAMeL، جرّب Transformers
        logger.warning(f"CAMeL فشل، محاولة Transformers: {e}")
        try:
            return _dialect_transformers(text)
        except Exception:
            return {'error': str(e), 'status': 'error'}


def _dialect_transformers(text):
    try:
        from transformers import pipeline as hf_pipeline
        classifier = hf_pipeline(
            "text-classification",
            model="CAMeL-Lab/bert-base-arabic-camelbert-da-did"
        )
        result = classifier(text[:512])
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
def analyze_sentiment(text):
    """تحليل المشاعر في النص العربي"""
    if not text or not text.strip():
        return [{'error': 'لا يوجد نص', 'status': 'error'}]

    if BACKEND == "camel":
        return _sentiment_camel(text)
    elif BACKEND == "transformers":
        return _sentiment_transformers(text)
    else:
        return [_no_backend_error("تحليل المشاعر")]


def _sentiment_camel(text):
    try:
        from camel_tools.sentiment import SentimentAnalyzer
        sa = SentimentAnalyzer.pretrained()
        sentences = [s.strip() for s in text.split('\n') if s.strip()]
        predictions = sa.predict(sentences)
        return [
            {
                'text': s,
                'sentiment': p,
                'sentiment_ar': SENTIMENT_AR.get(p, p),
                'backend': 'camel',
                'status': 'success'
            }
            for s, p in zip(sentences, predictions)
        ]
    except Exception as e:
        logger.warning(f"CAMeL Sentiment فشل: {e}")
        try:
            return _sentiment_transformers(text)
        except Exception:
            return [{'error': str(e), 'status': 'error'}]


def _sentiment_transformers(text):
    try:
        from transformers import pipeline as hf_pipeline
        classifier = hf_pipeline(
            "text-classification",
            model="CAMeL-Lab/bert-base-arabic-camelbert-da-sentiment"
        )
        sentences = [s.strip() for s in text.split('\n') if s.strip()]
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


# ============================================
# رسالة خطأ موحدة
# ============================================
def _no_backend_error(feature):
    return {
        'error': f'{feature} غير متاح',
        'message': 'ثبّت إحدى المكتبات التالية:',
        'options': [
            'pip install transformers torch (مُوصى به ✅)',
            'pip install camel-tools (يحتاج Python ≤ 3.10)',
        ],
        'status': 'error'
            }
