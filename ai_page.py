
import streamlit as st
from agent import ask_agent
from ai_engine import get_config

from chat_storage import (
    initialize_chat_storage,
    save_message,
    get_chat_history,
    clear_chat_history
)


def show_ai_page():

    initialize_chat_storage()

    st.title("🤖 AI Study Assistant")

    st.caption(
        "Your personal intelligent university planner"
    )

    st.info(
        "Ask me about your assignments, deadlines, "
        "class schedule and study plans."
    )

    st.caption(
        "Your question and saved student records "
        "are sent to Gemini for analysis."
    )

    st.warning(
        "Demo mode: Chat history is shared between "
        "visitors. Do not enter private information."
    )

    # Load saved chat history
    messages = get_chat_history()

    # Chat statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Saved Messages",
            len(messages)
        )

    with col2:
        st.metric(
            "Questions Asked",
            sum(
                m["role"] == "user"
                for m in messages
            )
        )

    # Clear conversation with confirmation
    confirm_clear = st.checkbox(
        "Confirm deletion of all chat history"
    )

    if st.button(
        "🗑️ Clear Chat",
        disabled=not confirm_clear
    ):
        clear_chat_history()
        st.rerun()

    st.divider()

    # Suggested questions
    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)

    selected_question = None

    with col1:

        if st.button(
            "📅 Plan my day",
            use_container_width=True
        ):
            selected_question = (
                "What should I study today?"
            )

        if st.button(
            "🔥 Urgent assignments",
            use_container_width=True
        ):
            selected_question = (
                "Which assignments should I finish first?"
            )

    with col2:

        if st.button(
            "🏫 Today's classes",
            use_container_width=True
        ):
            selected_question = (
                "What classes do I have today?"
            )

        if st.button(
            "📚 Study schedule",
            use_container_width=True
        ):
            selected_question = (
                "Help me create a three-hour study plan."
            )

    st.divider()

    # Display database chat history
    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Receive student question
    typed_question = st.chat_input(
        "Ask your AI assistant..."
    )

    question = typed_question or selected_question

    if question:

        # Save student question
        save_message("user", question)

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Analyzing your tasks and schedule..."
                ):

                    answer = ask_agent(question)

                # Save AI response permanently
                # in the current SQLite database
                save_message("assistant", answer)

            except Exception as e:

                print(
                    f"AI Assistant Error: {type(e).__name__}",
                    flush=True
                )

                error_message = (
                    "The AI assistant is temporarily "
                    "unavailable. Please try again."
                )

                save_message(
                    "assistant",
                    error_message
                )

        st.rerun()

    st.divider()

    st.caption(
        "Powered by Gemini AI | Model: "
        + get_config(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )
    )

    st.caption(
        "AI recommendations may contain errors. "
        "Always review your study plan."
    )
