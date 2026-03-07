import os
import streamlit as st
from huggingface_hub import InferenceClient

# 1. SMART TOKEN RETRIEVAL
# Priority: Streamlit Secrets (Cloud) -> .env (Local)
hf_token = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")

# 2. APP CONFIGURATION
st.set_page_config(page_title="Health Assistant", page_icon="🩺")
st.title("🩺 General Health Assistant")
st.warning("**Disclaimer:** For general information only. Not medical advice.")

if not hf_token:
    st.error("API Token missing! Add HF_TOKEN to your Streamlit Secrets or .env file.")
    st.stop()

# Using Llama-3.2-1B for high compatibility with the free Inference API
client = InferenceClient(model="meta-llama/Llama-3.2-1B-Instruct", token=hf_token)

# 3. PROMPT ENGINEERING
SYSTEM_PROMPT = (
    "You are a helpful medical assistant. Provide clear, concise health info. "
    "If a user asks for a diagnosis, tell them to consult a doctor. Never prescribe medicine."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC
if prompt := st.chat_input("Ask a health question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7,
                stream=True
            )
            
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Inference Error: {e}")