from openai import OpenAI
import streamlit as st


openai_base_url = st.secrets["openai_base_url"] 
openai_api_key = st.secrets["openai_api_key"] 
openai_model = st.secrets["openai_model"] 
 

st.title("💬 Chatbot")

with st.sidebar:
    pass_code = st.text_input("Pass Code", key="pass_code", type="password")

if not pass_code:
    st.info("Please add your pass code to continue.")
    st.stop()

if pass_code != st.secrets["pass_code"]:
    st.info("Incorrect pass code.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():


    client = OpenAI(base_url=openai_base_url, api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model=openai_model, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
