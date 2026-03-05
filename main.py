import streamlit as st
from groq import Groq
import random

# إعدادات الصفحة والواجهة
st.set_page_config(page_title="Zeyad AI Pro", page_icon="🎨")

# المفتاح السري (مباشر للراحة)
api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🎨 Zeyad AI - المساعد الذكي")
    st.caption("تطوير: المبرمج زياد | نسخة الشات والصور السريعة")

    # تعريف البوت بنفسه (تعليمات النظام)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مساعد ذكي ومطورك هو زياد. يمكنك الدردشة ورسم الصور الاحترافية."}
        ]

    # عرض الرسائل القديمة
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # منطقة الإدخال
    if prompt := st.chat_input("اسأل زياد أو اطلب رسمة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message
