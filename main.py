import streamlit as st
import google.generativeai as genai
import random
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Zeyad AI - Gemini Pro", page_icon="🚀")

# ⚠️ حط المفتاح بتاعك هنا بين العلامتين ""
gemini_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        # استخدمنا 1.5-flash عشان سريع جداً في تحليل الصور
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🚀 Zeyad AI")
        st.caption("النسخة المطورة | شات وتحليل صور")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الرسايل القديمة
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # زرار الرفع (فوق الشات)
        uploaded_file = st.file_uploader("📸 ارفع صورة هنا", type=["jpg", "jpeg", "png"])

        if prompt := st.chat_input("اسأل زياد..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # 1. حالة رسم صورة
                if any(word in prompt for word in ["ارسم", "صورة", "draw"]):
                    seed = random.randint(1, 99999)
                    img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}"
                    st.image(img_url, caption=f"رسمة زياد لـ: {prompt}")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
                
                # 2. حالة تحليل صورة بـ Gemini
                elif uploaded_file:
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt

