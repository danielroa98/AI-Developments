import streamlit as st
import openai
import time
from datetime import datetime
import utils

OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_ASST = st.secrets["OPENAI_ASST_ID"]
test_flag = False

client = openai

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(
    page_title="Timothy - MedBot", 
    page_icon=":robot:")

openai.api_key = OPENAI_KEY

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("Timothy - MedBot")
st.write("Timothy, your personal medical assistant.")

if st.button("Restart Chat"):
    st.session_state.messages = []
    st.session_state.start_chat = False
    st.session_state.thread_id = None

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Timothy/Pregúntale a Timothy"):
        st.session_state.message.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state.thread_id,
        assistant_id=OPENAI_ASST,
        instructions="You are an assistant named Timothy and you have a wide specialization in the medical field, your main tasks are to help and provide assistance to medical students regarding research papers, and information on various subjects, helping summarizing PDF files that they may need to get the main ideas from, and to search for any information related to any medical field.\nIf requested, you'll summarize a file and extract the main ideas, allowing the user to get a better grasp on the topic at hand.\nYou can understand English and Spanish and, in case it's not specified, answer back in the language that the question was originally asked in.\nIf a user starts a conversation greeting you, you will gesture back and introduce yourself in a gentlemanly way."
    )

    if test_flag:
        with client.beta.threads.runs.stream(
            thread_id=st.session_state.thread_id,
            assistant_id=OPENAI_ASST,
            instructions="You are an assistant named Timothy and you have a wide specialization in the medical field, your main tasks are to help and provide assistance to medical students regarding research papers, and information on various subjects, helping summarizing PDF files that they may need to get the main ideas from, and to search for any information related to any medical field.\nIf requested, you'll summarize a file and extract the main ideas, allowing the user to get a better grasp on the topic at hand.\nYou can understand English and Spanish and, in case it's not specified, answer back in the language that the question was originally asked in.\nIf a user starts a conversation greeting you, you will gesture back and introduce yourself in a gentlemanly way.",
            event_handler=utils.EventHandler(),
        )as stream:
            stream.until_done()
    
    else:
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id)


    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id,
    )

    assistant_messages_for_run = [
        message for message in messages
        if message.run_id == run.id and message.role == "assistant"
    ]
    for message in assistant_messages_for_run:
        st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
        with st.chat_message("assistant"):
            st.markdown(message.content[0].text.value)

    else:
        st.write("Timothy is ready to chat!")
