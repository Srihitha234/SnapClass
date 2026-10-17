
import time
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialogue_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
)
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance


def teacherscreen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


# =========================================================
# TEACHER DASHBOARD
# =========================================================

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    st.subheader(
        f"Welcome, {teacher_data['name']}",
        text_alignment="center",
    )

    col1, col2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large",
    )

    with col1:
        header_dashboard()

    with col2:
        if st.button(
            "Logout",
            type="secondary",
            width="stretch",
            key="teacher_logout",
        ):
            st.session_state["is_logged_in"] = False
            st.session_state.pop("teacher_data", None)
            st.session_state.pop("current_teacher_tab", None)
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    # Dashboard navigation styling
    st.markdown(
        """
        <style>
        /* Keep dashboard navigation buttons readable */
        div[data-testid="stHorizontalBlock"] {
            align-items: stretch;
        }

        div[data-testid="stButton"] button {
            min-height: 46px;
            white-space: normal;
            overflow-wrap: anywhere;
            border-radius: 10px;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Three dashboard navigation buttons
    tab1, tab2, tab3 = st.columns(3, gap="small")

    with tab1:
        if st.button(
            "Take Attendance",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "take_attendance"
                else "secondary"
            ),
            width="stretch",
            key="tab_take_attendance",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        if st.button(
            "Manage Subjects",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "manage_subjects"
                else "secondary"
            ),
            width="stretch",
            key="tab_manage_subjects",
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        if st.button(
            "Attendance Records",
            type=(
                "primary"
                if st.session_state.current_teacher_tab == "attendance_records"
                else "secondary"
            ),
            width="stretch",
            key="tab_attendance_records",
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    # Display the selected dashboard section
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
    

    footer_dashboard()


# =========================================================
# TAKE ATTENDANCE
# =========================================================

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    # Initialize photo state
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "attendance_image_ids" not in st.session_state:
        st.session_state.attendance_image_ids = set()

    # Fetch teacher subjects
    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            "You have not created any subjects yet. "
            "Please create one to begin!"
        )
        return

    subject_options = {
        f"{subject['name']}-{subject['subject_code']}":
            subject["subject_id"]
        for subject in subjects
    }

    col1, col2 = st.columns(
        2,
        vertical_alignment="bottom",
    )

    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subject_options.keys()),
            key="attendance_subject_select",
        )

    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
            key="add_attendance_photos",
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    # Display uploaded photos
    if st.session_state.attendance_images:
        st.divider()
        st.subheader("Added Photos")

        gallery_cols = st.columns(4)

        for idx, image in enumerate(
            st.session_state.attendance_images
        ):
            with gallery_cols[idx % 4]:
                st.image(
                    image,
                    width="stretch",
                    caption=f"Photo {idx + 1}",
                )

        st.space()

        col1, col2, col3 = st.columns(3, gap="small")

        # Clear photos
        with col1:
            if st.button(
                "Clear All Photos",
                width="stretch",
                type="secondary",
                icon=":material/delete:",
                key="clear_all_attendance_photos",
            ):
                st.session_state.attendance_images = []
                st.session_state.attendance_image_ids = set()
                st.rerun()

        # Run face recognition
        with col2:
            if st.button(
                "Run Face Analysis",
                width="stretch",
                type="secondary",
                icon=":material/face:",
                key="run_face_analysis",
            ):
                try:
                    with st.spinner(
                        "Analyzing classroom photos..."
                    ):
                        all_detected_ids = {}

                        for idx, image in enumerate(
                            st.session_state.attendance_images
                        ):
                            image_np = np.array(
                                image.convert("RGB")
                            )

                            detected, _, _ = predict_attendance(
                                image_np
                            )

                            if detected:
                                for student_id in detected.keys():
                                    student_id = int(student_id)

                                    all_detected_ids.setdefault(
                                        student_id, []
                                    ).append(f"Photo {idx + 1}")

                        enrolled_response = (
                            supabase.table("subject_students")
                            .select("*,students(*)")
                            .eq("subject_id", selected_subject_id)
                            .execute()
                        )

                        enrolled_students = enrolled_response.data

                        if not enrolled_students:
                            st.warning(
                                "No students are enrolled in this subject."
                            )
                            return

                        results = []
                        attendance_to_log = []

                        current_timestamp = (
                            datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S"
                            )
                        )

                        for record in enrolled_students:
                            student = record.get("students")

                            if not student:
                                continue

                            student_id = int(student["student_id"])

                            sources = all_detected_ids.get(
                                student_id, []
                            )

                            is_present = len(sources) > 0

                            results.append(
                                {
                                    "Name": student["name"],
                                    "ID": student_id,
                                    "Source": (
                                        ", ".join(sources)
                                        if is_present
                                        else "-"
                                    ),
                                    "Status": (
                                        "Present"
                                        if is_present
                                        else "Absent"
                                    ),
                                }
                            )

                            attendance_to_log.append(
                                {
                                    "student_id": student_id,
                                    "subject_id": selected_subject_id,
                                    "timestamp": current_timestamp,
                                    "is_present": bool(is_present),
                                }
                            )

                        if not results:
                            st.warning(
                                "No valid enrolled student records were found."
                            )
                            return

                    # Show the attendance review dialog
                    attendance_result_dialog(
                        pd.DataFrame(results),
                        attendance_to_log,
                    )

                except Exception as e:
                    st.error(
                        f"Face attendance analysis failed: {e}"
                    )

        # Run voice attendance
        with col3:
            if st.button(
                "Use Voice Attendance",
                type="primary",
                width="stretch",
                icon=":material/mic:",
                key="use_voice_attendance",
            ):
                voice_attendance_dialog(selected_subject_id)


# =========================================================
# MANAGE SUBJECTS
# =========================================================

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects")

    with col2:
        if st.button(
            "Create New Subject",
            width="stretch",
            type="primary",
            key="create_new_subject",
        ):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for subject in subjects:
            stats = [
                (
                    "👥",
                    "Students",
                    subject["total_students"],
                ),
                (
                    "📚",
                    "Classes",
                    subject["total_classes"],
                ),
            ]

            def share_btn(subject=subject):
                if st.button(
                    f"Share Code: {subject['name']}",
                    key=f"share_{subject['subject_code']}",
                    icon=":material/share:",
                    width="stretch",
                ):
                    share_subject_dialog(
                        subject["name"],
                        subject["subject_code"],
                    )

            subject_card(
                name=subject["name"],
                code=subject["subject_code"],
                section=subject["section"],
                stats=stats,
                footer_callback=share_btn,
            )

    else:
        st.info("No subjects found. Create one above.")


# =========================================================
# ATTENDANCE RECORDS
# =========================================================

def teacher_tab_attendance_records():
    st.header("Attendance Records")

    st.info(
        "Attendance history will appear here once the records "
        "view is implemented."
    )


# =========================================================
# TEACHER LOGIN
# =========================================================

def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    style_background_dashboard()
    style_base_layout()

    col1, col2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large",
    )

    with col1:
        header_dashboard()

    with col2:
        if st.button(
            "Go Back to Home",
            type="secondary",
            key="teacher_login_back",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header(
        "Login Using Password",
        text_alignment="center",
    )

    st.space()

    teacher_username = st.text_input(
        "Enter Username",
        placeholder="Enter your username",
        key="teacher_login_username",
    )

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Enter your password",
        key="teacher_login_password",
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Login",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_login_button",
        ):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(
                    "Invalid username and password combination."
                )

    with col2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/person_add:",
            width="stretch",
            key="teacher_register_instead",
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# =========================================================
# TEACHER REGISTRATION
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm,
):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken."

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(
            teacher_username,
            teacher_pass,
            teacher_name,
        )

        return True, "Account created successfully! Please log in."

    except Exception as e:
        return False, f"Registration failed: {e}"


def teacher_screen_register():
    style_background_dashboard()
    style_base_layout()

    col1, col2 = st.columns(
        2,
        vertical_alignment="center",
        gap="large",
    )

    with col1:
        header_dashboard()

    with col2:
        if st.button(
            "Go Back to Home",
            type="secondary",
            key="teacher_register_back",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header(
        "Register Your Teacher Profile",
        text_alignment="center",
    )

    st.space()

    teacher_username = st.text_input(
        "Enter Username",
        placeholder="Choose a username",
        key="teacher_register_username",
    )

    teacher_name = st.text_input(
        "Enter Name",
        placeholder="Enter your name",
        key="teacher_register_name",
    )

    teacher_pass = st.text_input(
        "Enter Password",
        type="password",
        placeholder="Choose a password",
        key="teacher_register_password",
    )

    teacher_pass_confirm = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password",
        key="teacher_register_password_confirm",
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Register Now",
            icon=":material/person_add:",
            width="stretch",
            key="teacher_register_button",
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm,
            )

            if success:
                st.success(message)
                time.sleep(1)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with col2:
        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch",
            key="teacher_login_instead",
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()
