import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Zeyad AI", page_icon="🚀")

# المفتاح بتاعك
api_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if api_key:
    try:
        genai.configure(api_key=api_key)
        # الأسماء دي هي اللي شغالة دلوقتي رسمي
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        st.title("🚀 Zeyad AI")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

        uploaded_file = st.file_uploader("📸 ارفع صورة", type=["jpg", "jpeg", "png"])

        if prompt := st.chat_input("اسأل زياد..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # الموديل ده بيقدر يشيل نص وصور مع بعض
                    if uploaded_file:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt, img])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"فيه مشكلة بسيطة: {e}")
                        
    except Exception as e:
        st.error("تأكد من إعدادات المفتاح")
