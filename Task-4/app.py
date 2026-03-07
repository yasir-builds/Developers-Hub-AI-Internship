import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv


# UI Config
st.set_page_config(page_title="General Health Assistant", page_icon="🩺")
st.title("🩺 General Health Query Chatbot")
st.markdown("---")

# Safety Disclaimer (Persistent)
st.warning("**Disclaimer:** This is an AI-based assistant for general information only. It does not provide medical advice. Consult a professional for health concerns.")

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)

# Prompt Engineering - The "System" Persona
SYSTEM_PROMPT = (
    "You are a helpful and friendly medical assistant. "
    "Provide clear, concise information about general health. "
    "Rule 1: If a user asks for a diagnosis or specific dosage, tell them to consult a doctor. "
    "Rule 2: Never give definitive medical prescriptions. "
    "Rule 3: Keep responses empathetic and informative."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Combine system prompt with user query for better context
        full_prompt = f"<s>[INST] {SYSTEM_PROMPT} \nUser Query: {prompt} [/INST]</s>"
        
        response = client.text_generation(full_prompt, max_new_tokens=500, temperature=0.7)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})