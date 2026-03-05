import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Zeyad AI", page_icon="🚀")

# المفتاح اللي شغال معاك
api_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if api_key:
    try:
        genai.configure(api_key=api_key)
        # تم تعديل الاسم لـ 'gemini-pro' عشان يشتغل فوراً
        model = genai.GenerativeModel('gemini-pro')
        # للموديل اللي بيشوف الصور
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        
        st.title("🚀 Zeyad AI - المساعد الذكي")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        uploaded_file = st.file_uploader("📸 ارفع صورة يحللها زياد", type=["jpg", "jpeg", "png"])

        if prompt := st.chat_input("اسأل زياد..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = vision_model.generate_content([prompt, img])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"فيه مشكلة بسيطة: {e}")
                        
    except Exception as e:
        st.error("تأكد من إعدادات المفتاح")
