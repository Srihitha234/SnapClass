import streamlit as st


def footer_home():

    logo_url = "https://tse3.mm.bing.net/th/id/OIP.dNUVNd3-JtROSjEKZlK_DQHaE8?r=0&pid=Api&h=220&P=0"

    st.html(f"""
        <div style="
            margin-top: 2rem;
            display: flex;
            gap: 6px;
            justify-content: center;
            align-items: center;
        ">

            <span style="
                font-family: 'Roboto', sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: white;
            ">
                Created with ❤️ by
            </span>

            <img
                src="{logo_url}"
                style="
                    height: 25px;
                    width: auto;
                    object-fit: contain;
                    display: block;
                "
            >

        </div>
    """)

def footer_dashboard():

    logo_url = "https://tse3.mm.bing.net/th/id/OIP.dNUVNd3-JtROSjEKZlK_DQHaE8?r=0&pid=Api&h=220&P=0"

    st.html(f"""
        <div style="
            margin-top: 2rem;
            display: flex;
            gap: 6px;
            justify-content: center;
            align-items: center;
        ">

            <span style="
                font-family: 'Roboto', sans-serif;
                font-size: 18px;
                font-weight: bold;
                color: black;
            ">
                Created with ❤️ by
            </span>

            <img
                src="{logo_url}"
                style="
                    height: 25px;
                    width: auto;
                    object-fit: contain;
                    display: block;
                "
            >

        </div>
    """)