import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun

openai_base_url = st.secrets["openai_base_url"] 
openai_api_key = st.secrets["openai_api_key"] 
openai_model = st.secrets["openai_model"] 


st.title("🔎 Chat with search")


"""
You will have wings of a chatbot that can search the web.

"""

with st.sidebar:
    pass_code = st.text_input("Pass Code", key="pass_code", type="password")

if not pass_code:
    st.info("Please add your pass code to continue.")
    st.stop()

if pass_code != st.secrets["pass_code"]:
    st.info("Incorrect pass code.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your api key to continue.")
        st.stop()

    if not openai_base_url:
        st.info("Please add your Base Url to continue.")
        st.stop()

    if not openai_model:
        st.info("Please add your model to continue.")
        st.stop()

    llm = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, base_url=openai_base_url, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
