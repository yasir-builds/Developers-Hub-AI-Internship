import os
import streamlit as st
from huggingface_hub import InferenceClient

# 1. LOAD LIBRARIES & TOKENS SAFELY
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Priority: Local .env -> Streamlit Secrets (Cloud)
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    try:
        hf_token = st.secrets["HF_TOKEN"]
    except (KeyError, FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        hf_token = None

# 2. UI CONFIGURATION
st.set_page_config(page_title="Health Assistant", page_icon="🩺")
st.title("🩺 General Health Assistant")
st.warning("**Disclaimer:** This AI provides general information and is not a substitute for professional medical advice.")

if not hf_token:
    st.error("Missing API Token! Ensure HF_TOKEN is in your .env (local) or Secrets (cloud).")
    st.stop()

# Using Llama-3.2-1B (Highly stable for free-tier conversational tasks)
client = InferenceClient(model="meta-llama/Llama-3.2-1B-Instruct", token=hf_token)

# 3. PROMPT ENGINEERING
SYSTEM_PROMPT = (
    "You are a helpful and friendly medical assistant. "
    "Provide clear, concise information about general health. "
    "Rule 1: If a user asks for a diagnosis or dosage, tell them to consult a doctor. "
    "Rule 2: Never give definitive medical prescriptions. "
    "Rule 3: Keep responses empathetic and informative."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. CHAT LOGIC (Error-Free Streaming)
if prompt := st.chat_input("How can I help you today?"):
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
            
            # Helper function to extract text and avoid 'index out of range' errors
            def stream_generator(response_stream):
                for chunk in response_stream:
                    # Safely check if the chunk contains valid content
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            yield content

            # Stream the response word-by-word
            full_response = st.write_stream(stream_generator(stream))
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Inference Error: {str(e)}")