import streamlit as st
import time

from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Enroll in Subject")
def enroll_dialog():

    # =====================================================
    # DIALOG FONT COLOR
    # =====================================================

    st.markdown(
        """
        <style>

        /* Dialog container */
        [role="dialog"] {
            color: white !important;
        }

        /* Dialog heading */
        [role="dialog"] h1,
        [role="dialog"] h2,
        [role="dialog"] h3,
        [role="dialog"] h4 {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Dialog normal text */
        [role="dialog"] p {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Streamlit markdown */
        [role="dialog"] [data-testid="stMarkdownContainer"] {
            color: white !important;
        }

        [role="dialog"] [data-testid="stMarkdownContainer"] p {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Text input label */
        [role="dialog"] [data-testid="stWidgetLabel"] {
            color: white !important;
        }

        [role="dialog"] [data-testid="stWidgetLabel"] * {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Text input */
        [role="dialog"] input {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Placeholder */
        [role="dialog"] input::placeholder {
            color: #b8b8c5 !important;
            -webkit-text-fill-color: #b8b8c5 !important;
            opacity: 1 !important;
        }

        /* Button text */
        [role="dialog"] button,
        [role="dialog"] button * {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Warning / success messages */
        [role="dialog"] [data-testid="stAlert"] p,
        [role="dialog"] [data-testid="stAlert"] span {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # DIALOG CONTENT
    # =====================================================

    st.write("Enter the subject code provided")

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg. CS101"
    )


    # =====================================================
    # ENROLL
    # =====================================================

    if st.button(
        "Enroll now",
        type="primary",
        width="stretch"
    ):

        if join_code:

            res = (
                supabase
                .table("subjects")
                .select("subject_id,name,subject_code")
                .eq("subject_code", join_code)
                .execute()
            )

            if res.data:

                subject = res.data[0]

                student_id = st.session_state.student_data["student_id"]

                check = (
                    supabase
                    .table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )

                if check.data:

                    st.warning(
                        "You are already enrolled in this program"
                    )

                else:

                    enroll_student_to_subject(
                        student_id,
                        subject["subject_id"]
                    )

                    st.success(
                        "Successfully enrolled!"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                st.warning(
                    "Please enter a valid subject code"
                )

        else:

            st.warning(
                "Please enter a subject code"
            )