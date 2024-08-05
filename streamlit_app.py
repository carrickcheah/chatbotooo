import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (access api via .env)
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Inject custom CSS
st.markdown(
    """
    <style>
    .title {
        font-size: 3em;
    }
    .description {
        font-size: 1.9em;
    }
    .chat-message {
        font-size: 1.5em; /* Adjust this value to change the font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Show title and description.
st.markdown("<h1 class='title'>💬 Bella Blouses</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='description'>"
    "This is a simple chatbot that uses OpenAI's GPT-4o-mini model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get "
    "<a href='https://platform.openai.com/account/api-keys'>here</a>. "
    "You can also learn how to build this app step by step by "
    "<a href='https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps'>following our tutorial</a>."
    "</p>",
    unsafe_allow_html=True
)

if not openai_api_key:
    st.info("Please add your OpenAI API key to the .env file to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='chat-message'>{message['content']}</div>", unsafe_allow_html=True)

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-message'>{prompt}</div>", unsafe_allow_html=True)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
