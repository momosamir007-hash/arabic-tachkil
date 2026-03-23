# ═══════════════════════════════════════════════════════════
#  app.py — أدوات Adawat | Streamlit Interface v0.2.0
# ═══════════════════════════════════════════════════════════

import streamlit as st
import json
import traceback
from typing import Any

# ─────────────────────────────────────────────────────────
# 1) إعداد الصفحة — يجب أن يكون أول أمر Streamlit
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="أدوات — Adawat",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# 2) فحص التبعيات عند بدء التشغيل
# ─────────────────────────────────────────────────────────
REQUIRED_PACKAGES = {
    "pyarabic":   "pyarabic",
    "maskouk":    "maskouk-pysqlite",
    "mishkal":    "mishkal",
    "qalsadi":    "qalsadi",
    "naftawayh":  "naftawayh",
    "tashaphyne": "tashaphyne",
    "asmai":      "asmai",
    "sylajone":   "sylajone",
    "arramooz":   "arramooz-pysqlite",
    "stanza":     "stanza",
    "pydantic":   "pydantic>=2.0",
}

PYPI_MAP = {
    "maskouk":   "maskouk-pysqlite",
    "arramooz":  "arramooz-pysqlite",
    "mishkal":   "mishkal",
    "qalsadi":   "qalsadi",
    "naftawayh": "naftawayh",
    "tashaphyne": "tashaphyne",
    "asmai":     "asmai",
    "sylajone":  "sylajone",
    "stanza":    "stanza",
}

missing_packages = []
installed_packages = []
for module_name, pip_name in REQUIRED_PACKAGES.items():
    try:
        __import__(module_name)
        installed_packages.append(module_name)
    except ImportError:
        missing_packages.append(pip_name)


# ─────────────────────────────────────────────────────────
# 3) CSS مخصص
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

    /* ─── Global RTL ─── */
    .main .block-container {
        direction: rtl;
        text-align: right;
    }

    /* ─── Arabic Font ─── */
    * {
        font-family: 'Tajawal', sans-serif !important;
    }

    /* ─── Header ─── */
    .app-header {
        background: linear-gradient(135deg, #D4A017 0%, #8B6914 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    .app-header h1 {
        margin: 0;
        font-size: 2.2rem;
    }
    .app-header p {
        margin: 0.3rem 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }

    /* ─── Result Box ─── */
    .result-box {
        background: #0a3d62;
        border-right: 5px solid #D4A017;
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        direction: rtl;
        text-align: right;
        font-size: 1.15rem;
        line-height: 2.2;
        color: #e0e0e0;
        white-space: pre-wrap;
    }

    /* ─── Category Badges ─── */
    .category-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .cat-nlp       { background: #1abc9c; color: #fff; }
    .cat-extract   { background: #3498db; color: #fff; }
    .cat-format    { background: #9b59b6; color: #fff; }
    .cat-generate  { background: #e67e22; color: #fff; }
    .cat-basic     { background: #e74c3c; color: #fff; }
    .cat-advanced  { background: #2c3e50; color: #fff; }

    /* ─── Text Area RTL ─── */
    .stTextArea textarea {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1.1rem;
        line-height: 1.8;
    }

    /* ─── Text Input RTL ─── */
    .stTextInput input {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif !important;
    }

    /* ─── Sidebar ─── */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    /* ─── Status Cards ─── */
    .status-ok {
        color: #27ae60;
        font-weight: bold;
    }
    .status-err {
        color: #e74c3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# 4) تعريف جميع الأدوات (بديل COMMAND_TABLE)
# ─────────────────────────────────────────────────────────
TOOLS = {
    "🗣️ معالجة لغوية (NLP)": {
        "category_class": "cat-nlp",
        "tools": {
            "التشكيل التلقائي": {
                "action": "TashkeelText",
                "icon": "✏️",
                "has_options": True,
                "needs_text": True,
                "description": "إضافة الحركات للنص العربي تلقائياً",
                "requires": ["mishkal", "tashaphyne"],
            },
            "اقتراح التشكيل": {
                "action": "Tashkeel2",
                "icon": "💡",
                "has_options": True,
                "needs_text": True,
                "description": "اقتراح تشكيلات بديلة للنص",
                "requires": ["mishkal", "tashaphyne"],
            },
            "التجذيع": {
                "action": "LightStemmer",
                "icon": "🌿",
                "has_options": True,
                "needs_text": True,
                "description": "استخراج جذوع الكلمات العربية",
                "requires": ["qalsadi", "tashaphyne"],
            },
            "وسم الكلمات (POS)": {
                "action": "Wordtag",
                "icon": "🏷️",
                "has_options": False,
                "needs_text": True,
                "description": "تحديد نوع كل كلمة (اسم، فعل، حرف...)",
                "requires": ["qalsadi"],
            },
            "التقطيع (Chunking)": {
                "action": "chunk",
                "icon": "✂️",
                "has_options": False,
                "needs_text": True,
                "description": "تقسيم الجمل إلى أجزاء نحوية",
                "requires": ["qalsadi"],
            },
            "الثنائيات (Bigrams)": {
                "action": "bigrams",
                "icon": "🔗",
                "has_options": False,
                "needs_text": True,
                "description": "استخراج أزواج الكلمات المتتالية",
                "requires": ["pyarabic"],
            },
            "الترتيب المعكوس (قافية)": {
                "action": "Inverse",
                "icon": "🔄",
                "has_options": False,
                "needs_text": True,
                "description": "ترتيب الكلمات حسب أواخرها (للقوافي)",
                "requires": ["pyarabic"],
            },
            "فصل اللغات": {
                "action": "Language",
                "icon": "🌐",
                "has_options": False,
                "needs_text": True,
                "description": "فصل النصوص العربية عن الأجنبية",
                "requires": ["pyarabic"],
            },
            "تحليل المشاعر": {
                "action": "Sentiment",
                "icon": "🎭",
                "has_options": False,
                "needs_text": True,
                "description": "تحديد المشاعر (إيجابي / سلبي / محايد)",
                "requires": ["asmai"],
            },
            "تحديد اللهجة": {
                "action": "Dialect",
                "icon": "🗺️",
                "has_options": False,
                "needs_text": True,
                "description": "تحديد لهجة النص العربي",
                "requires": [],
            },
        },
    },
    "🔍 الاستخراج": {
        "category_class": "cat-extract",
        "tools": {
            "الأرقام إلى حروف": {
                "action": "NumberToLetters",
                "icon": "🔢",
                "has_options": False,
                "needs_text": True,
                "description": "تحويل الأرقام في النص إلى كلمات عربية",
                "requires": ["naftawayh"],
            },
            "استخراج المرقّمات": {
                "action": "extractNumbered",
                "icon": "📋",
                "has_options": False,
                "needs_text": True,
                "description": "استخراج العناصر المرقّمة من النص",
                "requires": ["pyarabic"],
            },
            "استخراج الأسماء": {
                "action": "extractNamed",
                "icon": "👤",
                "has_options": False,
                "needs_text": True,
                "description": "استخراج أسماء الأشخاص والأماكن",
                "requires": ["pyarabic"],
            },
            "المتلازمات اللفظية": {
                "action": "showCollocations",
                "icon": "🤝",
                "has_options": False,
                "needs_text": True,
                "description": "استخراج المتلازمات اللفظية (collocations)",
                "requires": ["maskouk"],
            },
        },
    },
    "📄 التنسيق": {
        "category_class": "cat-format",
        "tools": {
            "تنسيق Itemize (LaTeX)": {
                "action": "Itemize",
                "icon": "📝",
                "has_options": False,
                "needs_text": True,
                "description": "تحويل النص إلى قائمة LaTeX itemize",
                "requires": [],
            },
            "تنسيق جدول (LaTeX)": {
                "action": "Tabulize",
                "icon": "📊",
                "has_options": False,
                "needs_text": True,
                "description": "تحويل النص إلى جدول LaTeX",
                "requires": [],
            },
            "تنسيق Tabbing (LaTeX)": {
                "action": "Tabbing",
                "icon": "📐",
                "has_options": False,
                "needs_text": True,
                "description": "تحويل النص إلى tabbing LaTeX",
                "requires": [],
            },
            "CSV إلى جدول Python": {
                "action": "CsvToData",
                "icon": "🔄",
                "has_options": False,
                "needs_text": True,
                "description": "تحويل CSV إلى بنية بيانات Python",
                "requires": [],
            },
        },
    },
    "⚙️ التوليد": {
        "category_class": "cat-generate",
        "tools": {
            "توليد اللواصق": {
                "action": "Affixate",
                "icon": "🔧",
                "has_options": False,
                "needs_text": True,
                "description": "توليد تصريفات الكلمة مع اللواصق",
                "requires": ["pyarabic"],
            },
            "نص عشوائي": {
                "action": "RandomText",
                "icon": "🎲",
                "has_options": False,
                "needs_text": False,
                "description": "توليد نص عربي عشوائي",
                "requires": [],
            },
        },
    },
    "🔤 العمليات الأساسية": {
        "category_class": "cat-basic",
        "tools": {
            "إزالة التشكيل": {
                "action": "StripHarakat",
                "icon": "🧹",
                "has_options": False,
                "needs_text": True,
                "description": "إزالة جميع الحركات من النص",
                "requires": ["pyarabic"],
            },
            "تقطيع النص (Tokenize)": {
                "action": "Tokenize",
                "icon": "🔤",
                "has_options": False,
                "needs_text": True,
                "description": "تقسيم النص إلى كلمات مفردة",
                "requires": ["pyarabic"],
            },
        },
    },
    "🧠 التحليل المتقدم": {
        "category_class": "cat-advanced",
        "tools": {
            "تحليل Stanza": {
                "action": "Stanza",
                "icon": "🏗️",
                "has_options": False,
                "needs_text": True,
                "description": "تحليل نحوي متقدم باستخدام Stanza (Stanford)",
                "requires": ["stanza"],
            },
            "Farasa NER": {
                "action": "FarasaNER",
                "icon": "🎯",
                "has_options": False,
                "needs_text": True,
                "description": "التعرف على الكيانات المسماة بـ Farasa",
                "requires": [],
            },
        },
    },
}

# ── نصوص نموذجية لكل أداة ──
SAMPLE_TEXTS = {
    "TashkeelText":     "ذهب الطالب الى المدرسة وتعلم دروسا جديدة في اللغة العربية",
    "Tashkeel2":        "كتب الشاعر قصيدة جميلة عن الوطن",
    "LightStemmer":     "المدرسون يعلمون الطلاب ويرشدونهم",
    "Wordtag":          "سافر الرجل إلى القاهرة يوم الجمعة",
    "chunk":            "ذهب الرجل الطويل إلى السوق الكبير واشترى خبزا طازجا",
    "bigrams":          "العلم نور والجهل ظلام والعمل عبادة",
    "Inverse":          "قمر\nنهر\nزهر\nبحر\nفجر",
    "Language":         "هذا نص عربي مع some English words مختلطة فيه",
    "NumberToLetters":  "في المكتبة 350 كتابا وفي القاعة 12 طالبا",
    "extractNumbered":  "1. الفصل الأول\n2. الفصل الثاني\n3. الفصل الثالث",
    "extractNamed":     "سافر محمد إلى القاهرة والتقى بأحمد في جامعة الأزهر",
    "showCollocations": "بسم الله الرحمن الرحيم الحمد لله رب العالمين الرحمن الرحيم",
    "Itemize":          "العنصر الأول\nالعنصر الثاني\nالعنصر الثالث",
    "Tabulize":         "الاسم\tالعمر\tالمدينة\nأحمد\t25\tالرياض\nسارة\t30\tجدة",
    "Tabbing":          "المفتاح\tالقيمة\nاسم\tأحمد\nعمر\t25",
    "CsvToData":        "name,age,city\nAhmed,25,Riyadh\nSara,30,Jeddah",
    "Affixate":         "كتب",
    "StripHarakat":     "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ",
    "Tokenize":         "ذهب الطالب إلى المدرسة، وتعلّم دروساً جديدة.",
    "Sentiment":        "هذا الفيلم رائع جداً وأنصح الجميع بمشاهدته",
    "Dialect":          "ايش تبي تسوي اليوم يا خوي",
    "Stanza":           "درس الطالب في الجامعة",
    "FarasaNER":        "يعيش محمد بن سلمان في المملكة العربية السعودية",
}


# ─────────────────────────────────────────────────────────
# 5) دوال الاستيراد الآمن + التنفيذ
# ─────────────────────────────────────────────────────────
def safe_import(module_path: str, func_name: str):
    """
    استيراد آمن لدالة من وحدة — يُرجع الدالة أو يرفع خطأً واضحاً
    """
    import importlib
    try:
        module = importlib.import_module(module_path)
        return getattr(module, func_name)
    except ImportError as e:
        missing = str(e).split("'")[-2] if "'" in str(e) else str(e)
        pip_name = PYPI_MAP.get(missing, missing)
        raise ImportError(
            f"❌ مكتبة «{missing}» غير مثبّتة.\n"
            f"💡 الحل:\n"
            f"   pip install {pip_name}"
        )
    except AttributeError:
        raise AttributeError(
            f"❌ الدالة «{func_name}» غير موجودة في «{module_path}»"
        )


def execute_action(action_name: str, text: str, options: dict) -> Any:
    """
    محرّك التنفيذ — يطابق تماماً منطق FastAPI endpoint
    يستخدم استيراداً آمناً لكل وحدة
    """
    lastmark = options.get("lastmark", True)

    # ═══════════════════════════════════════════
    #  الاستخراج
    # ═══════════════════════════════════════════
    if action_name == "NumberToLetters":
        func = safe_import("adawat.extractors.numbers", "number_to_words")
        return func(text)

    elif action_name == "extractNumbered":
        func = safe_import("adawat.extractors.numbers", "extract_numbered_phrases")
        return func(text)

    elif action_name == "extractNamed":
        func = safe_import("adawat.extractors.entities", "extract_named_entities")
        return func(text)

    elif action_name == "showCollocations":
        func = safe_import("adawat.extractors.entities", "show_collocations")
        return func(text)

    # ═══════════════════════════════════════════
    #  NLP — التشكيل والتجذيع
    # ═══════════════════════════════════════════
    elif action_name == "TashkeelText":
        func = safe_import("adawat.nlp.tashkeel", "tashkeel")
        return func(text, lastmark)

    elif action_name == "Tashkeel2":
        func = safe_import("adawat.nlp.tashkeel", "tashkeel_suggest")
        return func(text, lastmark)

    elif action_name == "LightStemmer":
        func = safe_import("adawat.nlp.stemming", "full_stemmer")
        return func(text, lastmark)

    # ═══════════════════════════════════════════
    #  NLP — الوسم والتحليل
    # ═══════════════════════════════════════════
    elif action_name == "Wordtag":
        func = safe_import("adawat.nlp.tagging", "word_tagging")
        return func(text)

    elif action_name == "chunk":
        func = safe_import("adawat.nlp.tagging", "chunk_split")
        return func(text)

    elif action_name == "bigrams":
        func = safe_import("adawat.nlp.tagging", "get_bigrams")
        return func(text)

    elif action_name == "Inverse":
        func = safe_import("adawat.nlp.tagging", "inverse_rhyme_sort")
        return func(text)

    elif action_name == "Language":
        func = safe_import("adawat.nlp.tagging", "segment_language")
        return func(text)

    elif action_name == "Sentiment":
        func = safe_import("adawat.nlp.sentiment", "get_sentiment")
        return func(text)

    elif action_name == "Dialect":
        func = safe_import("adawat.nlp.dialect", "identify_dialect")
        return func(text)

    # ═══════════════════════════════════════════
    #  التنسيق
    # ═══════════════════════════════════════════
    elif action_name == "Itemize":
        func = safe_import("adawat.formatters.latex", "itemize")
        return func(text)

    elif action_name == "Tabulize":
        func = safe_import("adawat.formatters.latex", "tabulize")
        return func(text)

    elif action_name == "Tabbing":
        func = safe_import("adawat.formatters.latex", "tabbing")
        return func(text)

    elif action_name == "CsvToData":
        func = safe_import("adawat.formatters.data", "csv_to_python_table")
        return func(text)

    # ═══════════════════════════════════════════
    #  التوليد
    # ═══════════════════════════════════════════
    elif action_name == "Affixate":
        func = safe_import("adawat.generators.affixation", "generate_affixes")
        return func(text)

    elif action_name == "RandomText":
        func = safe_import("adawat.generators.randtext", "random_text")
        return func()

    # ═══════════════════════════════════════════
    #  العمليات الأساسية (pyarabic مباشرة)
    # ═══════════════════════════════════════════
    elif action_name == "StripHarakat":
        import pyarabic.araby as araby
        return araby.strip_tashkeel(text)

    elif action_name == "Tokenize":
        import pyarabic.araby as araby
        return araby.tokenize(text)

    # ═══════════════════════════════════════════
    #  التحليل المتقدم
    # ═══════════════════════════════════════════
    elif action_name == "Stanza":
        func = safe_import("adawat.nlp.advanced_nlp", "stanza_analyze")
        return func(text)

    elif action_name == "FarasaNER":
        func = safe_import("adawat.nlp.advanced_nlp", "farasa_ner")
        return func(text)

    else:
        raise ValueError(f"❌ إجراء غير معروف: {action_name}")


# ─────────────────────────────────────────────────────────
# 6) دالة عرض النتائج بذكاء
# ─────────────────────────────────────────────────────────
def render_result(result: Any, action_name: str):
    """عرض النتيجة بأنسب شكل حسب نوعها والإجراء"""

    # ── None ──
    if result is None:
        st.info("ℹ️ لم تُرجع الأداة أي نتيجة.")
        return

    # ── قائمة (list) ──
    if isinstance(result, list):

        if not result:
            st.info("ℹ️ القائمة فارغة — لا توجد نتائج.")
            return

        # قائمة من قواميس → جدول
        if isinstance(result[0], dict):
            import pandas as pd
            df = pd.DataFrame(result)
            st.dataframe(df, use_container_width=True, hide_index=True)

        # قائمة من أزواج (tuples / lists) → جدول
        elif isinstance(result[0], (list, tuple)):
            import pandas as pd
            df = pd.DataFrame(result)
            st.dataframe(df, use_container_width=True, hide_index=True)

        # قائمة قصيرة ≤ 30 → شرائح (chips)
        elif len(result) <= 30:
            cols_count = min(len(result), 6)
            cols = st.columns(cols_count)
            for i, item in enumerate(result):
                with cols[i % cols_count]:
                    st.code(str(item), language=None)

        # قائمة طويلة → نص متصل
        else:
            st.markdown(
                '<div class="result-box">'
                + " ◈ ".join(str(x) for x in result)
                + "</div>",
                unsafe_allow_html=True,
            )

        st.caption(f"📊 عدد العناصر: {len(result)}")

    # ── قاموس (dict) ──
    elif isinstance(result, dict):

        # فحص إذا كان قاموس خطأ (fallback)
        if "error" in result:
            st.warning(result["error"])
            if "fix" in result:
                st.code(result["fix"], language="bash")
            return

        for key, val in result.items():
            st.markdown(f"**{key}:**")
            if isinstance(val, (list, dict)):
                render_result(val, action_name)
            else:
                st.markdown(
                    f'<div class="result-box">{val}</div>',
                    unsafe_allow_html=True,
                )

    # ── نص (str) ──
    elif isinstance(result, str):
        # كود LaTeX أو كود عام
        code_actions = ("Itemize", "Tabulize", "Tabbing", "CsvToData")
        if action_name in code_actions:
            st.code(result, language="latex")
        else:
            st.markdown(
                f'<div class="result-box">{result}</div>',
                unsafe_allow_html=True,
            )

    # ── رقم ──
    elif isinstance(result, (int, float)):
        st.metric(label="النتيجة", value=result)

    # ── أي نوع آخر ──
    else:
        st.write(result)


# ─────────────────────────────────────────────────────────
# 7) دالة فحص جاهزية أداة معيّنة
# ─────────────────────────────────────────────────────────
def check_tool_ready(tool_info: dict) -> tuple[bool, list[str]]:
    """
    فحص إذا كانت جميع تبعيات الأداة مثبّتة
    يُرجع (True/False, [قائمة المفقود])
    """
    missing = []
    for mod in tool_info.get("requires", []):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return (len(missing) == 0, missing)


# ═══════════════════════════════════════════════════════════
#                   8) واجهة التطبيق
# ═══════════════════════════════════════════════════════════

# ── العنوان الرئيسي ──
st.markdown("""
<div class="app-header">
    <h1>🛠️ أدوات — Adawat</h1>
    <p>منصة متكاملة لمعالجة اللغة العربية الطبيعية</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────
# الشريط الجانبي
# ──────────────────────────────
with st.sidebar:

    st.markdown("## 🛠️ لوحة التحكم")
    st.markdown("---")

    # ── حالة التبعيات ──
    if missing_packages:
        st.error(f"⚠️ حزم مفقودة: {len(missing_packages)}")
        with st.expander("عرض الحزم المفقودة"):
            for pkg in missing_packages:
                st.markdown(f"- `{pkg}`")
            install_cmd = "pip install " + " ".join(missing_packages)
            st.code(install_cmd, language="bash")
    else:
        st.success("✅ جميع الحزم مثبّتة")

    st.markdown("---")

    # ── اختيار الفئة ──
    category = st.selectbox(
        "📂 الفئة:",
        list(TOOLS.keys()),
        index=0,
    )
    cat_info = TOOLS[category]

    # ── اختيار الأداة ──
    tool_names = list(cat_info["tools"].keys())
    tool_name = st.selectbox(
        "🔧 الأداة:",
        tool_names,
        index=0,
    )
    tool_info = cat_info["tools"][tool_name]
    action_name = tool_info["action"]

    # ── وصف الأداة ──
    st.caption(tool_info.get("description", ""))

    st.markdown("---")

    # ── خيارات إضافية ──
    options = {}
    if tool_info.get("has_options"):
        st.markdown("### ⚙️ خيارات")
        options["lastmark"] = st.checkbox(
            "علامة آخر الكلمة (lastmark)",
            value=True,
            help="إضافة حركة آخر الكلمة عند التشكيل أو التجذيع",
        )

    # ── حالة الأداة ──
    is_ready, tool_missing = check_tool_ready(tool_info)
    st.markdown("---")
    st.markdown(
        f'<span class="category-badge {cat_info["category_class"]}">'
        f"{category}</span>",
        unsafe_allow_html=True,
    )

    if is_ready:
        st.markdown('<span class="status-ok">● جاهزة للاستخدام</span>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-err">● تبعيات مفقودة</span>',
                    unsafe_allow_html=True)
        for m in tool_missing:
            pip_n = PYPI_MAP.get(m, m)
            st.code(f"pip install {pip_n}", language="bash")

    st.caption(f"الإجراء: `{action_name}`")


# ──────────────────────────────
# المنطقة الرئيسية
# ──────────────────────────────
st.markdown(f"## {tool_info['icon']} {tool_name}")
st.caption(tool_info.get("description", ""))

# ── حقل الإدخال ──
needs_text = tool_info.get("needs_text", True)
text = ""

if needs_text:
    text = st.text_area(
        "📝 أدخل النص:",
        value=SAMPLE_TEXTS.get(action_name, "أدخل النص العربي هنا..."),
        height=160,
        key="main_input",
    )

# ── أزرار التحكم ──
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

with col_btn1:
    run_clicked = st.button(
        f"▶️  تنفيذ: {tool_name}",
        type="primary",
        use_container_width=True,
        disabled=(not is_ready),
    )

with col_btn2:
    if st.button("🗑️ مسح", use_container_width=True):
        st.rerun()

with col_btn3:
    copy_mode = st.checkbox("📋 وضع النسخ", value=False)

# ── رسالة إذا الأداة غير جاهزة ──
if not is_ready:
    st.warning(
        f"⚠️ هذه الأداة تحتاج إلى تثبيت: "
        f"**{', '.join(PYPI_MAP.get(m, m) for m in tool_missing)}**"
    )
    install_all = "pip install " + " ".join(PYPI_MAP.get(m, m) for m in tool_missing)
    st.code(install_all, language="bash")


# ── التنفيذ ──
if run_clicked:
    if needs_text and not text.strip():
        st.warning("⚠️ الرجاء إدخال نص أولاً!")
    else:
        with st.spinner(f"⏳ جارٍ تنفيذ «{tool_name}»..."):
            try:
                result = execute_action(action_name, text, options)

                st.success(f"✅ تم تنفيذ «{tool_name}» بنجاح")
                st.markdown("### 📤 النتيجة:")

                # ── وضع النسخ ──
                if copy_mode:
                    if isinstance(result, str):
                        raw = result
                        lang = None
                    else:
                        raw = json.dumps(result, ensure_ascii=False, indent=2)
                        lang = "json"
                    st.code(raw, language=lang)

                # ── العرض الذكي ──
                else:
                    render_result(result, action_name)

                # ── تفاصيل التنفيذ ──
                with st.expander("🔍 تفاصيل الاستجابة (Debug)"):
                    debug_data = {
                        "action_executed": action_name,
                        "input_length": len(text) if text else 0,
                        "result_type": type(result).__name__,
                    }
                    # JSON-safe result
                    try:
                        json.dumps(result, ensure_ascii=False)
                        debug_data["result"] = result
                    except (TypeError, ValueError):
                        debug_data["result"] = str(result)

                    st.json(debug_data)

            except ImportError as e:
                st.error(str(e))
                st.info("💡 قم بتثبيت المكتبة المطلوبة ثم أعد تشغيل التطبيق.")

            except Exception as e:
                st.error(f"❌ خطأ أثناء التنفيذ: {str(e)}")
                with st.expander("🐛 تفاصيل الخطأ"):
                    st.code(traceback.format_exc())


# ═══════════════════════════════════════════════════════════
#  9) وضع API للمطورين (اختياري)
# ═══════════════════════════════════════════════════════════
st.markdown("---")

with st.expander("🔌 استدعاء API مباشر (للمطوّرين)"):
    st.markdown(
        "يمكنك محاكاة طلب API كما في FastAPI الأصلي "
        "(`POST /api/v1/process`):"
    )

    api_col1, api_col2 = st.columns(2)

    with api_col1:
        api_action = st.text_input(
            "الإجراء (action):",
            value=action_name,
            key="api_action",
        )
    with api_col2:
        api_opts = st.text_input(
            "الخيارات (JSON):",
            value="{}",
            key="api_opts",
        )

    api_text = st.text_area(
        "النص:",
        value=text if needs_text else "",
        height=80,
        key="api_text",
    )

    if st.button("🚀 إرسال طلب API", use_container_width=True):
        try:
            parsed_opts = json.loads(api_opts)
            api_result = execute_action(api_action, api_text, parsed_opts)
            st.json({
                "action_executed": api_action,
                "result": api_result,
            })
        except json.JSONDecodeError:
            st.error("❌ صيغة JSON غير صالحة في الخيارات")
        except Exception as e:
            st.error(f"❌ {e}")

    st.markdown("**مثال `curl` مكافئ (FastAPI الأصلي):**")
    curl_body = json.dumps(
        {"action": action_name, "text": "نص تجريبي", "options": {}},
        ensure_ascii=False,
    )
    st.code(
        f'curl -X POST http://localhost:8000/api/v1/process \\\n'
        f'  -H "Content-Type: application/json" \\\n'
        f"  -d '{curl_body}'",
        language="bash",
    )


# ═══════════════════════════════════════════════════════════
#  10) قسم حالة النظام
# ═══════════════════════════════════════════════════════════
with st.expander("📦 حالة النظام والتبعيات"):
    import sys

    st.markdown(f"**Python:** `{sys.version}`")

    dep_col1, dep_col2 = st.columns(2)

    with dep_col1:
        st.markdown("**✅ مكتبات مثبّتة:**")
        for pkg in installed_packages:
            try:
                mod = __import__(pkg)
                ver = getattr(mod, "__version__", "—")
            except Exception:
                ver = "?"
            st.markdown(f"- `{pkg}` → v{ver}")

    with dep_col2:
        st.markdown("**❌ مكتبات مفقودة:**")
        if missing_packages:
            for pkg in missing_packages:
                st.markdown(f"- `{pkg}`")
        else:
            st.markdown("*لا شيء — كل شيء مثبّت* ✅")

    if missing_packages:
        st.markdown("---")
        st.markdown("**أمر التثبيت الشامل:**")
        st.code(
            "pip install " + " ".join(missing_packages),
            language="bash",
        )


# ── التذييل ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; opacity:0.5; font-size:0.85rem; padding: 1rem;">
    🛠️ <strong>أدوات Adawat</strong> — معالجة اللغة العربية الطبيعية<br>
    Streamlit Interface v0.2.0 — Built with ❤️
</div>
""", unsafe_allow_html=True)
