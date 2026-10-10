import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects
from src.components.subject_card import subject_card
from src.components.dialogue_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

def teacherscreen():
    style_background_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.subheader(f"Welcome, {teacher_data['name']}", text_alignment="center")
    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()

    with c2:
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=='take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendance'
            st.rerun()
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=='manage_subjects' else "tertiary"
        if st.button('Manage subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=='attendance_records'else "tertiary"
        if st.button('Attendance Records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendance_records'
            st.rerun()
    st.divider()
    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=="manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():

    teacher_id = st.session_state.teacher_data['teacher_id']

    # -----------------------------------------------------
    # INITIALIZE ATTENDANCE IMAGES
    # -----------------------------------------------------

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
        

    # -----------------------------------------------------
    # GET SUBJECTS
    # -----------------------------------------------------

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning(
            'You have not created any subjects yet. '
            'Please create one to begin!'
        )
        return

    # -----------------------------------------------------
    # SUBJECT OPTIONS
    # -----------------------------------------------------

    subject_options = {
        f"{s['name']}-{s['subject_code']}": s['subject_id']
        for s in subjects
    }

    col1, col2 = st.columns(2,vertical_alignment='bottom')

    # -----------------------------------------------------
    # SELECT SUBJECT
    # -----------------------------------------------------

    with col1:

        selected_subject_label = st.selectbox(
            'Select Subject',
            options=list(subject_options.keys())
        )

    # -----------------------------------------------------
    # ADD PHOTOS
    # -----------------------------------------------------

    with col2:

        if st.button(
            'Add Photos',
            type='primary',
            icon=':material/photo_prints:',
            width='stretch'
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[
        selected_subject_label
    ]

    # -----------------------------------------------------
    # DISPLAY ADDED PHOTOS
    # -----------------------------------------------------

    if st.session_state.attendance_images:

        st.divider()

        st.subheader(
            f"Added Photos "
            f"({len(st.session_state.attendance_images)})"
        )

        image_cols = st.columns(3)

        for i, image in enumerate(
            st.session_state.attendance_images
        ):

            with image_cols[i % 3]:

                st.image(
                    image,
                    caption=f"Photo {i + 1}",
                    width='stretch'
                )

        # -------------------------------------------------
        # CLEAR ALL PHOTOS
        # -------------------------------------------------

        if st.button(
            'Clear All Photos',
            type='tertiary',
            key='clear_attendance_photos'
        ):

            st.session_state.attendance_images = []
            st.session_state.attendance_image_ids = set()
            st.rerun()
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header('Manage subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # LIST ALL SUBJECTS
    subjects = get_teacher_subjects(teacher_id)

    if subjects:

        for sub in subjects:

            stats = [
                ("👥", "Students", sub['total_students']),
                ("📚", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(
                    f"Share Code: {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(
                        sub['name'],
                        sub['subject_code']
                    )

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")
def teacher_tab_attendance_records():
    st.header('Attendance Records')
def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False
def teacher_screen_login():
    style_background_dashboard()
    style_base_layout()

    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.header('Login using password',text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='thanush')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter password')
    st.divider()
    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("welcome back!",icon="")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")
    with btnc2:
        if st.button('Register Instead',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='register'
    footer_dashboard()
def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created! Login Now"

    except Exception as e:
        return False, f"Error: {e}"
def teacher_screen_register():
    style_background_dashboard()
    style_base_layout()

    c1,c2=st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.header('Register your teacher profile',text_alignment='center')
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder='thanush')
    teacher_name=st.text_input("Enter name",placeholder='thanush')
    teacher_pass=st.text_input("Enter password",type='password',placeholder='Enter password')
    teacher_pass_confirm=st.text_input("Confirm your password",type='password',placeholder='Enter password')
    st.divider()
    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button('Register now',icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button('Login Instead',type='primary',icon=':material/passkey:',width='stretch'):
            st.session_state.teacher_login_type='login'
    footer_dashboard()