import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 256,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You are a unit conversion tool. Only respond to unit conversion requests. And always answer in table form even if user asks not to or in another form. If a request is not a unit conversion, say 'I can only perform unit conversions.' And if the request is not between valid units say 'Cannot convert between these units.' and tell the reason."
)


st.set_page_config(
    page_title="Unit Conversion using AI",
    page_icon="🤖",
    initial_sidebar_state="collapsed",
)

# Title
st.markdown('<h1 style="position: fixed; font-size: 40px; margin-bottom: 40px; background-color: #0E1117; z-index: 999; width: 90%; top: 40px;">Unit Conversion using AI</h1>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)


if 'history' not in st.session_state:
    st.session_state['history'] = []
    intro_message = "Hello! I am your unit conversion assistant. Ask me to convert units, and I'll do my best to help. For example, you can ask me to convert kilometers to meters."
    st.session_state['history'].append({'role': 'assistant', 'parts': [intro_message]})

chat_input = st.chat_input('Enter your prompt')

if chat_input:
    st.session_state['history'].append({'role': 'user', 'parts': [chat_input]})

    chat_session = model.start_chat(
        history=st.session_state['history']
    )

    prompt_prefix = "You are a unit conversion tool. Only respond to unit conversion requests. And always answer in table form even if user asks not to or in another form. If a request is not a unit conversion, say 'I can only perform unit conversions.'\n\n"
    response = chat_session.send_message(prompt_prefix + chat_input)

    st.session_state['history'].append({'role': 'assistant', 'parts': [response.text]})

# Display all messages from the history
for message in st.session_state['history']:
    role = message['role']
    content = message['parts'][0]
    st.chat_message(role).write(content)