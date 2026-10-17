import streamlit as st

from src.screens.homescreen import homescreen
from src.screens.teacherscreen import teacherscreen
from src.screens.studentscreen import studentscreen
from src.components.dialog_auto_enroll import auto_enroll_dialog
def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type']=None
    
    match st.session_state['login_type']:
        case 'teacher':
            teacherscreen()

        case 'student':
            studentscreen()

        case None:
            homescreen()
    join_code=st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type!='student':
            st.session_state.login_type='student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')== 'student':
            auto_enroll_dialog(join_code)
    
main()