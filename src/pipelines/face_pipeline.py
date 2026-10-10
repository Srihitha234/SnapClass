import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from src.database.db import get_all_students


# =========================================================
# SETTINGS
# =========================================================

# Start with a strict threshold.
# Smaller distance = more similar faces.
FACE_MATCH_THRESHOLD = 0.50


# =========================================================
# LOAD DLIB MODELS
# =========================================================

@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_five_point_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


# =========================================================
# GET FACE EMBEDDINGS
# =========================================================

def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)

    encodings = []

    for face in faces:

        shape = sp(
            image_np,
            face
        )

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encoding = np.array(
            face_descriptor,
            dtype=np.float64
        )

        encodings.append(encoding)

    return encodings


# =========================================================
# GET REGISTERED STUDENT FACE DATA
# =========================================================

def get_student_face_data():

    students = get_all_students()

    student_faces = []

    for student in students:

        embedding = student.get("face_embedding")

        if embedding is None:
            continue

        if len(embedding) != 128:
            print(
                f"WARNING: Student {student.get('student_id')} "
                f"has invalid face embedding length: "
                f"{len(embedding)}"
            )
            continue

        student_faces.append(
            {
                "student_id": student["student_id"],
                "name": student["name"],
                "embedding": np.array(
                    embedding,
                    dtype=np.float64
                )
            }
        )

    return student_faces


# =========================================================
# FIND BEST MATCH
# =========================================================

def find_best_match(
    new_embedding,
    student_faces
):

    best_student_id = None
    best_student_name = None
    best_distance = float("inf")

    for student in student_faces:

        stored_embedding = student["embedding"]

        distance = np.linalg.norm(
            stored_embedding - new_embedding
        )

        print(
            f"[FACE] "
            f"{student['name']} "
            f"(ID={student['student_id']}) "
            f"distance={distance:.4f}"
        )

        if distance < best_distance:

            best_distance = distance

            best_student_id = student["student_id"]

            best_student_name = student["name"]

    return (
        best_student_id,
        best_student_name,
        best_distance
    )


# =========================================================
# PREDICT ATTENDANCE / FACE LOGIN
# =========================================================

def predict_attendance(class_image_np):

    # -----------------------------------------------------
    # Detect faces in image
    # -----------------------------------------------------

    encodings = get_face_embeddings(
        class_image_np
    )

    detected_student = {}

    # -----------------------------------------------------
    # No face detected
    # -----------------------------------------------------

    if len(encodings) == 0:

        print("[FACE] No face detected.")

        return (
            detected_student,
            [],
            0
        )

    # -----------------------------------------------------
    # Get all registered student faces
    # -----------------------------------------------------

    student_faces = get_student_face_data()

    # -----------------------------------------------------
    # No registered students
    # -----------------------------------------------------

    if not student_faces:

        print(
            "[FACE] No registered face embeddings."
        )

        return (
            detected_student,
            [],
            len(encodings)
        )

    # -----------------------------------------------------
    # Get all registered IDs
    # -----------------------------------------------------

    all_students = [
        student["student_id"]
        for student in student_faces
    ]

    # -----------------------------------------------------
    # Process every detected face
    # -----------------------------------------------------

    for encoding in encodings:

        (
            predicted_id,
            predicted_name,
            best_distance
        ) = find_best_match(
            encoding,
            student_faces
        )

        print(
            "----------------------------------------"
        )

        print(
            f"[FACE] BEST MATCH: "
            f"{predicted_name}"
        )

        print(
            f"[FACE] STUDENT ID: "
            f"{predicted_id}"
        )

        print(
            f"[FACE] DISTANCE: "
            f"{best_distance:.4f}"
        )

        print(
            f"[FACE] THRESHOLD: "
            f"{FACE_MATCH_THRESHOLD}"
        )

        print(
            "----------------------------------------"
        )

        # -------------------------------------------------
        # Accept only if distance is below threshold
        # -------------------------------------------------

        if (
            predicted_id is not None
            and best_distance <= FACE_MATCH_THRESHOLD
        ):

            detected_student[
                predicted_id
            ] = True

        else:

            print(
                "[FACE] Face rejected."
            )

    return (
        detected_student,
        all_students,
        len(encodings)
    )


# =========================================================
# COMPATIBILITY FUNCTION
# =========================================================

def train_classifier():

    # -----------------------------------------------------
    # There is no SVM anymore.
    #
    # Face embeddings are compared directly against the
    # embeddings stored in the database.
    #
    # This function remains so studentscreen.py does not
    # break.
    # -----------------------------------------------------

    return True