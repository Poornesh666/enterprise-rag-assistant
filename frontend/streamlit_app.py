import time
import requests
import streamlit as st

# ---------------------------------------------------------
# Backend Configuration
# ---------------------------------------------------------
API_URL = "http://127.0.0.1:8000"

# ---------------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Enterprise RAG Assistant")
st.caption(
    "Secure Retrieval-Augmented Generation powered by FastAPI, ChromaDB and Ollama."
)

# ---------------------------------------------------------
# Session State - Store user information
# ---------------------------------------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Backend Connection - Verify API availability
# ---------------------------------------------------------
def check_connection():

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    try:

        response = requests.get(
            f"{API_URL}/test",
            headers=headers,
            timeout=3,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


# =========================================================
# Login - Authenticate user and store JWT token
# =========================================================
if st.session_state.token is None:

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):

        with st.spinner("Authenticating user..."):

            try:

                response = requests.post(
                    f"{API_URL}/login",
                    data={
                        "username": username,
                        "password": password,
                    },
                    timeout=10,
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state.token = data["access_token"]
                    st.session_state.username = username
                    st.session_state.role = data["role"]

                    st.success("Login Successful!")

                    st.rerun()

                else:

                    st.error("Invalid username or password.")

            except requests.RequestException:

                st.error("Unable to connect to the backend.")


# =========================================================
# Chat Page - Display AI Assistant
# =========================================================
else:

    # -----------------------------------------------------
    # Sidebar - User information and actions
    # -----------------------------------------------------
    with st.sidebar:

        st.title("👤 User")

        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role}")

        st.divider()

        if check_connection():

            st.success("🟢 Backend Connected")

        else:

            st.error("🔴 Backend Offline")

        st.divider()

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):

            st.session_state.messages = []

            st.rerun()

        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):

            st.session_state.token = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.messages = []

            st.rerun()

    # -----------------------------------------------------
    # Welcome Message - Show once for new conversations
    # -----------------------------------------------------
    if len(st.session_state.messages) == 0:

        st.info(
            f"""
Welcome **{st.session_state.username}**!

You are logged in as **{st.session_state.role}**.

Try asking questions related to your department's documents.
"""
        )

    # -----------------------------------------------------
    # Chat History - Display previous conversation
    # -----------------------------------------------------
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # -----------------------------------------------------
    # Chat Input - Accept user query
    # -----------------------------------------------------
    question = st.chat_input("Ask a question...")

    if question:

        # Store User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }

        start_time = time.time()

        # -------------------------------------------------
        # Chat Request - Send query to FastAPI backend
        # -------------------------------------------------
        with st.spinner("🔍 Retrieving documents and generating response..."):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    headers=headers,
                    json={
                        "message": question,
                    },
                    timeout=120,
                )

                end_time = time.time()

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": result["response"],
                        }
                    )

                    st.session_state.response_time = (
                        end_time - start_time
                    )

                    st.rerun()

                else:

                    try:

                        detail = response.json()["detail"]

                    except Exception:

                        detail = "Unexpected server error."

                    st.error(f"❌ {detail}")

            except requests.RequestException:

                st.error("Unable to connect to the backend.")

    # -----------------------------------------------------
    # Response Time - Display latest response duration
    # -----------------------------------------------------
    if "response_time" in st.session_state:

        st.caption(
            f"⏱️ Response generated in {st.session_state.response_time:.2f} seconds"
        )


# ---------------------------------------------------------
# Footer - Project Information
# ---------------------------------------------------------
st.divider()

st.caption(
    "Enterprise RAG Assistant • FastAPI • SQLAlchemy • LangChain • ChromaDB • Ollama • Docker"
)