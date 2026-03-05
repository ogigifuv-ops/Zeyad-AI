import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة واللمسات الجمالية
st.set_page_config(page_title="Zeyad AI", page_icon="⚡", layout="centered")

# CSS لتحسين الشكل وإخفاء الرسائل التنبيهية
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%); color: white; }
    .stButton>button { border-radius: 12px; background-color: #4facfe; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. الهيدر (العنوان)
st.title("⚡ Zeyad AI - المساعد الذكي")
st.caption("برمجة وتطوير: زياد | مدعوم بأقوى محرك ذكاء اصطناعي")

# 3. التحقق من المفتاح السري تلقائياً
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    # لو المفتاح مش موجود في Secrets هيطلبه من الجنب
    api_key = st.sidebar.text_input("🔑 Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل السابقة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # صندوق الدردشة
    if prompt := st.chat_input("اسأل Zeyad AI أي شيء..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("حدث خطأ في الاتصال، تأكد من صحة الـ API Key")
else:
    st.warning("⚠️ برجاء إضافة الـ API Key في إعدادات Secrets لتشغيل الموقع تلقائياً.")

# أزرار سريعة
st.sidebar.title("🛠️ أدوات سريعة")
if st.sidebar.button("✨ تنظيف المحادثة"):
    st.session_state.messages = []
    st.rerun()
