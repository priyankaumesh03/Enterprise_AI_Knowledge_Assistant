import streamlit as st
import sys
import time
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# IMPORT RAG PIPELINE AND QUERY CLASSIFIER
# --------------------------------------------------

from src.generation.generate_answer import generate_answer
from src.utils.query_classifier import classify_query


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff 0%,
        #f5f3ff 50%,
        #fdf2f8 100%
    );
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    color: #312e81;
    font-size: 32px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    color: #64748b;
    text-align: center;
    font-size: 16px;
    margin-bottom: 30px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #e0e7ff,
        #ede9fe
    );
}

[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #e0e7ff;
}

.stButton > button {
    border-radius: 10px;
    border: none;
    background-color: #6366f1;
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #4338ca;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INITIALIZE CHAT SESSION
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        "<h2 style='color:#4338ca;'>🤖 Enterprise Assistant</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 📚 Knowledge Categories")

    st.markdown("""
    <div style="
        background-color:white;
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        color:#334155;
    ">
        👥 <b>HR Policies</b><br>
        <small>Leave policies, employee guidelines and HR information.</small>
    </div>

    <div style="
        background-color:white;
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        color:#334155;
    ">
        💻 <b>IT Support</b><br>
        <small>Password reset, troubleshooting and technical support.</small>
    </div>

    <div style="
        background-color:white;
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        color:#334155;
    ">
        🏭 <b>Manufacturing Operations</b><br>
        <small>Production procedures, equipment and safety guidelines.</small>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.caption(
        "Powered by LangChain, ChromaDB and Google Gemini"
    )


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    "<div class='main-title'>Enterprise AI Knowledge Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Ask questions about HR policies, IT support, and manufacturing operations.</div>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if len(st.session_state.messages) == 0:

    st.html("""
    <div style="
        background: linear-gradient(135deg, #ffffff, #eef2ff);
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #c7d2fe;
        margin-bottom: 25px;
    ">

        <h2 style="
            color: #4338ca;
            margin-bottom: 15px;
        ">
            👋 Welcome!
        </h2>

        <p style="
            color: #475569;
            font-size: 16px;
        ">
            I'm your Enterprise AI Knowledge Assistant.
        </p>

        <p style="
            color: #475569;
            font-size: 16px;
        ">
            Ask me anything about HR policies, IT support,
            or manufacturing operations.
        </p>

        <h3 style="
            color: #6366f1;
            margin-top: 20px;
        ">
            How can I help you today?
        </h3>

    </div>
    """)


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                st.markdown("**📄 Source Documents:**")

                for source in sources:
                    st.caption(f"• {source}")

            response_time = message.get("response_time")

            if response_time is not None:

                st.caption(
                    f"⏱️ Response time: {response_time:.2f} seconds"
                )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_question = st.chat_input(
    "Ask a question about HR, IT support, or manufacturing..."
)


# --------------------------------------------------
# QUERY CLASSIFICATION AND ANSWER GENERATION
# --------------------------------------------------

if user_question:

    # Display user question

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate assistant response

    with st.chat_message("assistant"):

        with st.spinner("🤖 Preparing your response..."):

            try:

                start_time = time.time()

                # ------------------------------------------
                # STEP 1: CLASSIFY USER QUERY
                # ------------------------------------------

                intent = classify_query(user_question)

                # ------------------------------------------
                # STEP 2: HANDLE CASUAL CONVERSATIONS
                # ------------------------------------------

                if intent == "greeting":

                    answer = (
                        "Hello! 👋 Welcome to the Enterprise AI Knowledge "
                        "Assistant. How can I help you today?"
                    )

                    sources = []

                elif intent == "appreciation":

                    answer = (
                        "You're very welcome! 😊 Happy to help."
                    )

                    sources = []

                elif intent == "general_conversation":

                    answer = (
                        "I'm doing well, thank you! 😊 "
                        "I'm your Enterprise AI Knowledge Assistant. "
                        "I can help you with HR policies, IT support, "
                        "and manufacturing operations."
                    )

                    sources = []

                # ------------------------------------------
                # STEP 3: HANDLE KNOWLEDGE-BASED QUESTIONS
                # ------------------------------------------

                else:

                    answer, sources = generate_answer(user_question)

                # ------------------------------------------
                # STEP 4: CALCULATE RESPONSE TIME
                # ------------------------------------------

                response_time = time.time() - start_time

                # ------------------------------------------
                # STEP 5: DISPLAY ANSWER
                # ------------------------------------------

                st.markdown(answer)

                # Display source documents

                if sources:

                    st.markdown("**📄 Source Documents:**")

                    for source in sources:
                        st.caption(f"• {source}")

                # Display response time

                st.caption(
                    f"⏱️ Response time: {response_time:.2f} seconds"
                )

                # ------------------------------------------
                # STEP 6: SAVE ASSISTANT RESPONSE
                # ------------------------------------------

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "response_time": response_time
                })

            except Exception as e:

                error_message = (
                    "Sorry, something went wrong while generating "
                    "the response. Please try again."
                )

                st.error(error_message)

                print(f"Error generating answer: {e}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                    "response_time": None
                })