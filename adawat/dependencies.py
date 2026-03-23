# adawat/dependencies.py
"""إدارة التبعيات الاختيارية"""
import importlib
import sys


def check_dependency(module_name, pip_name=None):
    """
    التحقق من توفر مكتبة
    Args:
        module_name: اسم الاستيراد
        pip_name: اسم التثبيت (إذا مختلف)
    Returns:
        tuple: (متوفرة, الوحدة أو None)
    """
    try:
        module = importlib.import_module(module_name)
        return True, module
    except ImportError:
        return False, None


def get_status():
    """عرض حالة جميع التبعيات"""
    deps = {
        # ─── أساسية ───
        'pyarabic': {'pip': 'pyarabic', 'required': True},
        'mishkal': {'pip': 'mishkal', 'required': True},
        'qalsadi': {'pip': 'qalsadi', 'required': True},
        'naftawayh': {'pip': 'naftawayh', 'required': True},
        'tashaphyne': {'pip': 'tashaphyne', 'required': True},
        'asmai': {'pip': 'asmai', 'required': True},
        'sylajone': {'pip': 'sylajone', 'required': True},
        'maskouk': {'pip': 'maskouk-pysqlite', 'required': True},
        'streamlit': {'pip': 'streamlit', 'required': True},
        # ─── اختيارية ───
        'torch': {'pip': 'torch', 'required': False},
        'transformers': {'pip': 'transformers', 'required': False},
        'camel_tools': {'pip': 'camel-tools', 'required': False},
        'stanza': {'pip': 'stanza', 'required': False},
        'farasapy': {'pip': 'farasapy', 'required': False},
    }

    status = {}
    for module_name, info in deps.items():
        available, module = check_dependency(module_name)
        version = getattr(module, '__version__', 'unknown') if available else None
        status[module_name] = {
            'available': available,
            'version': version,
            'pip_name': info['pip'],
            'required': info['required'],
            'icon': '✅' if available else ('❌' if info['required'] else '⚠️')
        }
    return status


def print_status():
    """طباعة حالة التبعيات"""
    status = get_status()
    print(f"\nPython {sys.version}")
    print("=" * 50)
    print("\n📦 المكتبات الأساسية:")
    for name, info in status.items():
        if info['required']:
            ver = info['version'] or 'غير مثبتة'
            print(f" {info['icon']} {name}: {ver}")
    print("\n📦 المكتبات الاختيارية:")
    for name, info in status.items():
        if not info['required']:
            ver = info['version'] or 'غير مثبتة'
            print(f" {info['icon']} {name}: {ver}")


# ============================================
# دوال مساعدة للميزات الاختيارية
# ============================================
def require(module_name, feature_name="هذه الميزة"):
    """
    التحقق من توفر مكتبة قبل استخدام ميزة
    Usage:
        module = require('torch', 'تحليل المشاعر')
    """
    available, module = check_dependency(module_name)
    if not available:
        raise ImportError(
            f"⚠️ {feature_name} تحتاج مكتبة '{module_name}'\n"
            f" ثبتها بالأمر: pip install {module_name}"
        )
    return module
