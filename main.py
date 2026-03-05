import streamlit as st
import google.generativeai as genai
import random
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Zeyad AI - Gemini", page_icon="🚀")

# المفتاح اللي أنت بعته يا بطل
gemini_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if gemini_key:
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.title("🚀 Zeyad AI - المساعد الذكي")
        st.caption("تطوير: المبرمج زياد | مدعوم بمحرك Google Gemini")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # عرض الشات القديم
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # زرار الرفع فوق الشات مباشرة
        uploaded_file = st.file_uploader("📸 ارفع صورة لزياد يحللها", type=["jpg", "jpeg", "png"])

        if prompt := st.chat_input("اسأل زياد عن صورة أو دردش معه..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # 1. لو طلب رسم صورة
                if any(word in prompt for word in ["ارسم", "صورة", "draw"]):
                    with st.spinner("زياد بيرسم..."):
                        seed = random.randint(1, 99999)
                        img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}"
                        st.markdown(f"![Zeyad Art]({img_url})")
                        st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
                
                # 2. تحليل صورة باستخدام Gemini
                elif uploaded_file:
                    with st.spinner("زياد يشوف الصورة..."):
                        try:
                            img = Image.open(uploaded_file)
                            response = model.generate_content([prompt, img])
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except:
                            st.error("مشكلة في تحليل الصورة.")
                
                # 3. دردشة عادية
                else:
                    try:
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except:
                        st.error("المحرك مشغول حالياً.")
    except Exception as e:
        st.error("فيه مشكلة في مفتاح الـ API.")
