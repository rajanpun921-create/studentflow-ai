
import streamlit as st


def apply_styles():

    apply_dashboard_styles()

    st.markdown("""
    <style>

    /* Main website layout */

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Typography */

    h1 {
        font-weight: 750 !important;
        letter-spacing: -1px;
    }

    h2, h3 {
        font-weight: 650 !important;
    }

    /* Metric cards */

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 3px 12px
            rgba(15, 23, 42, 0.04);
    }

    /* Buttons */

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

    /* Welcome banner */

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


def apply_dashboard_styles():

    st.markdown("""
    <style>

    /* =========================
       SIDEBAR NAVIGATION
       ========================= */

    section[data-testid="stSidebar"] {
        background: #2359d8 !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarContent"] {
        padding-top: .35rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"]
    .university-link {
        color: #e0edff !important;
    }

    section[data-testid="stSidebar"]
    .university-link:hover {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"]
    [role="radiogroup"] label {
        padding: .65rem;
        border-radius: 9px;
        margin: 2px 0;
    }

    section[data-testid="stSidebar"]
    [role="radiogroup"] label:hover,

    section[data-testid="stSidebar"]
    [role="radiogroup"] label:has(input:checked) {
        background: rgba(255,255,255,.18);
    }

    section[data-testid="stSidebar"]
    [data-testid="stAlert"] p {
        color: #14532d !important;
    }

    section[data-testid="stSidebar"] button {
        color: #ffffff;
    }


    /* =========================
       DASHBOARD LAYOUT
       ========================= */

    .sf-dashboard,
    .sf-dashboard * {
        box-sizing: border-box;
    }

    .sf-dashboard {
        color: #14213b;
        font-family: inherit;
        font-size: 14px;
    }

    .sf-grid {
        display: grid;
        grid-template-columns:
            minmax(0,1.65fr) minmax(0,1fr);
        gap: 18px;
        align-items: start;
    }

    .sf-stack {
        display: flex;
        flex-direction: column;
        gap: 18px;
        min-width: 0;
    }

    .sf-card {
        background: white;
        border: 1px solid #e5eaf3;
        border-radius: 18px;
        padding: 20px;
        box-shadow:
            0 4px 16px rgba(35,58,105,.045);
        min-width: 0;
    }


    /* =========================
       DARK WELCOME BANNER
       ========================= */

    .sf-hero {
        min-height: 192px;
        border-radius: 18px;
        padding: 26px;
        color: white;
        display: flex;
        gap: 18px;
        align-items: center;
        justify-content: space-between;

        background:
            radial-gradient(
                ellipse at 100% 0%,
                #234797 0%,
                transparent 52%
            ),

            linear-gradient(
                135deg,
                #111a36,
                #101c40 70%,
                #172d61
            );

        overflow: hidden;
    }

    .sf-dashboard .sf-hero h2 {
        color: white;
        font-size: clamp(23px,2.4vw,32px);
        line-height: 1.15;
        margin: 9px 0;
        padding: 0;
        letter-spacing: -.6px;
    }

    .sf-hero h2 span {
        color: #8bbaff;
    }

    .sf-hero p {
        color: #cbd9f5;
        margin: 0 0 14px;
        font-size: 14px;
        line-height: 1.5;
    }

    .sf-eyebrow {
        font-size: 10px;
        font-weight: 750;
        color: #a8c8ff;
        letter-spacing: 1.6px;
    }

    .sf-hero-note {
        display: inline-block;
        padding: 7px 11px;
        background: #275ad1;
        border-radius: 20px;
        font-size: 12px;
        color: white;
    }

    .sf-hero-right {
        border: 1px solid #5473bd;
        border-radius: 16px;
        padding: 17px;
        min-width: 124px;
        flex-shrink: 0;
    }

    .sf-hero-right strong {
        font-size: 34px;
        display: block;
        line-height: 1.2;
    }

    .sf-hero-right span {
        font-size: 11px;
        color: #d3e0fa;
    }

    .sf-hero-track {
        height: 5px;
        background: #364a76;
        border-radius: 8px;
        margin-top: 12px;
        overflow: hidden;
    }

    .sf-hero-track i {
        display: block;
        background: #76b5ff;
        height: 100%;
        border-radius: 8px;
    }


    /* =========================
       STATISTICS CARDS
       ========================= */

    .sf-metrics {
        display: grid;
        grid-template-columns:
            repeat(2,minmax(0,1fr));
        gap: 10px;
        min-height: 192px;
        padding: 14px;
    }

    .sf-metric {
        background: #f5f7fc;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 10px;
        min-width: 0;
    }

    .sf-icon {
        width: 35px;
        height: 35px;
        flex-shrink: 0;
        display: grid;
        place-items: center;
        border-radius: 9px;
        font-size: 20px;
        font-weight: 700;
    }

    .sf-blue {
        background: #e3edff;
        color: #245bd2;
    }

    .sf-green {
        background: #dcfce7;
        color: #166534;
    }

    .sf-violet {
        background: #ede9fe;
        color: #6d28d9;
    }

    .sf-teal {
        background: #d9f7f6;
        color: #0f766e;
    }

    .sf-red {
        background: #fee2e2;
        color: #b91c1c;
    }

    .sf-amber {
        background: #fef3c7;
        color: #92400e;
    }

    .sf-muted {
        color: #64748b;
        font-size: 11px;
        line-height: 1.3;
    }

    .sf-metric strong {
        font-size: 24px;
        line-height: 1.35;
        color: #14213b;
    }


    /* =========================
       SECTION HEADINGS
       ========================= */

    .sf-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 13px;
    }

    .sf-dashboard .sf-heading h3 {
        color: #14213b;
        font-size: 18px;
        letter-spacing: -.3px;
        margin: 0;
        padding: 0;
        line-height: 1.25;
    }

    .sf-heading > span {
        color: #64748b;
        font-size: 11px;
        text-align: right;
    }


    /* =========================
       UPCOMING ASSIGNMENTS
       ========================= */

    .sf-task {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        border-top: 1px solid #eef1f6;
        padding: 13px 0;
    }

    .sf-task-main {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
    }

    .sf-task-icon {
        background: #edf3ff;
        color: #2563eb;
        border-radius: 10px;
        width: 38px;
        height: 38px;
        display: grid;
        place-items: center;
        flex-shrink: 0;
        font-size: 20px;
    }

    .sf-task strong {
        display: block;
        font-size: 14px;
        overflow-wrap: anywhere;
    }

    .sf-task small {
        display: block;
        margin-top: 3px;
        color: #64748b;
        font-size: 12px;
    }

    .sf-pill {
        font-size: 10px;
        font-weight: 650;
        padding: 5px 9px;
        border-radius: 30px;
        flex-shrink: 0;
    }

    .sf-note,
    .sf-footer {
        font-size: 11px;
        color: #64748b;
    }

    .sf-note {
        padding-top: 6px;
    }

    .sf-footer {
        text-align: center;
        padding: 18px 0 0;
    }

    .sf-empty {
        padding: 17px 10px;
        background: #f5f7fc;
        border-radius: 10px;
        color: #64748b;
        font-size: 13px;
    }


    /* =========================
       MONTHLY CALENDAR
       ========================= */

    .sf-calendar {
        display: grid;
        grid-template-columns:
            repeat(7,minmax(0,1fr));
        row-gap: 5px;
        text-align: center;
    }

    .sf-weekday {
        font-size: 9px;
        font-weight: 700;
        color: #64748b;
        padding: 7px 0;
    }

    .sf-day {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 35px;
        font-size: 13px;
    }

    .sf-day span:first-child {
        width: 29px;
        height: 29px;
        display: grid;
        place-items: center;
        border-radius: 50%;
    }

    .sf-outside {
        color: #a9b3c3;
    }

    .sf-today span:first-child {
        background: #2563eb;
        color: white;
        font-weight: 700;
    }

    .sf-dot {
        position: absolute;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #f59e0b;
        bottom: 0;
        left: calc(50% - 2.5px);
    }

    .sf-calendar-legend {
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
        margin-top: 14px;
        font-size: 10px;
        color: #64748b;
    }

    .sf-calendar-legend i,
    .sf-progress-key i {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 5px;
    }

    .sf-legend-today {
        background: #2563eb;
    }

    .sf-legend-due {
        background: #f59e0b;
    }


    /* =========================
       CLASS TIMETABLE
       ========================= */

    .sf-table-wrap {
        overflow-x: auto;
    }

    .sf-table {
        border-collapse: collapse;
        width: 100%;
        font-size: 12px;
        border: none !important;
    }

    .sf-table th,
    .sf-table td {
        text-align: left;
        padding: 11px 7px;
        border: 0 !important;
        border-bottom:
            1px solid #edf1f7 !important;
        color: #14213b;
        background: white !important;
    }

    .sf-table th {
        color: #64748b;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: .4px;
    }


    /* =========================
       DONUT PROGRESS CHART
       ========================= */

    .sf-progress {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        padding: 10px 0;
    }

    .sf-ring {
        width: 124px;
        height: 124px;
        padding: 11px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .sf-ring > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        background: white;
        border-radius: 50%;
    }

    .sf-ring strong {
        font-size: 26px;
        line-height: 1.15;
    }

    .sf-ring small {
        color: #64748b;
        font-size: 10px;
    }

    .sf-progress-key {
        flex: 1;
        min-width: 115px;
        font-size: 12px;
    }

    .sf-progress-key > div {
        display: flex;
        align-items: center;
        margin: 9px 0;
    }

    .sf-progress-key b {
        margin-left: auto;
    }

    .sf-progress-key p {
        font-size: 11px;
        color: #475569;
        margin: 12px 0 0;
    }

    .sf-progress-key small {
        font-size: 10px;
        color: #64748b;
    }


    /* =========================
       AI ASSISTANT CARD
       ========================= */

    .sf-assistant {
        display: flex;
        align-items: center;
        gap: 13px;
        background: #eaf1ff;
        padding: 17px;
        border-radius: 15px;
        color: #1e40af;
    }

    .sf-assistant p {
        margin: 4px 0 0;
        color: #475569;
        font-size: 12px;
    }

    .sf-assistant-icon {
        display: grid;
        place-items: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        flex-shrink: 0;
        background: #2563eb;
        color: white;
        font-size: 24px;
    }


    /* =========================
       RESPONSIVE DESIGN
       ========================= */

    @media(max-width: 1050px) {

        .sf-grid {
            grid-template-columns: minmax(0,1fr);
        }

        .sf-metrics {
            min-height: 0;
            grid-template-columns:
                repeat(4,minmax(0,1fr));
        }

    }

    @media(max-width: 650px) {

        .sf-metrics {
            grid-template-columns:
                repeat(2,minmax(0,1fr));
        }

        .sf-hero {
            padding: 18px;
            flex-wrap: wrap;
        }

        .sf-hero-right {
            min-width: 0;
            width: 100%;
        }

        .sf-card {
            padding: 15px;
        }

        .sf-task {
            align-items: flex-start;
        }

        .sf-pill {
            max-width: 100px;
            white-space: normal;
            text-align: center;
        }

        .sf-task-icon {
            width: 30px;
            height: 30px;
        }

    }

    </style>
    """, unsafe_allow_html=True)
