import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Zeyad AI Pro", page_icon="🚀")

# المفتاح بتاعك
api_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if api_key:
    try:
        # إجبار المكتبة على استخدام النسخة المستقرة
        genai.configure(api_key=api_key)
        
        # استخدام اسم الموديل بدون أي إضافات
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🚀 Zeyad AI")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        uploaded_file = st.file_uploader("📸 ارفع صورة", type=["jpg", "png"])

        if prompt := st.chat_input("اسأل زياد..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # تعديل طريقة إرسال البيانات للموديل
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt, img])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # طباعة الخطأ التقني لو لسه موجود
                    st.error(f"عطل فني: {e}")
                        
    except Exception as e:
        st.error(f"خطأ إعدادات: {e}")
