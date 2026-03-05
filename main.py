import streamlit as st
import google.generativeai as genai
import random
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Zeyad AI - Gemini Pro", page_icon="🚀")

# المفتاح الخاص بك
gemini_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🚀 Zeyad AI")
        st.caption("نسخة المبرمج زياد | شات وتحليل صور")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # زرار رفع الصور
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
                
                # 2. حالة تحليل صورة (تم قفل الأقواس هنا بدقة)
                elif uploaded_file:
                    try:
                        img = Image.open(uploaded_file)
                        response = model.generate_content([prompt, img])
                        res_text = response.text
                        st.markdown(res_text)
                        st.session_state.messages.append({"role": "assistant", "content": res_text})
                    except Exception as e:
                        st.error(f"مشكلة فنية: {e}")
                
                # 3. شات عادي
                else:
                    try:
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except:
                        st.error("المحرك مشغول حالياً، جرب تاني.")
                        
    except Exception as e:
        st.error("تأكد من صحة الـ API Key")
