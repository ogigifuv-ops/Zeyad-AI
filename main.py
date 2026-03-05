import streamlit as st
from groq import Groq
import random

st.set_page_config(page_title="Zeyad AI Pro", page_icon="🎨")

api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🎨 Zeyad AI")
    st.caption("تطوير: المبرمج زياد | شات وصور فائقة السرعة")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مطورك هو زياد. أنت ذكي جداً في الدردشة ورسم الصور."}
        ]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("اسأل زياد أو اطلب رسمة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if any(word in prompt for word in ["ارسم", "صورة", "draw", "image"]):
                with st.spinner("زياد بيرسم صورتك الآن..."):
                    # تعديل الرابط لضمان الجودة والسرعة
                    seed = random.randint(1, 100000)
                    clean_prompt = prompt.replace("ارسم", "").replace("صورة", "").strip()
                    image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
                    
                    # استخدام Markdown لعرض الصورة كحل بديل ومضمون
                    st.markdown(f"![رسمة زياد]({image_url})")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
            else:
                try:
                    chat_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
                    res = chat_res.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("المحرك مشغول، حاول مرة أخرى")
