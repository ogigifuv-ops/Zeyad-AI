 import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(page_title="Zeyad AI - Chat & Image", page_icon="🎨")

# المفتاح السري
api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🎨 Zeyad AI - المساعد الذكي")
    st.caption("تطوير: زياد | النسخة الاحترافية (دردشة وصور)")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مطورك هو المبرمج العبقري زياد. أنت تستطيع الدردشة وصناعة الصور."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("اسأل زياد أو اطلب منه رسم صورة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if any(word in prompt for word in ["ارسم", "صورة", "draw"]):
                with st.spinner("جاري الرسم..."):
                    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42"
                    st.image(image_url, caption=f"رسمة لزياد: {prompt}")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
            else:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("فيه ضغط حالياً، جرب كمان شوية.")
