
import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
        .stApp {
            background: #5865F2 !important;
        }

        .stApp div[data-testid="stColumn"] {
            background-color: #E0E3FF !important;
            padding: 2.5rem !important;
            border-radius: 5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
        .stApp {
            background: #E0E3FF !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Edu+NSW+ACT+Cursive:wght@400..700&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap'
        );

        /* Hide default Streamlit UI */
        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }

        /* Main container */
        .block-container {
            padding-top: 1.5rem !important;
        }

        /* Main headings: black on the light dashboard */
        .stApp h1,
        .stApp h2 {
            font-family: 'Edu NSW ACT Cursive', cursive !important;
            color: #000000 !important;
        }

        .stApp h1 {
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0 !important;
        }

        .stApp h2 {
            font-size: 2rem !important;
            line-height: 0.9 !important;
            margin-bottom: 0 !important;
        }

        /* Normal dashboard text */
        .stApp h3,
        .stApp h4,
        .stApp p {
            font-family: 'Roboto', sans-serif !important;
            color: #000000 !important;
        }

        /* Dialog: override the dashboard's black text */
        div[data-testid="stDialog"],
        div[data-testid="stDialog"] h1,
        div[data-testid="stDialog"] h2,
        div[data-testid="stDialog"] h3,
        div[data-testid="stDialog"] h4,
        div[data-testid="stDialog"] p,
        div[data-testid="stDialog"] label,
        div[data-testid="stDialog"] span {
            color: #FFFFFF !important;
        }

        div[data-testid="stDialog"] h1,
        div[data-testid="stDialog"] h2 {
            font-family: 'Roboto', sans-serif !important;
        }

        /* Toast notification text */
        div[data-testid="stToast"],
        div[data-testid="stToast"] p,
        div[data-testid="stToast"] span {
            color: #FFFFFF !important;
        }

        /* Buttons */
        button {
            border-radius: 1.5rem !important;
            padding: 10px 20px !important;
            border: none !important;
            font-family: 'Roboto', sans-serif !important;
            transition: transform 0.25s ease-in-out !important;
        }

        /* Primary buttons */
        button[kind="primary"] {
            background-color: #5865F2 !important;
            color: #FFFFFF !important;
        }

        button[kind="primary"] p,
        button[kind="primary"] span {
            color: #FFFFFF !important;
        }

        /* Secondary buttons */
        button[kind="secondary"] {
            background-color: #EB459E !important;
            color: #FFFFFF !important;
        }

        button[kind="secondary"] p,
        button[kind="secondary"] span {
            color: #FFFFFF !important;
        }

        /* Tertiary buttons */
        button[kind="tertiary"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        button[kind="tertiary"] p,
        button[kind="tertiary"] span {
            color: #FFFFFF !important;
        }

        /* Input fields */
        input,
        textarea,
        select {
            font-family: 'Roboto', sans-serif !important;
        }

        input::placeholder {
            font-family: 'Roboto', sans-serif !important;
        }

        /* Button hover */
        button:hover {
            transform: scale(1.02) !important;
        }
        </style>
    """, unsafe_allow_html=True)
