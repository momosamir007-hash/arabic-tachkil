# adawat/adaat.py
# طبقة التوافقية للملفات والسكريبتات القديمة
from .config import COMMAND_TABLE, resolve_action
from .extractors.numbers import number_to_words, extract_numbered_phrases
from .extractors.entities import (
    extract_named_entities,
    show_collocations,
    extract_all_entities
)
from .nlp.tashkeel import (
    tashkeel,
    reduce_tashkeel,
    tashkeel_suggest,
    assistant_tashkeel,
    compare_tashkeel
)
from .nlp.stemming import light_stemmer, full_stemmer
from .nlp.tagging import (
    word_tagging,
    chunk_split,
    get_bigrams,
    inverse_rhyme_sort,
    segment_language
)
from .formatters.latex import itemize, tabulize, tabbing
from .formatters.data import csv_to_python_table
from .generators.affixation import generate_affixes
from .generators.randtext import random_text
import pyarabic.araby as araby
import pyarabic.unshape

# ============================================
# محاولة استيراد تحديد اللهجة وتحليل المشاعر
# ============================================
try:
    from .nlp.dialect_sentiment import detect_dialect, analyze_sentiment
    CAMEL_AVAILABLE = True
except ImportError:
    CAMEL_AVAILABLE = False

    def detect_dialect(text):
        return {'error': 'CAMeL Tools غير مثبتة: pip install camel-tools'}

    def analyze_sentiment(text):
        return [{'error': 'CAMeL Tools غير مثبتة: pip install camel-tools'}]

# ============================================
# تحديث جدول الأوامر
# ============================================
COMMAND_TABLE.update({
    'dialect': {
        'action': 'DetectDialect',
        'help': 'detect Arabic dialect of text'
    },
    'sentiment': {
        'action': 'AnalyzeSentiment',
        'help': 'analyze sentiment of Arabic text'
    },
})

# ============================================
# أسماء بديلة للتوافقية مع الكود القديم
# ============================================
numbers_to_words = number_to_words
التفقيط = number_to_words
number2letters = number_to_words
extractNumbered = extract_numbered_phrases
tashkeel_text = tashkeel
reduced_tashkeel_text = reduce_tashkeel
tashkeel2 = tashkeel_suggest
assistanttashkeel = assistant_tashkeel
extractNamed = extract_named_entities
extractEnteties = extract_all_entities
wordtag = word_tagging
chunksplit = chunk_split
bigrams = get_bigrams
inverse = inverse_rhyme_sort
csv_to_python_table = csv_to_python_table
affixate = generate_affixes
random_text = random_text
normalize = lambda t: t
tokenize = araby.tokenize

# ============================================
# دالة المساعدة
# ============================================
def help(command=""):
    """عرض الأوامر المتاحة"""
    if command:
        helpstr = COMMAND_TABLE.get(command, {}).get("help", "")
        if not helpstr:
            return "Error: command '%s' not found" % command
        return "Command: %s : %s" % (command, helpstr)
    lines = []
    max_len = len(max(COMMAND_TABLE.keys(), key=len)) + 2
    for cmd in sorted(COMMAND_TABLE.keys()):
        helpstr = COMMAND_TABLE.get(cmd, {}).get("help", "")
        lines.append("\t%s: %s" % (cmd.ljust(max_len), helpstr))
    return "\n".join(lines)

# ============================================
# الدالة الرئيسية لتنفيذ الأوامر
# ============================================
def DoAction(text, action, options=None):
    """
    تنفيذ أمر بالاسم
    Args:
        text: النص المدخل
        action: اسم الأمر
        options: خيارات إضافية
    Returns:
        نتيجة تنفيذ الأمر
    """
    if options is None:
        options = {}
    # ترجمة اسم الأمر الخارجي إلى الداخلي
    action = COMMAND_TABLE.get(action, {}).get('action', action)
    lastmark = options.get('lastmark', '0')

    # -------- جدول التوجيه --------
    ACTION_MAP = {
        "DoNothing": lambda: text,
        "Contibute": lambda: text,
        # التشكيل
        "TashkeelText": lambda: tashkeel(text, lastmark),
        "Tashkeel2": lambda: tashkeel_suggest(text, lastmark),
        "CompareTashkeel": lambda: compare_tashkeel(text),
        "ReduceTashkeel": lambda: reduce_tashkeel(text),
        # التحليل الصرفي
        "LightStemmer": lambda: full_stemmer(text, lastmark),
        "Wordtag": lambda: word_tagging(text),
        # الاستخراج
        "extractNamed": lambda: extract_named_entities(text),
        "extractEnteties": lambda: extract_all_entities(text),
        "extractNumbered": lambda: extract_numbered_phrases(text),
        "showCollocations": lambda: show_collocations(text),
        # التحويل
        "StripHarakat": lambda: araby.strip_tashkeel(text),
        "Normalize": lambda: normalize(text),
        "Tokenize": lambda: tokenize(text),
        "Romanize": lambda: romanize(text),
        "Unshape": lambda: pyarabic.unshape.unshaping_text(text),
        "NumberToLetters": lambda: number_to_words(text),
        "Inverse": lambda: inverse_rhyme_sort(text),
        # التنسيق
        "Poetry": lambda: justify_poetry(text),
        "CsvToData": lambda: csv_to_python_table(text),
        "Affixate": lambda: generate_affixes(text),
        "Itemize": lambda: itemize(text),
        "Tabulize": lambda: tabulize(text),
        "Tabbing": lambda: tabbing(text),
        # التقطيع
        "chunk": lambda: chunk_split(text),
        "bigrams": lambda: get_bigrams(text),
        "Language": lambda: segment_language(text),
        # اللهجة والمشاعر
        "DetectDialect": lambda: detect_dialect(text),
        "AnalyzeSentiment": lambda: analyze_sentiment(text),
        # نصوص عشوائية
        "RandomText": lambda: random_text(),
    }

    handler = ACTION_MAP.get(action)
    if handler:
        return handler()
    return text

# ============================================
# دوال مساعدة
# ============================================
def romanize(text, code="ISO"):
    """تحويل النص العربي إلى لاتيني"""
    try:
        import pyarabic.trans
        return pyarabic.trans.convert(text, 'arabic', 'tim')
    except ImportError:
        return text

def justify_poetry(text):
    """تنسيق نص شعري"""
    lines = text.splitlines()
    lines = [l for l in lines if l.strip()]
    rows = []
    for line in lines:
        parts = [p for p in line.strip().split("\t") if p.strip()]
        if len(parts) == 2:
            rows.append(parts)
    return rows
