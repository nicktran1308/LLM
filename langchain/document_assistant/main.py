# ------------------------------- Import Libraries -------------------------------
from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

# ------------------------------- Helper Function -------------------------------
def create_sources_string(source_urls: Set[str]) -> str:
    """
    Generate a formatted string of source URLs.
    """
    if not source_urls:
        return ""
    sources_list = sorted(list(source_urls))
    return "Sources:\n" + "\n".join(f"{i+1}. {source}" for i, source in enumerate(sources_list))

# ------------------------------- Streamlit UI -------------------------------
st.header("LangChain🦜🔗 Udemy Course- Helper Bot")

# Initialize session state for chat history if not present
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Capture user prompt
prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button("Submit")

# If prompt exists, get and display the response
if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )

        st.session_state.chat_history.append((prompt, generated_response["answer"]))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)

# Display the chat history in the streamlit UI
if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)

