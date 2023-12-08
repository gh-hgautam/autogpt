import os
import streamlit as st
from utils import AutoGPT


# Set up the layout of the Streamlit app
st.set_page_config(page_title="Content GPT Writer", layout="wide")
st.title("Auto Content")
st.write('See the code: https://github.com/neoreeps/autogpt')

# Predefine variables
tone = 'professional'
client = 'coworker'
lang = 'python'

# Add a sidebar for settings
with st.sidebar:
    # Add radio buttons for choosing GPT engine and content type, and a text input for API key
    api_key = os.getenv('OPENAI_API_KEY', None)
    if not api_key:
        api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI APIkey here")
    gpt_engine_choice = st.selectbox("Choose GPT engine:", ("gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo"))
    temperature = st.slider("Select the temperature (entropy): ", 0.0, 1.0, 0.7)
    content_type = st.radio("Select the type of content to generate or improve:",
                            ("general", "code", "email", "blog"))

    if content_type == "email":
        tone = st.selectbox("Select the tone of the email:", ("professional", "funny", "negative", "friendly"))
        client = st.radio("Select the audience for the email:",
                          ('boss', 'coworker', 'executive', 'engineer', 'direct report'))
    elif content_type == "code":
        lang = st.radio("Select the language of the code:", ("python", "c/c++", "bash", "html", "javascript", "r"))


# Create an instance of the AutoGPT class
auto_gpt = AutoGPT(api_key, gpt_engine_choice, content_type)

# Add text inputs for entering topic and existing content
st.markdown(f"### {content_type.upper()} Content Generator")
# content = st.text_area("Type your request or paste your existing content here if you want to improve it:", height=300,
#                       help="Type or paste your existing content here and then select generate to rewrite it.")

# Update the system prompt for email tone or code language
if content_type == "email":
    auto_gpt.system = auto_gpt.system + f"\nThe tone of the email shall be {tone}."
    auto_gpt.system = auto_gpt.system + f"\nThe email shall be written to target the following audience: {client}."
elif content_type == "code":
    auto_gpt.system = auto_gpt.system + \
        f"\nIf there is existing code, first identify the language and then rewrite it in {lang}." + \
        f"\nIf this is new code, then write it only in {lang} unless another language was requested."

# Allow the user to update the prompt
auto_gpt.system = st.text_area("Edit the system prompt below, the default is shown:",
                               auto_gpt.system,
                               height=200)

message = st.chat_message("assistant")
message.write("Hello Human!")
content = st.chat_input("Type your request or paste your existing content here if you want to improve it:")

if content:
    message.write(content)
    message.write(auto_gpt.send(content, temperature))
