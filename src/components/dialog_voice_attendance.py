
import streamlit as st
import pandas as pd
from datetime import datetime

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase


@st.dialog("Voice Attendance", width="large")
def voice_attendance_dialog(selected_subject_id):
    st.write(
        "Record students saying 'I am present'. "
        "The AI will attempt to recognize their voices."
    )

    audio_data = st.audio_input(
        "Record classroom audio",
        key="voice_attendance_audio",
    )

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary",
        key="analyze_voice_attendance",
    ):
        if audio_data is None:
            st.warning("Please record audio before analyzing.")

        else:
            try:
                with st.spinner("Processing audio data..."):
                    enrolled_res = (
                        supabase.table("subject_students")
                        .select("*, students(*)")
                        .eq("subject_id", selected_subject_id)
                        .execute()
                    )

                    enrolled_students = enrolled_res.data

                    if not enrolled_students:
                        st.warning(
                            "No students are enrolled in this subject."
                        )
                        return

                    candidates_dict = {
                        record["students"]["student_id"]:
                        record["students"]["voice_embedding"]
                        for record in enrolled_students
                        if record.get("students")
                        and record["students"].get("voice_embedding")
                    }

                    if not candidates_dict:
                        st.error(
                            "No enrolled students have registered "
                            "voice profiles."
                        )
                        return

                    audio_bytes = audio_data.getvalue()

                    if not audio_bytes:
                        st.warning(
                            "The recording is empty. Please try again."
                        )
                        return

                    detected_scores = process_bulk_audio(
                        audio_bytes,
                        candidates_dict,
                    )

                    results = []
                    attendance_to_log = []

                    current_timestamp = datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    for record in enrolled_students:
                        student = record.get("students")

                        if not student:
                            continue

                        student_id = student["student_id"]
                        score = detected_scores.get(student_id, 0.0)

                        # Confirm this threshold against your pipeline's
                        # score definition before relying on it.
                        is_present = score > 0

                        results.append({
                            "Name": student["name"],
                            "ID": student_id,
                            "Source": (
                                f"{score:.3f}" if is_present else "-"
                            ),
                            "Status": (
                                "Present" if is_present else "Absent"
                            ),
                        })

                        attendance_to_log.append({
                            "student_id": student_id,
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present),
                        })

                    if not results:
                        st.warning(
                            "No valid student records were found."
                        )
                        return

                    # Store results for the dashboard to display later.
                    st.session_state.voice_attendance_results = (
                        pd.DataFrame(results),
                        attendance_to_log,
                    )

                    st.session_state.show_voice_results = True

                    st.success(
                        "Analysis complete! Close this dialog "
                        "to review the attendance report."
                    )

            except Exception as e:
                st.error(f"Voice attendance analysis failed: {e}")
