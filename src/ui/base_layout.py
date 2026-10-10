import streamlit as st


def style_background_home():

    st.markdown("""
        <style>

        /* =========================
           HOME PAGE BACKGROUND
           ========================= */

        .stApp {
            background: #5865F2 !important;
        }


        /* =========================
           STUDENT / TEACHER CARDS
           ========================= */

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

        /* =========================
           DASHBOARD BACKGROUND
           ========================= */

        .stApp {
            background: #E0E3FF !important;
        }

        </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
        <style>

        /* =====================================================
           GOOGLE FONTS
           ===================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Edu+NSW+ACT+Cursive:wght@400..700&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap'
        );


        /* =====================================================
           HIDE STREAMLIT DEFAULT UI
           ===================================================== */

        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }


        /* =====================================================
           MAIN CONTAINER
           ===================================================== */

        .block-container {
            padding-top: 1.5rem !important;
        }


        /* =====================================================
           MAIN HEADING
           ===================================================== */

        h1 {
            font-family: 'Edu NSW ACT Cursive', cursive !important;

            font-size: 3.5rem !important;

            line-height: 1.1 !important;

            margin-bottom: 0 !important;

            color: black !important;
        }


        /* =====================================================
           SECONDARY HEADING
           ===================================================== */

        h2 {
            font-family: 'Edu NSW ACT Cursive', cursive !important;

            font-size: 2rem !important;

            line-height: 0.9 !important;

            margin-bottom: 0 !important;

            color: black !important;
        }


        /* =====================================================
           NORMAL TEXT
           ===================================================== */

        h3,
        h4,
        p {
            font-family: 'Roboto', sans-serif !important;

            color: black !important;
        }


        /* =====================================================
           ALL BUTTONS
           ===================================================== */

        button {
            border-radius: 1.5rem !important;

            padding: 10px 20px !important;

            border: none !important;

            font-family: 'Roboto', sans-serif !important;

            transition: transform 0.25s ease-in-out !important;
        }


        /* =====================================================
           PRIMARY BUTTON
           ===================================================== */

        button[kind="primary"] {
            background-color: #5865F2 !important;

            color: white !important;
        }

        button[kind="primary"] p,
        button[kind="primary"] span {
            color: white !important;
        }


        /* =====================================================
           SECONDARY BUTTON
           ===================================================== */

        button[kind="secondary"] {
            background-color: #EB459E !important;

            color: white !important;
        }

        button[kind="secondary"] p,
        button[kind="secondary"] span {
            color: white !important;
        }


        /* =====================================================
           TERTIARY BUTTON
           ===================================================== */

        button[kind="tertiary"] {
            background-color: black !important;

            color: white !important;
        }

        button[kind="tertiary"] p,
        button[kind="tertiary"] span {
            color: white !important;
        }


        /* =====================================================
           TEXT INPUTS
           ===================================================== */

        input {
            font-family: 'Roboto', sans-serif !important;
        }


        /* =====================================================
           TEXT INPUT PLACEHOLDER
           ===================================================== */

        input::placeholder {
            font-family: 'Roboto', sans-serif !important;
        }


        /* =====================================================
           SELECT BOX / TEXT AREA
           ===================================================== */

        textarea,
        select {
            font-family: 'Roboto', sans-serif !important;
        }


        /* =====================================================
           BUTTON HOVER
           ===================================================== */

        button:hover {
            transform: scale(1.05) !important;
        }

        </style>
    """, unsafe_allow_html=True)