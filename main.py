import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Zeyad AI Diagnostics", page_icon="🔍")

# 🔑 المفتاح بتاعك
api_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

st.title("🔍 Zeyad AI - فاحص الأعطال")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = st.chat_input("اكتب أي حاجة هنا للتجربة...")
        
        if prompt:
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                try:
                    # محاولة الاتصال بجوجل
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    # المرة دي هيطبع لنا الغلط الحقيقي بدل كلمة "مشغول"
                    st.error(f"العطل الحقيقي هو: {str(e)}")
                    st.info("لو طلع لك 'API_KEY_INVALID'، يبقى المفتاح محتاج يتغير.")
                    st.info("لو طلع لك 'User location not supported'، يبقى لازم نغير السيرفر.")
                    
    except Exception as e:
        st.error(f"خطأ في الإعدادات: {e}")
