import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.components.footer import footer_home

def homescreen():

    header_home()

    style_base_layout()
    style_background_home()

    col1, col2 = st.columns(2,gap="large")

    with col1:
        st.header("I'm a Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png",width=145)
        if st.button("Student Portal",type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2:
        st.header("I'm a Teacher")
        st.image("https://i.ibb.co/844D9Lrt/mascot-teacher.png",width=145)
        if st.button("Teacher Portal",type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state["login_type"] = "teacher"
            st.rerun()
    footer_home()