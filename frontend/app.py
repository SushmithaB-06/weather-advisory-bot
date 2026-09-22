import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# BACKEND IMPORT
# ============================================================

from backend.graph import weather_graph


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Weather Advisory Support Bot",
    page_icon="🌦️",
    layout="centered",
)


# ============================================================
# TITLE
# ============================================================

st.title("🌦️ Weather Advisory Support Bot")

st.caption(
    "Ask about outdoor activities and weather conditions."
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_location" not in st.session_state:
    st.session_state.previous_location = None

if "previous_activity" not in st.session_state:
    st.session_state.previous_activity = None


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_message = st.chat_input(
    "Ask a weather advisory question..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_message:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # --------------------------------------------------------
    # Run LangGraph
    # --------------------------------------------------------

    try:

        result = weather_graph.invoke(
            {
                "user_message": user_message,
                "previous_location":
                    st.session_state.previous_location,
                "previous_activity":
                    st.session_state.previous_activity,
            }
        )

        response = result.get(
            "response",
            "Unable to generate a response.",
        )

        # ----------------------------------------------------
        # Update session memory
        # ----------------------------------------------------

        if result.get("previous_location"):
            st.session_state.previous_location = (
                result.get("previous_location")
            )

        if result.get("previous_activity"):
            st.session_state.previous_activity = (
                result.get("previous_activity")
            )

    except Exception as exc:

        response = (
            "Unable to process your request.\n\n"
            f"Error: {exc}"
        )

    # --------------------------------------------------------
    # Display bot response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response)