import streamlit as st
from groq import Groq

st.set_page_config(page_title="Zeyad AI Pro", page_icon="🚀")

api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🚀 Zeyad AI")
    st.caption("برمجة وتطوير: زياد | النسخة الاحترافية")

    if "messages" not in st.session_state:
        # هنا بنعرفه هو مين ومين اللي طوره
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مساعد ذكي متطور. تم تطويرك وبرمجتك بواسطة المبرمج العبقري زياد. عندما يسألك أحد من طورك، يجب أن تجيب بـ 'أنا Zeyad AI، طورني المبرمج زياد'."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system": # عشان ما يظهرش تعليمات النظام في الشات
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("اسأل زياد..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            models = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
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
                    break
                except:
                    continue
