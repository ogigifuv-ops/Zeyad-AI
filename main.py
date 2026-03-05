import streamlit as st
from groq import Groq
import random

# إعدادات الصفحة والواجهة
st.set_page_config(page_title="Zeyad AI Pro", page_icon="🎨")

# المفتاح السري (مباشر للراحة)
api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("🎨 Zeyad AI - المساعد الذكي")
    st.caption("تطوير: المبرمج زياد | نسخة الشات والصور السريعة")

    # تعريف البوت بنفسه (تعليمات النظام)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "أنت Zeyad AI، مساعد ذكي ومطورك هو زياد. يمكنك الدردشة ورسم الصور الاحترافية."}
        ]

    # عرض الرسائل القديمة
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # منطقة الإدخال
    if prompt := st.chat_input("اسأل زياد أو اطلب رسمة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # ميزة صناعة الصور
            if any(word in prompt for word in ["ارسم", "صورة", "draw", "image"]):
                with st.spinner("زياد بيجهز لك الرسمة..."):
                    seed = random.randint(1, 99999) # لضمان عدم تعليق الصورة
                    image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}"
                    st.image(image_url, caption=f"إهداء من زياد: {prompt}")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
            else:
                # ميزة الدردشة
                try:
                    chat_res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.messages
                    )
                    res = chat_res.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.error("المحرك مشغول، جرب تاني يا بطل.")
