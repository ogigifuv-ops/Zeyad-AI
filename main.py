import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Zeyad AI", page_icon="🚀")

# المفتاح بتاعك
api_key = "AIzaSyCn9CHItDoA-H3sdmWNmR_A1K3HGKw51c4"

if api_key:
    genai.configure(api_key=api_key)
    # الموديل ده هو اللي شغال دلوقتي في النسخة الجديدة
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.title("🚀 Zeyad AI")
    
    if prompt := st.chat_input("اكتب أهلاً للتجربة"):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"العطل لسه موجود: {e}")
