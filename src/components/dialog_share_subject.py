import streamlit as st
import segno
import io


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):

    # =========================
    # DIALOG FONT COLOR
    # =========================

    st.markdown("""
        <style>

        /* Target the Streamlit dialog itself */
        section[data-testid="stDialog"] * {
            color: white !important;
        }

        div[data-testid="stDialog"] * {
            color: white !important;
        }

        /* Headings */
        section[data-testid="stDialog"] h1,
        section[data-testid="stDialog"] h2,
        section[data-testid="stDialog"] h3,
        section[data-testid="stDialog"] h4 {
            color: white !important;
        }

        /* Normal text */
        section[data-testid="stDialog"] p,
        section[data-testid="stDialog"] span,
        section[data-testid="stDialog"] label {
            color: white !important;
        }

        /* Code blocks */
        section[data-testid="stDialog"] code,
        section[data-testid="stDialog"] pre {
            color: white !important;
        }

        /* Alert / info box */
        section[data-testid="stDialog"] [data-testid="stAlert"] * {
            color: white !important;
        }

        /* Close button */
        section[data-testid="stDialog"] button {
            color: white !important;
        }

        </style>
    """, unsafe_allow_html=True)


    # =========================
    # CREATE JOIN URL
    # =========================

    app_domain = "http://localhost:8501"

    join_url = f"{app_domain}/?join-code={subject_code}"


    # =========================
    # HEADER
    # =========================

    st.header("Scan to Join")


    # =========================
    # GENERATE QR CODE
    # =========================

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(
        out,
        kind="png",
        scale=10,
        border=1
    )


    # =========================
    # TWO COLUMNS
    # =========================

    col1, col2 = st.columns(2)


    # =========================
    # COPY LINK
    # =========================

    with col1:

        st.markdown("### Copy Link")

        st.code(
            join_url,
            language="text"
        )

        st.code(
            subject_code,
            language="text"
        )

        st.info(
            "Copy this link to share on WhatsApp or Email"
        )


    # =========================
    # QR CODE
    # =========================

    with col2:

        st.markdown("### Scan to Join")

        st.image(
            out.getvalue(),
            caption="QRCODE for class joining"
        )