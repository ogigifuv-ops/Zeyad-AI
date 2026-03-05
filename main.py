import streamlit as st
from groq import Groq
import random
import base64
from PIL import Image
import io

st.set_page_config(page_title="Zeyad AI - Vision", page_icon="👁️")

api_key = "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"

if api_key:
    client = Groq(api_key=api_key)
    st.title("👁️ Zeyad AI")
    st.caption("تطوير: زياد | نسخة الشات والصور والتحليل")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "أنت Zeyad AI، مطورك هو زياد. يمكنك تحليل الصور ورسمها."}]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # زرار الرفع في قلب الصفحة
    uploaded_file = st.file_uploader("📸 ارفع صورة لزياد هنا", type=["jpg", "jpeg", "png"])
    
    if prompt := st.chat_input("اسأل زياد عن الصورة أو دردش معه..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            if uploaded_file:
                try:
                    with st.spinner("زياد يحلل الصورة..."):
                        # معالجة الصورة لضمان توافقها
                        img = Image.open(uploaded_file)
                        buffered = io.BytesIO()
                        img.save(buffered, format="JPEG")
                        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                        
                        response = client.chat.completions.create(
                            model="llama-3.2-11b-vision-preview",
                            messages=[{
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }]
                        )
                        res = response.choices[0].message.content
                        st.markdown(res)
                        st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    st.error(f"عذراً يا زياد، فيه مشكلة في الصورة دي. جرب صورة تانية.")
            else:
                if any(word in prompt for word in ["ارسم", "صورة", "draw"]):
                    seed = random.randint(1, 100000)
                    img_url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={seed}"
                    st.markdown(f"![رسمة زياد]({img_url})")
                    st.session_state.messages.append({"role": "assistant", "content": f"تم رسم: {prompt}"})
                else:
                    chat_res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
                    res = chat_res.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
