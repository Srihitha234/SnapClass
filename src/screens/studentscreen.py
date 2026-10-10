import streamlit as st
import time

from PIL import Image
import numpy as np


from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)


from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)


from src.pipelines.voice_pipeline import get_voice_embedding


from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subjects
)


from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_dashboard():

    student_data = st.session_state.student_data

    student_id = student_data["student_id"]
    student_name = student_data["name"]


    # =====================================================
    # WELCOME
    # =====================================================

    st.subheader(
        f"Welcome, {student_name}",
        text_alignment="center"
    )


    # =====================================================
    # HEADER + LOGOUT
    # =====================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )


    with c1:

        header_dashboard()


    with c2:

        if st.button(
            "Logout",
            type="secondary",
            key="student_logout",
            shortcut="control+backspace"
        ):

            # Remove current student
            st.session_state.pop(
                "student_data",
                None
            )

            # Reset login state
            st.session_state["is_logged_in"] = False
            st.session_state["user_role"] = None

            st.rerun()


    st.space()


    # =====================================================
    # ENROLLED SUBJECTS HEADER
    # =====================================================

    c1, c2 = st.columns(2)


    with c1:

        st.header(
            "Your Enrolled Subjects"
        )


    with c2:

        if st.button(
            "Enroll in Subject",
            type="primary",
            width="stretch",
            key="enroll_subject_button"
        ):

            enroll_dialog()


    st.divider()


    # =====================================================
    # LOAD STUDENT DATA
    # =====================================================

    with st.spinner(
        "Loading your enrolled subjects.."
    ):

        subjects = get_student_subjects(
            student_id
        )

        logs = get_student_attendance(
            student_id
        )


    # =====================================================
    # ATTENDANCE STATISTICS
    # =====================================================

    stats_map = {}


    for log in logs:

        sid = log["subject_id"]

        if sid not in stats_map:

            stats_map[sid] = {
                "total": 0,
                "attended": 0
            }


        # Count attendance record
        stats_map[sid]["total"] += 1


        # Count only this log
        if log.get("is_present"):

            stats_map[sid]["attended"] += 1


    # =====================================================
    # SUBJECT CARDS
    # =====================================================

    cols = st.columns(
        2,
        gap="medium"
    )


    for i, sub_node in enumerate(subjects):

        sub = sub_node["subjects"]

        sid = sub["subject_id"]

        stats = stats_map.get(
            sid,
            {
                "total": 0,
                "attended": 0
            }
        )


        # =================================================
        # UNENROLL BUTTON
        # =================================================

        def unenroll_button(
            sid=sid,
            subject_name=sub["name"]
        ):

            if st.button(
                "Unenroll from this course",
                type="tertiary",
                width="stretch",
                key=f"unenroll_{sid}"
            ):

                unenroll_student_to_subjects(
                    student_id,
                    sid
                )

                st.toast(
                    f"Unenrolled from "
                    f"{subject_name} successfully!"
                )

                st.rerun()


        # =================================================
        # DISPLAY SUBJECT CARD
        # =================================================

        with cols[i % 2]:

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    (
                        "📅",
                        "Total",
                        stats["total"]
                    ),
                    (
                        "✔️",
                        "Attended",
                        stats["attended"]
                    ),
                ],
                footer_callback=unenroll_button
            )


    # =====================================================
    # FOOTER
    # =====================================================

    footer_dashboard()


# =========================================================
# STUDENT SCREEN
# =========================================================

def studentscreen():

    style_background_dashboard()
    style_base_layout()


    # =====================================================
    # IF STUDENT IS ALREADY LOGGED IN
    # =====================================================

    if "student_data" in st.session_state:

        student_dashboard()

        return


    # =====================================================
    # HEADER + BACK BUTTON
    # =====================================================

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )


    with c1:

        header_dashboard()


    with c2:

        if st.button(
            "Go back to Home",
            type="secondary",
            key="student_go_home",
            shortcut="control+backspace"
        ):

            st.session_state.pop(
                "student_data",
                None
            )

            st.session_state["is_logged_in"] = False
            st.session_state["user_role"] = None
            st.session_state["login_type"] = None

            st.rerun()


    # =====================================================
    # LOGIN HEADINGS
    # =====================================================

    st.header(
        "Login using password",
        text_alignment="center"
    )

    st.header(
        "Login using FACEID",
        text_alignment="center"
    )

    st.space()
    st.space()


    # =====================================================
    # REGISTRATION FLAG
    # =====================================================

    show_registration = False


    # =====================================================
    # FACE LOGIN
    # =====================================================

    photo_source = st.camera_input(
        "Position your face in the center"
    )


    if photo_source:

        image_np = np.array(
            Image.open(photo_source)
        )


        with st.spinner(
            "AI is scanning.."
        ):

            detected, all_ids, num_faces = (
                predict_attendance(
                    image_np
                )
            )


        # =================================================
        # NO FACE
        # =================================================

        if num_faces == 0:

            st.warning(
                "Face not found! "
                "Please make sure your face is visible."
            )


        # =================================================
        # MULTIPLE FACES
        # =================================================

        elif num_faces > 1:

            st.warning(
                "Multiple faces found. "
                "Please make sure only your face "
                "is visible."
            )


        # =================================================
        # EXACTLY ONE FACE
        # =================================================

        else:

            # -------------------------------------------------
            # FACE RECOGNIZED
            # -------------------------------------------------

            if detected:

                student_id = list(
                    detected.keys()
                )[0]


                # -------------------------------------------------
                # Get all students
                # -------------------------------------------------

                all_students = get_all_students()


                # -------------------------------------------------
                # Find recognized student
                # -------------------------------------------------

                student = next(
                    (
                        s
                        for s in all_students
                        if s["student_id"] == student_id
                    ),
                    None
                )


                if student:

                    # -------------------------------------------------
                    # Clear any old student session
                    # -------------------------------------------------

                    st.session_state.pop(
                        "student_data",
                        None
                    )


                    # -------------------------------------------------
                    # Login recognized student
                    # -------------------------------------------------

                    st.session_state["is_logged_in"] = True

                    st.session_state["user_role"] = "student"

                    st.session_state["student_data"] = student


                    st.toast(
                        f"Welcome Back "
                        f"{student['name']}"
                    )


                    time.sleep(1)

                    st.rerun()


            # -------------------------------------------------
            # FACE NOT RECOGNIZED
            # -------------------------------------------------

            else:

                st.info(
                    "Face not recognized! "
                    "You might be a new student."
                )

                show_registration = True


    # =========================================================
    # REGISTRATION
    # =========================================================

    if show_registration:

        with st.container(
            border=True
        ):

            st.header(
                "Register new Profile"
            )


            # =================================================
            # NAME
            # =================================================

            new_name = st.text_input(
                "Enter your name",
                placeholder="E.g. Hamza Ravi"
            )


            # =================================================
            # VOICE ENROLLMENT
            # =================================================

            st.subheader(
                "Optional: Voice Enrollment"
            )

            st.info(
                "Enroll your voice for "
                "voice-only attendance"
            )


            # =================================================
            # VOICE INPUT
            # =================================================

            audio_data = st.audio_input(
                'Record a short phrase like '
                '"I am present, my name is Akash."'
            )


            # =================================================
            # CREATE ACCOUNT
            # =================================================

            if st.button(
                "Create Account",
                type="primary",
                key="create_student_account"
            ):


                # =============================================
                # NAME VALIDATION
                # =============================================

                if not new_name.strip():

                    st.warning(
                        "Please enter your name!"
                    )


                else:

                    with st.spinner(
                        "Creating profile.."
                    ):


                        # =====================================
                        # FACE EMBEDDING
                        # =====================================

                        img = np.array(
                            Image.open(
                                photo_source
                            )
                        )


                        encodings = get_face_embeddings(
                            img
                        )


                        # =====================================
                        # NO FACE
                        # =====================================

                        if len(encodings) == 0:

                            st.error(
                                "Could not detect your face. "
                                "Please capture your face again."
                            )


                        # =====================================
                        # MULTIPLE FACES
                        # =====================================

                        elif len(encodings) > 1:

                            st.error(
                                "Multiple faces detected. "
                                "Please make sure only your face "
                                "is visible and capture again."
                            )


                        # =====================================
                        # EXACTLY ONE FACE
                        # =====================================

                        else:

                            face_emb = (
                                encodings[0].tolist()
                            )


                            # =================================
                            # CHECK IF FACE ALREADY REGISTERED
                            # =================================

                            existing_students = (
                                get_all_students()
                            )


                            duplicate_student = None
                            duplicate_distance = float("inf")


                            new_embedding = np.array(
                                face_emb,
                                dtype=np.float64
                            )


                            for existing_student in existing_students:

                                existing_embedding = (
                                    existing_student.get(
                                        "face_embedding"
                                    )
                                )


                                if not existing_embedding:
                                    continue


                                existing_embedding = np.array(
                                    existing_embedding,
                                    dtype=np.float64
                                )


                                if len(existing_embedding) != 128:
                                    continue


                                distance = np.linalg.norm(
                                    existing_embedding
                                    - new_embedding
                                )


                                print(
                                    f"[REGISTRATION] "
                                    f"{existing_student['name']} "
                                    f"(ID={existing_student['student_id']}) "
                                    f"distance={distance:.4f}"
                                )


                                if distance < duplicate_distance:

                                    duplicate_distance = distance

                                    duplicate_student = (
                                        existing_student
                                    )


                            # =================================
                            # REJECT DUPLICATE FACE
                            # =================================

                            registration_threshold = 0.50


                            if (
                                duplicate_student is not None
                                and duplicate_distance
                                <= registration_threshold
                            ):

                                st.error(
                                    f"This face is already "
                                    f"registered as "
                                    f"{duplicate_student['name']}. "
                                    f"Please use a different face."
                                )


                            else:

                                # =================================
                                # VOICE EMBEDDING
                                # =================================

                                voice_emb = None


                                if audio_data is not None:

                                    voice_emb = (
                                        get_voice_embedding(
                                            audio_data.read()
                                        )
                                    )


                                # =================================
                                # CREATE STUDENT
                                # =================================

                                response_data = (
                                    create_student(
                                        new_name.strip(),
                                        face_embedding=face_emb,
                                        voice_embedding=voice_emb
                                    )
                                )


                                if response_data:

                                    # =================================
                                    # FACE CLASSIFIER COMPATIBILITY
                                    # =================================

                                    train_classifier()


                                    # =================================
                                    # CLEAR OLD STUDENT
                                    # =================================

                                    st.session_state.pop(
                                        "student_data",
                                        None
                                    )


                                    # =================================
                                    # LOGIN NEW STUDENT
                                    # =================================

                                    st.session_state[
                                        "is_logged_in"
                                    ] = True


                                    st.session_state[
                                        "user_role"
                                    ] = "student"


                                    st.session_state[
                                        "student_data"
                                    ] = response_data[0]


                                    st.toast(
                                        f"Profile Created! "
                                        f"Hi {new_name.strip()}!"
                                    )


                                    time.sleep(1)

                                    st.rerun()


                                else:

                                    st.error(
                                        "Could not create "
                                        "student profile."
                                    )


    # =====================================================
    # FOOTER
    # =====================================================

    footer_dashboard()