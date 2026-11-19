
import streamlit as st


def apply_styles():

    st.markdown("""
    <style>

    /* Main website layout */
    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Modern typography */
    h1 {
        font-weight: 750 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        font-weight: 650 !important;
    }

    /* Dashboard metric cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 3px 12px
            rgba(15, 23, 42, 0.04);
    }

    /* Professional buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        min-height: 44px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        border-color: #4F46E5;
        color: #4F46E5;
    }

    /* Input fields */
    input, textarea {
        font-size: 16px !important;
    }

    /* AI chat messages */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 15px;
    }

    /* Dashboard welcome banner */
    .welcome-banner {
        background: linear-gradient(
            135deg,
            #4338CA,
            #6366F1
        );
        color: white;
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
    }

    .welcome-banner h2 {
        color: white;
        margin: 0;
        font-size: 27px;
    }

    .welcome-banner p {
        color: #E0E7FF;
        margin-top: 10px;
        margin-bottom: 0;
    }

    /* Mobile optimization */
    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 2rem;
        }

        h1 {
            font-size: 26px !important;
        }

        h2 {
            font-size: 21px !important;
        }

        .welcome-banner {
            padding: 20px;
            border-radius: 14px;
        }

        .welcome-banner h2 {
            font-size: 22px;
        }

        div[data-testid="stMetric"] {
            padding: 14px;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            width: 100%;
            min-height: 48px;
        }

        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }

        div[data-testid="stHorizontalBlock"]
        > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 0 !important;
            width: 100% !important;
        }

    }

    </style>
    """, unsafe_allow_html=True)


def show_welcome_banner():

    st.markdown("""
        <div class="welcome-banner">
            <h2>Make today productive.</h2>
            <p>
                Manage your assignments,
                organize your university schedule,
                and study smarter with AI.
            </p>
        </div>
    """, unsafe_allow_html=True)
