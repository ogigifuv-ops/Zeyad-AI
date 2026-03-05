import streamlit as st
import requests
import io
from PIL import Image
from groq import Groq

# 1. إعدادات الصفحة واللمسات الجمالية
st.set_page_config(page_title="Zeyad AI v2.0", page_icon="🚀", layout="wide")

# CSS مخصص لتحسين الشكل (أزرار وحركات)
st.markdown("""
    <style>
    /* تغيير لون الخلفية العام */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    
    /* تجميل أزرار القائمة الجانبية */
    .stButton>button {
        border-radius: 12px;
        transition: all 0.3s ease;
        background-color: #4facfe;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background-color: #00f2fe;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.4);
    }
    
    /* شكل فقاعات الشات */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)
# 2. الهيدر (العنوان)
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80) # أيقونة ذكاء اصطناعي
with col2:
    st.title("⚡ Zeyad AI - المساعد الذكي")
    st.caption("برمجة وتطوير: زياد | مدعوم بأقوى محرك ذكاء اصطناعي في العالم")

# 3. القائمة الجانبية (الأدوات)
with st.sidebar:
    st.markdown("### 🟢 الحالة: متصل")
    st.markdown("---")
    api_key = st.text_input("🔑 Groq API Key:", type="password", placeholder="ضع مفتاحك هنا...")
    
    st.subheader("🛠️ أدوات سريعة")
    if st.button("✨ تنظيف المحادثة"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("💡 **نصيحة زياد:** اطلب منه يرسم لك صورة بكتابة كلمة 'ارسم' في البداية.")

# 4. الأزرار السريعة (Quick Prompts)
st.write("---")
cols = st.columns(3)
with cols[0]:
    if st.button("🎭 احكيلي نكتة"):
        prompt_input = "احكيلي نكتة مصرية مضحكة"
with cols[1]:
    if st.button("📝 لخص لي نص"):
        prompt_input = "لخص لي هذا النص بأسلوب بسيط:"
with cols[2]:
    if st.button("💻 ساعدني في برمجة"):
        prompt_input = "عندي مشكلة في الكود، ممكن تساعدني؟"

# 5. نظام الذاكرة ومعالجة الصور
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message:
            st.image(message["image"], use_column_width=True)
        st.markdown(message["content"])

# 6. معالجة الإدخال
user_input = st.chat_input("اكتب سؤالك لـ Zeyad AI هنا...")
# لو داس على زرار من الأزرار السريعة
final_prompt = prompt_input if 'prompt_input' in locals() else user_input

if final_prompt:
    if not api_key:
        st.warning("⚠️ يرجى إدخال API Key في القائمة الجانبية للبدء.")
    else:
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        with st.chat_message("user"):
            st.markdown(final_prompt)

        # هل هو طلب صورة؟
        if any(word in final_prompt.lower() for word in ["ارسم", "صورة", "image", "draw"]):
            with st.chat_message("assistant"):
                with st.spinner("🎨 زياد يقوم بالرسم الآن..."):
                    # API الرسم المجاني
                    IMG_API = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
                    headers = {"Authorization": "Bearer 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"}
                    res = requests.post(IMG_API, headers=headers, json={"inputs": final_prompt})
                    if res.status_code == 200:
                        img = Image.open(io.BytesIO(res.content))
                        st.image(img, caption="من صنع Zeyad AI")
                        st.session_state.messages.append({"role": "assistant", "content": "تفضل الصورة!", "image": img})
                    else:
                        st.error("السيرفر مشغول حالياً، جرب تطلب الصورة كمان دقيقة.")
        
        # دردشة عادية
        else:
            try:
                client = Groq(api_key=api_key)
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    full_response = ""
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if "image" not in m],
                        stream=True
                    )
                    for chunk in completion:
                        full_response += (chunk.choices[0].delta.content or "")
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"خطأ: {e}")
