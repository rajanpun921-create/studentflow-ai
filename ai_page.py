
import streamlit as st
from agent import ask_agent
import os


def show_ai_page():

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
        "are sent to Gemini for analysis. "
        "Use sample data during testing."
    )

    # Initialize chat history
    if "ai_messages" not in st.session_state:

        st.session_state.ai_messages = []

    # Clear conversation
    if st.button("🗑️ Clear Chat"):

        st.session_state.ai_messages = []
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

    # Display conversation history
    for message in st.session_state.ai_messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Receive student question
    typed_question = st.chat_input(
        "Ask your AI assistant..."
    )

    question = typed_question or selected_question

    # Process student question
    if question:

        st.session_state.ai_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Analyzing your tasks and schedule..."
                ):

                    answer = ask_agent(question)

                st.markdown(answer)

                st.session_state.ai_messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception:

                error_message = (
                    "The AI assistant is temporarily "
                    "unavailable. Please try again."
                )

                st.error(error_message)

                st.session_state.ai_messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )

    st.divider()

    st.caption(
        "Powered by Gemini AI | "
        "Model: " + os.getenv("GEMINI_MODEL", "Gemini")
    )

    st.caption(
        "AI recommendations may contain errors. "
        "Always review your study plan."
    )
