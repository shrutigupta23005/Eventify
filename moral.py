import streamlit as st
import pandas as pd

# --- MORAL EDUCATION DATA ---
MORAL_EDUCATION_DATA = {
    "Activity": ["Banasthali Campus Ethics"],
    "Requirement": ["Compliance of Vidyapith Rules and Wearing of Khadi"],
    "Focus Areas": [
        "Discipline, Participation in National and Cultural Festivals, "
        "Participation in Various Activities of the Vidyapith, "
        "Social Behavior, etc."
    ]
}


def moral_page():

    def go_back():
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.five_fold_page = None

    st.button("⬅ Back", on_click=go_back)

    st.markdown(
        """
        <h2 style='text-align:center; color:#00a0dc; margin-bottom:0;'>👩🏻‍🏫 Five Fold Activity – Moral Education</h2>
        <h4 style='text-align:center; color:#ffffff; margin-top:0;'>Session 2025-2026</h4>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Reduce extra spacing
    st.markdown("""
        <style>
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        div.row-widget.stHorizontal {
            margin-bottom: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(MORAL_EDUCATION_DATA)

    # Header Row
    col1, col2, col3 = st.columns([1, 1.2, 2])

    col1.markdown("<b style='color:#00a0dc;'>Activity</b>", unsafe_allow_html=True)
    col2.markdown("<b style='color:#00a0dc;'>Requirement</b>", unsafe_allow_html=True)
    col3.markdown("<b style='color:#00a0dc;'>Focus Areas</b>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Data Rows
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([1, 1.2, 2])

        col1.markdown(
            f"<span style='color:white;'>{row['Activity']}</span>",
            unsafe_allow_html=True
        )

        col2.markdown(
            f"<span style='color:white;'>{row['Requirement']}</span>",
            unsafe_allow_html=True
        )

        col3.markdown(
            f"<span style='color:white;'>{row['Focus Areas']}</span>",
            unsafe_allow_html=True
        )
