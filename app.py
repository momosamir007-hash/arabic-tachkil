import streamlit as st
import json
from typing import Any

# ─────────────────────────────────────────────────────────
# إعداد الصفحة (يجب أن يكون أول أمر Streamlit)
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="أدوات — Adawat",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# CSS مخصص
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

    /* ─── Global RTL ─── */
    .main .block-container { direction: rtl; text-align: right; }

    /* ─── Arabic Font ─── */
    * { font-family: 'Tajawal', sans-serif !important; }

    /* ─── Header ─── */
    .app-header {
        background: linear-gradient(135deg, #D4A017 0%, #8B6914 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }
    .app-header h1 { margin: 0; font-size: 2.2rem; }
    .app-header p  { margin: 0.3rem 0 0; opacity: 0.9; font-size: 1rem; }

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

    /* ─── Category Card ─── */
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

    /* ─── Sidebar ─── */
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# تعريف الأدوات (يعكس COMMAND_TABLE من config.py)
# ─────────────────────────────────────────────────────────
TOOLS = {
    "🗣️ معالجة لغوية (NLP)": {
        "category_class": "cat-nlp",
        "tools": {
            "التشكيل التلقائي":        {"action": "TashkeelText",   "icon": "✏️",  "has_options": True},
            "اقتراح التشكيل":          {"action": "Tashkeel2",      "icon": "💡",  "has_options": True},
            "التجذيع الخفيف":          {"action": "LightStemmer",   "icon": "🌿",  "has_options": True},
            "وسم الكلمات (POS)":       {"action": "Wordtag",        "icon": "🏷️",  "has_options": False},
            "التقطيع (Chunking)":      {"action": "chunk",          "icon": "✂️",  "has_options": False},
            "الثنائيات (Bigrams)":     {"action": "bigrams",        "icon": "🔗",  "has_options": False},
            "الترتيب المعكوس (قافية)": {"action": "Inverse",        "icon": "🔄",  "has_options": False},
            "فصل اللغات":              {"action": "Language",        "icon": "🌐",  "has_options": False},
            "تحليل المشاعر":           {"action": "Sentiment",      "icon": "🎭",  "has_options": False},
            "تحديد اللهجة":            {"action": "Dialect",         "icon": "🗺️",  "has_options": False},
        }
    },
    "🔍 الاستخراج": {
        "category_class": "cat-extract",
        "tools": {
            "الأرقام إلى حروف":       {"action": "NumberToLetters", "icon": "🔢",  "has_options": False},
            "استخراج المرقّمات":       {"action": "extractNumbered", "icon": "📋", "has_options": False},
            "استخراج الأسماء":         {"action": "extractNamed",   "icon": "👤",  "has_options": False},
            "المتلازمات اللفظية":      {"action": "showCollocations","icon": "🤝", "has_options": False},
        }
    },
    "📄 التنسيق": {
        "category_class": "cat-format",
        "tools": {
            "تنسيق Itemize (LaTeX)":   {"action": "Itemize",        "icon": "📝",  "has_options": False},
            "تنسيق جدول (LaTeX)":      {"action": "Tabulize",       "icon": "📊",  "has_options": False},
            "تنسيق Tabbing (LaTeX)":   {"action": "Tabbing",        "icon": "📐",  "has_options": False},
            "CSV إلى جدول Python":     {"action": "CsvToData",      "icon": "🔄",  "has_options": False},
        }
    },
    "⚙️ التوليد": {
        "category_class": "cat-generate",
        "tools": {
            "توليد اللواصق":           {"action": "Affixate",       "icon": "🔧",  "has_options": False},
            "نص عشوائي":               {"action": "RandomText",     "icon": "🎲",  "has_options": False},
        }
    },
    "🔤 العمليات الأساسية": {
        "category_class": "cat-basic",
        "tools": {
            "إزالة التشكيل":           {"action": "StripHarakat",   "icon": "🧹",  "has_options": False},
            "تقطيع النص (Tokenize)":   {"action": "Tokenize",       "icon": "🔤",  "has_options": False},
        }
    },
    "🧠 التحليل المتقدم": {
        "category_class": "cat-advanced",
        "tools": {
            "تحليل Stanza":            {"action": "Stanza",         "icon": "🏗️",  "has_options": False},
            "Farasa NER":               {"action": "FarasaNER",      "icon": "🎯",  "has_options": False},
        }
    },
}


# ─────────────────────────────────────────────────────────
# محرّك التنفيذ: يطابق تماماً FastAPI endpoint
# ─────────────────────────────────────────────────────────
def execute_action(action_name: str, text: str, options: dict) -> Any:
    """تنفيذ الإجراء — نسخة طبق الأصل من /api/v1/process"""

    import pyarabic.araby as araby
    from adawat.extractors.numbers  import number_to_words, extract_numbered_phrases
    from adawat.extractors.entities import extract_named_entities, show_collocations
    from adawat.nlp.tashkeel        import tashkeel, tashkeel_suggest
    from adawat.nlp.stemming        import light_stemmer, full_stemmer
    from adawat.nlp.tagging         import (word_tagging, chunk_split,
                                            get_bigrams, inverse_rhyme_sort,
                                            segment_language)
    from adawat.formatters.latex     import itemize, tabulize, tabbing
    from adawat.formatters.data      import csv_to_python_table
    from adawat.generators.affixation import generate_affixes
    from adawat.generators.randtext  import random_text
    from adawat.nlp.sentiment        import get_sentiment
    from adawat.nlp.dialect          import identify_dialect
    from adawat.nlp.advanced_nlp     import stanza_analyze, farasa_ner

    lastmark = options.get("lastmark", True)

    dispatch = {
        "NumberToLetters":  lambda: number_to_words(text),
        "extractNumbered":  lambda: extract_numbered_phrases(text),
        "extractNamed":     lambda: extract_named_entities(text),
        "showCollocations": lambda: show_collocations(text),
        "TashkeelText":     lambda: tashkeel(text, lastmark),
        "Tashkeel2":        lambda: tashkeel_suggest(text, lastmark),
        "LightStemmer":     lambda: full_stemmer(text, lastmark),
        "Wordtag":          lambda: word_tagging(text),
        "chunk":            lambda: chunk_split(text),
        "bigrams":          lambda: get_bigrams(text),
        "Inverse":          lambda: inverse_rhyme_sort(text),
        "Language":         lambda: segment_language(text),
        "Itemize":          lambda: itemize(text),
        "Tabulize":         lambda: tabulize(text),
        "Tabbing":          lambda: tabbing(text),
        "CsvToData":        lambda: csv_to_python_table(text),
        "Affixate":         lambda: generate_affixes(text),
        "StripHarakat":     lambda: araby.strip_tashkeel(text),
        "Tokenize":         lambda: araby.tokenize(text),
        "RandomText":       lambda: random_text(),
        "Sentiment":        lambda: get_sentiment(text),
        "Dialect":          lambda: identify_dialect(text),
        "Stanza":           lambda: stanza_analyze(text),
        "FarasaNER":        lambda: farasa_ner(text),
    }

    handler = dispatch.get(action_name)
    if handler is None:
        raise ValueError(f"إجراء غير معروف: {action_name}")
    return handler()


# ─────────────────────────────────────────────────────────
# عرض النتيجة بذكاء
# ─────────────────────────────────────────────────────────
def render_result(result: Any, action_name: str):
    """عرض النتيجة بأنسب شكل حسب نوعها"""

    # ── قائمة (list) ──
    if isinstance(result, list):

        # قائمة من القواميس → جدول
        if result and isinstance(result[0], dict):
            import pandas as pd
            df = pd.DataFrame(result)
            st.dataframe(df, use_container_width=True)

        # قائمة من أزواج (tuples) → جدول بعمودين
        elif result and isinstance(result[0], (list, tuple)):
            import pandas as pd
            df = pd.DataFrame(result)
            st.dataframe(df, use_container_width=True)

        # قائمة بسيطة → شرائح (chips)
        else:
            cols = st.columns(min(len(result), 6)) if len(result) <= 30 else [st.container()]
            if len(result) <= 30:
                for i, item in enumerate(result):
                    with cols[i % min(len(result), 6)]:
                        st.code(str(item), language=None)
            else:
                st.markdown(
                    '<div class="result-box">' +
                    " ◈ ".join(str(x) for x in result) +
                    '</div>',
                    unsafe_allow_html=True,
                )

    # ── قاموس (dict) ──
    elif isinstance(result, dict):
        for key, val in result.items():
            st.markdown(f"**{key}:**")
            if isinstance(val, list):
                render_result(val, action_name)
            else:
                st.markdown(
                    f'<div class="result-box">{val}</div>',
                    unsafe_allow_html=True,
                )

    # ── نص (str) ──
    elif isinstance(result, str):
        # إذا كان النص يبدو كـ LaTeX أو كود
        if any(kw in action_name for kw in ("Itemize", "Tabulize", "Tabbing", "CsvToData")):
            st.code(result, language="latex")
        else:
            st.markdown(
                f'<div class="result-box">{result}</div>',
                unsafe_allow_html=True,
            )

    # ── أي نوع آخر ──
    else:
        st.json(result) if isinstance(result, (dict, list)) else st.write(result)


# ═══════════════════════════════════════════════════════════
#                     واجهة التطبيق
# ═══════════════════════════════════════════════════════════

# ── العنوان ──
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
    st.markdown("## 🛠️ اختيار الأداة")
    st.markdown("---")

    # اختيار الفئة
    category = st.selectbox(
        "📂 الفئة:",
        list(TOOLS.keys()),
        index=0,
    )

    cat_info = TOOLS[category]

    # اختيار الأداة
    tool_name = st.selectbox(
        "🔧 الأداة:",
        list(cat_info["tools"].keys()),
        index=0,
    )

    tool_info = cat_info["tools"][tool_name]
    action_name = tool_info["action"]

    st.markdown("---")

    # ── خيارات إضافية ──
    options = {}
    if tool_info.get("has_options"):
        st.markdown("### ⚙️ خيارات إضافية")
        options["lastmark"] = st.checkbox(
            "علامة آخر الكلمة (lastmark)",
            value=True,
            help="إضافة حركة آخر الكلمة عند التشكيل أو التجذيع",
        )

    st.markdown("---")
    st.markdown(
        f'<span class="category-badge {cat_info["category_class"]}">{category}</span>',
        unsafe_allow_html=True,
    )
    st.caption(f"الإجراء الداخلي: `{action_name}`")


# ──────────────────────────────
# المنطقة الرئيسية
# ──────────────────────────────
st.markdown(f"## {tool_info['icon']} {tool_name}")

# بعض الأدوات لا تحتاج نصاً (مثل RandomText)
needs_text = action_name != "RandomText"

text = ""
if needs_text:
    # ── نص نموذجي لكل أداة ──
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

    text = st.text_area(
        "📝 أدخل النص:",
        value=SAMPLE_TEXTS.get(action_name, "أدخل النص العربي هنا..."),
        height=160,
        key="main_input",
    )

# ── أزرار التنفيذ ──
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

with col_btn1:
    run_clicked = st.button(
        f"▶️  تنفيذ: {tool_name}",
        type="primary",
        use_container_width=True,
    )

with col_btn2:
    clear_clicked = st.button("🗑️ مسح", use_container_width=True)

with col_btn3:
    copy_mode = st.checkbox("📋 وضع النسخ", value=False)

if clear_clicked:
    st.rerun()


# ── التنفيذ وعرض النتائج ──
if run_clicked:
    if needs_text and not text.strip():
        st.warning("⚠️ الرجاء إدخال نص أولاً!")
    else:
        with st.spinner(f"⏳ جارٍ تنفيذ «{tool_name}»..."):
            try:
                result = execute_action(action_name, text, options)

                st.success(f"✅ تم تنفيذ «{tool_name}» بنجاح")

                # عرض النتائج
                st.markdown("### 📤 النتيجة:")

                if copy_mode:
                    # وضع النسخ: عرض كنص خام
                    raw = json.dumps(result, ensure_ascii=False, indent=2) \
                          if not isinstance(result, str) else result
                    st.code(raw, language="json" if not isinstance(result, str) else None)
                else:
                    render_result(result, action_name)

                # ── معلومات إضافية ──
                with st.expander("🔍 تفاصيل الاستجابة (Debug)"):
                    st.json({
                        "action_executed": action_name,
                        "input_length":   len(text),
                        "result_type":    type(result).__name__,
                        "result":         result,
                    })

            except Exception as e:
                st.error(f"❌ خطأ أثناء التنفيذ: {str(e)}")
                with st.expander("🐛 تفاصيل الخطأ"):
                    import traceback
                    st.code(traceback.format_exc())


# ═══════════════════════════════════════════════════════════
#                     وضع API (اختياري)
# ═══════════════════════════════════════════════════════════
st.markdown("---")

with st.expander("🔌 استدعاء API مباشر (للمطوّرين)"):
    st.markdown("يمكنك استخدام واجهة API كما في FastAPI الأصلية:")

    api_action = st.text_input("الإجراء (action):", value=action_name)
    api_text   = st.text_area("النص:", value=text if needs_text else "", height=80, key="api_text")
    api_opts   = st.text_input("الخيارات (JSON):", value="{}")

    if st.button("🚀 إرسال طلب API", use_container_width=True):
        try:
            parsed_opts = json.loads(api_opts)
            result = execute_action(api_action, api_text, parsed_opts)
            st.json({"action_executed": api_action, "result": result})
        except json.JSONDecodeError:
            st.error("❌ خيارات JSON غير صالحة")
        except Exception as e:
            st.error(f"❌ {e}")

    st.markdown("**مثال `curl` مكافئ (للـ FastAPI الأصلي):**")
    st.code(f'''curl -X POST http://localhost:8000/api/v1/process \\
  -H "Content-Type: application/json" \\
  -d '{{"action": "{action_name}", "text": "نص تجريبي", "options": {{}}}}'
''', language="bash")


# ── التذييل ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; opacity:0.6; font-size:0.85rem;">
    🛠️ <strong>أدوات Adawat</strong> — معالجة اللغة العربية الطبيعية<br>
    Streamlit Interface v0.2.0
</div>
""", unsafe_allow_html=True)
