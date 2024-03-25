from typing import Set
from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="LangChain: Chat with Documents", page_icon="🦜")
st.title("LangChain🦜🔗 Basic Retrieval")


# Define CSS to style the chat bubbles and source list
css_style = """
<style>
    .stButton>button {
        height: 3em;
    }
    .streamlit-chat-message-container {
        overflow-wrap: break-word;
        word-break: break-word;
    }
    .source-container {
        max-height: 150px;
        overflow-y: auto;
        margin-top: 0.5em;
        border: 1px solid #e1e4e8;
        border-radius: 0.25em;
        padding: 0.5em;
    }
    .source-container a {
        color: white;
        text-decoration: underline;
        word-break: break-all;
        display: inline-block; /* This helps in wrapping the text if it overflows */
    }
</style>
"""

# Inject CSS with markdown at the beginning of your app
st.markdown(css_style, unsafe_allow_html=True)

def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = '<div class="source-container">\n'
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. <a href='{source}' target='_blank'>{source}</a><br>\n"
    sources_string += "</div>"
    return sources_string




# Initialize session state if not already done
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Setup the columns for the prompt and submit button
# Instead of defining separate columns, we integrate the prompt and submit button in one layout.
with st.form("prompt_form", clear_on_submit=True):  # We use a form for better alignment and interaction.
    prompt = st.text_input("Prompt", placeholder="Enter your message here...", key="prompt")
    submit = st.form_submit_button("Submit")  # We use a form submit button which aligns with the text input.

# When the submit button is pressed
if submit:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )

        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        
        # Format the response and sources
        formatted_response = generated_response['answer']
        sources_string = create_sources_string(sources)
        
        # Update the session state with the new information
        st.session_state["chat_history"].append((prompt, formatted_response))
        
        # Display the formatted response
        message(formatted_response)

        # Display the sources in an expander
        if sources_string:
            with st.expander("Show sources"):
                st.markdown(sources_string, unsafe_allow_html=True)

# Display chat history
for idx, (user_query, bot_response) in enumerate(st.session_state["chat_history"]):
    message(user_query, is_user=True, key=f"user_query_{idx}")
    message(bot_response, key=f"bot_response_{idx}")



