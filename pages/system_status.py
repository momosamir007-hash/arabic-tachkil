# pages/system_status.py
import streamlit as st
from adawat.dependencies import get_status

st.set_page_config(page_title="حالة النظام", page_icon="⚙️")
st.title("⚙️ حالة النظام")

status = get_status()

# ─── المكتبات الأساسية ───
st.subheader("📦 المكتبات الأساسية")
for name, info in status.items():
    if info['required']:
        col1, col2, col3 = st.columns([1, 3, 2])
        col1.write(info['icon'])
        col2.write(f"**{name}**")
        col3.write(info['version'] or "غير مثبتة")

# ─── المكتبات الاختيارية ───
st.subheader("📦 المكتبات الاختيارية")
for name, info in status.items():
    if not info['required']:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        col1.write(info['icon'])
        col2.write(f"**{name}**")
        col3.write(info['version'] or "غير مثبتة")
        if not info['available']:
            col4.code(f"pip install {info['pip_name']}", language="bash")

# ─── الميزات المتأثرة ───
st.subheader("🔧 حالة الميزات")
features = {
    'تحليل المشاعر': ['transformers', 'torch'],
    'تحديد اللهجة': ['transformers', 'torch'],
    'التشكيل': ['mishkal', 'qalsadi'],
    'التحليل الصرفي': ['qalsadi', 'tashaphyne'],
    'التصنيف': ['naftawayh'],
}
for feature, deps in features.items():
    all_available = all(status.get(d, {}).get('available', False) for d in deps)
    icon = "✅" if all_available else "❌"
    missing = [d for d in deps if not status.get(d, {}).get('available', False)]
    if all_available:
        st.success(f"{icon} {feature}")
    else:
        st.error(f"{icon} {feature} — ينقص: {', '.join(missing)}")
