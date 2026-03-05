 import streamlit as st
from groq import Groq

st.set_page_config(page_title="Zeyad AI - Chat & Image", page_icon="🎨")

api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🎨 Zeyad AI - المساعد الذكي")
    st.caption("تطوير: زياد | الآن يدعم صناعة الصور والدردشة")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مطورك هو زياد. أنت تستطيع الدردشة وصناعة الصور. إذا طلب منك المستخدم رسم صورة، أخبره أنك ستقوم بذلك."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("اسأل زيad أو اطلب منه رسم صورة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # لو المستخدم طلب "ارسم" أو "صورة"
            if "ارسم" in prompt or "صورة" in prompt or "draw" in prompt.lower():
                with st.spinner("جاري رسم صورتك يا بطل..."):
                    # هنا بنستخدم رابط خارجي لصناعة الصورة بناءً على وصفك
                    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed=42"
                    st.image(image_url, caption=f"الصورة التي طلبها زياد: {prompt}")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم صنع الصورة لـ: {prompt}"})
            else:
                # دردشة عادية
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages
                    )
                    res = response.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("المحرك مشغول، جرب تاني.")
