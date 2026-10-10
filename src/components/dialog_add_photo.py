import streamlit as st
from PIL import Image
import io
import hashlib


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write("Add classroom photos to scan for attendance")

    # =====================================================
    # INITIALIZE
    # =====================================================

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    if "attendance_image_ids" not in st.session_state:
        st.session_state.attendance_image_ids = set()

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"


    # =====================================================
    # CAMERA / UPLOAD TABS
    # =====================================================

    t1, t2 = st.columns(2)

    with t1:

        camera_type = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )

        if st.button(
            "Camera",
            type=camera_type,
            width="stretch"
        ):

            st.session_state.photo_tab = "camera"
            st.rerun()


    with t2:

        upload_type = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )

        if st.button(
            "Upload photos",
            type=upload_type,
            width="stretch"
        ):

            st.session_state.photo_tab = "upload"
            st.rerun()


    # =====================================================
    # CAMERA
    # =====================================================

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam"
        )

        if cam_photo:

            image_bytes = cam_photo.getvalue()

            image_id = hashlib.md5(
                image_bytes
            ).hexdigest()

            # Only add if this photo is new
            if image_id not in st.session_state.attendance_image_ids:

                image = Image.open(
                    io.BytesIO(image_bytes)
                ).copy()

                st.session_state.attendance_images.append(
                    image
                )

                st.session_state.attendance_image_ids.add(
                    image_id
                )

                st.toast(
                    "Photo added!",
                    icon="📸"
                )

                st.rerun()


    # =====================================================
    # UPLOAD
    # =====================================================

    if st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if uploaded_files:

            new_photos = 0

            for file in uploaded_files:

                image_bytes = file.getvalue()

                image_id = hashlib.md5(
                    image_bytes
                ).hexdigest()

                # Prevent duplicate addition
                if image_id not in st.session_state.attendance_image_ids:

                    image = Image.open(
                        io.BytesIO(image_bytes)
                    ).copy()

                    st.session_state.attendance_images.append(
                        image
                    )

                    st.session_state.attendance_image_ids.add(
                        image_id
                    )

                    new_photos += 1

            if new_photos > 0:

                st.toast(
                    f"{new_photos} photo(s) added!",
                    icon="📸"
                )

                st.rerun()


    # =====================================================
    # SHOW PHOTOS INSIDE DIALOG
    # =====================================================

    if st.session_state.attendance_images:

        st.divider()

        st.write(
            f"Photos added: "
            f"**{len(st.session_state.attendance_images)}**"
        )

        preview_cols = st.columns(3)

        for i, image in enumerate(
            st.session_state.attendance_images
        ):

            with preview_cols[i % 3]:

                st.image(
                    image,
                    caption=f"Photo {i + 1}",
                    width="stretch"
                )


    # =====================================================
    # DONE
    # =====================================================

    st.divider()

    if st.button(
        "Done",
        type="primary",
        width="stretch"
    ):

        st.rerun()