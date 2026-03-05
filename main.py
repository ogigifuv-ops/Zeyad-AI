import streamlit as st
from groq import Groq

# إعدادات واجهة زياد الاحترافية
st.set_page_config(page_title="Zeyad AI Pro", page_icon="🚀")

# المفتاح بتاعك ثابت جوه الكود عشان الراحة
api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🚀 Zeyad AI - النسخة المستقرة")
    st.caption("هذه النسخة مبرمجة لتعمل بأقصى طاقة ممكنة دون توقف")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("اسأل زياد..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # ميزة الطوارئ: لو موديل وقف، التاني يشتغل
            models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "llama3-8b-8192"]
            success = False
            for model_name in models:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    success = True
                    break # لو نجح يخرج من المحاولة
                except:
                    continue # لو فشل يجرب الموديل اللي بعده
            
            if not success:
                st.error("للأسف جميع المحركات مضغوطة حالياً، جرب كمان 5 دقائق.")
