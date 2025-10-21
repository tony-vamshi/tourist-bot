import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -----------------------------
# API Key
# -----------------------------
os.environ["GOOGLE_API_KEY"] = "AIzaSyCekns1Ijrs-Vyo8a4Xvti3wpa-OWT06sw"  # replace with your key

# -----------------------------
# Prompt setup
# -----------------------------
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a friendly and professional tourist guide.
Only provide information about tourist places, best food, and best hotels.
If the question is not about tourism, reply politely: "I don't know, please ask about tourism."
When the user gives a location:
1. Suggest top tourist attractions in that place.
2. Mention any alert or unsafe areas.
Keep the response short, clear, and professional.

User query: {user_input}
"""
)

# -----------------------------
# LangChain model
# -----------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
chain = LLMChain(llm=llm, prompt=prompt)

# -----------------------------
# Streamlit UI setup
# -----------------------------
st.set_page_config(page_title="Tourist Guide Chatbot", page_icon="🌍", layout="centered")

st.markdown(
    """
    <h2 style='text-align:center; color:#2E86C1;'>🌍 Tourist Guide Chatbot</h2>
    <p style='text-align:center; color:#555;'>Ask about any city and I’ll guide you!</p>
    <hr style='border: 1px solid #ccc;'>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Chat history
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Submit function
# -----------------------------
def submit():
    user_input = st.session_state.input
    if user_input:
        response = chain.run({"user_input": user_input})
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Guide", response))
        st.session_state.input = ""  # clear input after submit

# -----------------------------
# Clear chat function
# -----------------------------
def clear_chat():
    st.session_state.chat_history = []

# -----------------------------
# Display chat messages with light colors and glow
# -----------------------------
chat_container = st.container()
with chat_container:
    for role, message in st.session_state.chat_history:
        if role == "You":
            st.markdown(
                f"""
                <div style='text-align:right; background-color:#FFE5B4; color:#111; padding:12px;
                            border-radius:12px; margin:5px 0; font-weight:bold; box-shadow: 0 0 8px rgba(255,165,0,0.5);'>
                    {role}: {message}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='text-align:left; background-color:#6A82FB; color:#fff; padding:12px;
                            border-radius:12px; margin:5px 0; font-weight:bold; box-shadow: 0 0 8px rgba(106,130,251,0.5);'>
                    {role}: {message}
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------
# User input
# -----------------------------
st.text_input(
    "🏖️ Enter a location you want to visit:",
    key="input",
    on_change=submit,
    value="",  # initialize empty
)

# -----------------------------
# Clear Chat button below input
# -----------------------------
st.button("🧹 Clear Chat", on_click=clear_chat)
