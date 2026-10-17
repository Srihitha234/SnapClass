
import streamlit as st

from src.database.db import create_attendance


@st.dialog("Attendance Reports", width="large")
def attendance_result_dialog(df, logs):
    st.markdown(
        """
        <style>
        div[data-testid="stDialog"] h1,
        div[data-testid="stDialog"] h2,
        div[data-testid="stDialog"] h3,
        div[data-testid="stDialog"] h4 {
            color: #FFFFFF !important;
        }

        div[data-testid="stDialog"] p {
            color: #F1F5F9 !important;
        }

        div[data-testid="stDialog"] .stButton button {
            min-height: 46px;
            border-radius: 12px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="color:#CBD5E1 !important; font-size:15px;">
            Review the attendance records before saving.
        </p>
        """,
        unsafe_allow_html=True,
    )

    total_students = len(df)

    if "Status" in df.columns:
        statuses = (
            df["Status"].astype(str).str.strip().str.lower()
        )
        present_count = statuses.isin(
            ["present", "✅ present"]
        ).sum()
    else:
        present_count = 0

    absent_count = total_students - present_count

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", total_students)

    with col2:
        st.metric("Present", int(present_count))

    with col3:
        st.metric("Absent", int(absent_count))

    st.divider()

    st.markdown(
        """
        <p style="
            color:#FFFFFF !important;
            font-size:20px;
            font-weight:700;
            margin-bottom:10px;
        ">Attendance Details</p>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Verify the student names and attendance statuses before saving."
    )

    st.divider()

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        if st.button(
            "Discard",
            width="stretch",
            type="secondary",
            key="discard_attendance",
        ):
            st.session_state.attendance_images = []
            st.session_state.attendance_image_ids = set()
            st.session_state.voice_attendance_results = None
            st.session_state.show_voice_results = False
            st.rerun()

    with col2:
        if st.button(
            "Confirm & Save",
            width="stretch",
            type="primary",
            key="confirm_attendance",
        ):
            try:
                create_attendance(logs)

                st.session_state.attendance_images = []
                st.session_state.attendance_image_ids = set()
                st.session_state.voice_attendance_results = None
                st.session_state.show_voice_results = False

                st.toast("Attendance saved successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Sync failed: {e}")


# Keep these names available for existing imports.
show_attendance_result = attendance_result_dialog
show_attendance_results = attendance_result_dialog
debug = st.session_state.get("voice_debug_info")

if debug:
    with st.expander("Voice recognition debug"):
        st.write("Registered student IDs:", debug["registered_ids"])
        st.write("Detected student IDs and scores:", debug["detected_scores"])
