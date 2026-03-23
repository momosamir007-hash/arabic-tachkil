# adawat/nlp/dialect_sentiment.py
"""تحديد اللهجة العربية وتحليل المشاعر باستخدام CAMeL Tools"""

def detect_dialect(text):
    """
    تحديد اللهجة العربية
    Args:
        text: النص المدخل
    Returns:
        dict: نتيجة تحديد اللهجة
    """
    try:
        from camel_tools.dialectid import DialectIdentifier
        did = DialectIdentifier.pretrained()
        predictions = did.predict([text])
        return {
            'text': text,
            'dialect': str(predictions[0].top),
            'status': 'success'
        }
    except ImportError:
        return {
            'error': 'CAMeL Tools غير مثبتة',
            'install': 'pip install camel-tools && camel_data -i all',
            'status': 'error'
        }
    except Exception as e:
        return {
            'error': str(e),
            'status': 'error'
        }


def analyze_sentiment(text):
    """
    تحليل المشاعر في النص العربي
    Args:
        text: النص المدخل
    Returns:
        list: نتائج تحليل المشاعر لكل جملة
    """
    SENTIMENT_AR = {
        'positive': 'إيجابي 😊',
        'negative': 'سلبي 😞',
        'neutral': 'محايد 😐'
    }
    try:
        from camel_tools.sentiment import SentimentAnalyzer
        sa = SentimentAnalyzer.pretrained()
        sentences = [s.strip() for s in text.strip().split('\n') if s.strip()]
        if not sentences:
            return [{'error': 'لا يوجد نص للتحليل', 'status': 'error'}]
        predictions = sa.predict(sentences)
        results = []
        for sentence, prediction in zip(sentences, predictions):
            results.append({
                'text': sentence,
                'sentiment': prediction,
                'sentiment_ar': SENTIMENT_AR.get(prediction, prediction),
                'status': 'success'
            })
        return results
    except ImportError:
        return [{
            'error': 'CAMeL Tools غير مثبتة',
            'install': 'pip install camel-tools && camel_data -i all',
            'status': 'error'
        }]
    except Exception as e:
        return [{
            'error': str(e),
            'status': 'error'
        }]
