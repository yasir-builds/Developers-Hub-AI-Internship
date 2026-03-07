# Task 4: General Health Query Chatbot 🩺

An AI-powered conversational agent designed to provide general health information using **Prompt Engineering** and Large Language Models (LLMs). This project focuses on building a safe, friendly, and accessible medical assistant.

## 🚀 Live Demo
[Insert your Streamlit Cloud Link Here]

## 🎯 Objective
To create a chatbot that can answer general health-related questions (e.g., causes of symptoms, general safety of common medications) while maintaining strict safety boundaries to avoid providing harmful medical advice.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Interface:** Streamlit (Web-based UI)
* **LLM:** Mistral-7B-Instruct (via Hugging Face Inference API)
* **Deployment:** Streamlit Community Cloud

## ✨ Key Features
* **Medical Assistant Persona:** Purpose-built prompt to ensure a professional and empathetic tone.
* **Safety Filters:** Built-in disclaimers and logic to redirect users to professionals for diagnosis or prescriptions.
* **Real-time Interaction:** A clean, chat-like web interface for seamless user experience.
* **Zero-Cost Infrastructure:** Uses open-source models and free hosting tiers.

## 🧠 Prompt Engineering Approach
The chatbot is grounded using a system prompt that defines its identity:
> "Act like a helpful medical assistant. Provide clear, concise information. If a user asks for a diagnosis, tell them to consult a doctor. Never give definitive medical prescriptions."

## 📝 Example Queries
* *“What causes a sore throat?”*
* *“Is paracetamol safe for children?”*
* *“How can I improve my sleep hygiene?”*

## ⚙️ Setup & Installation
1. Clone the repository.
2. Navigate to the task folder:
   ```bash
   cd Task-4