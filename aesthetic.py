import streamlit as st
import pandas as pd

# --- AESTHETIC EDUCATION DATA ---
AESTHETIC_EDUCATION_DATA = {
    "Activity": [
        "Classical Dance (Bharatanatyam / Kathak / Manipuri)",
        "Folk Dance",
        "Creative Art",
        "Music – Instrumental (Guitar / Orchestra / Sarod / Sitar / Tabla / Violin)",
        "Music – Vocal",
        "Theatre",
        "Banasthali Band"
    ],
    "Venue": [
        "Dance Centre",
        "Dance Centre",
        "Kala Mandir / Shilp Mandir",
        "Sur Mandir (4:00 PM – 6:00 PM)",
        "Sur Mandir (4:00 PM – 6:00 PM)",
        "Sur Mandir (4:00 PM – 6:00 PM)",
        "Sur Mandir (4:00 PM – 6:00 PM)"
    ]
}


def aesthetic_page():

    def go_back():
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.five_fold_page = None

    st.button("⬅ Back", on_click=go_back)

    st.markdown(
        """
        <h2 style='text-align:center; color:#00a0dc; margin-bottom:0;'>💃🏻🎶🎨 Five Fold Activity – Aesthetic Education</h2>
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

    df = pd.DataFrame(AESTHETIC_EDUCATION_DATA).sort_values(by="Activity")

    # Header Row
    col1, col2 = st.columns([1, 2])
    col1.markdown("<b style='color:#00a0dc;'>Activity</b>", unsafe_allow_html=True)
    col2.markdown("<b style='color:#00a0dc;'>Venue</b>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Data Rows
    for _, row in df.iterrows():
        col1, col2 = st.columns([1, 2])

        col1.markdown(
            f"<span style='color:white;'>{row['Activity']}</span>",
            unsafe_allow_html=True
        )

        col2.markdown(
            f"<span style='color:white;'>{row['Venue']}</span>",
            unsafe_allow_html=True
        )
