import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None
):

    with st.container(border=True):

        # Keep the title area the same height
        # for every subject
        st.markdown(
            f"""
            <div style="
                height: 65px;
                display: flex;
                align-items: flex-start;
            ">
                <h3 style="
                    margin: 0;
                    padding: 0;
                    font-family: 'Roboto', sans-serif;
                    font-size: 1.6rem;
                    line-height: 1.2;
                    color: black;
                ">
                    {name}
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # IMPORTANT:
        # Use normal Streamlit for this.
        st.write(
            f"Code: `{code}` | Section: {section}"
        )

        # Statistics
        if stats:

            cols = st.columns(len(stats))

            for col, (icon, label, value) in zip(cols, stats):

                with col:

                    st.markdown(
                        f"### {icon} {value}"
                    )

                    st.markdown(
                        f"**{label}**"
                    )

        # Footer button
        if footer_callback:
            footer_callback()