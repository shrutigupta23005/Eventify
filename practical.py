import streamlit as st
import pandas as pd

# --- PRACTICAL EDUCATION DATA ---
PRACTICAL_EDUCATION_DATA = {
    "Activity": [
        "Art and Craft with Ornamental Design (2D and 3D)",
        "Art and Craft with Ornamental Design (Ropes)",
        "Art and Crafts with Fabric",
        "Craft and Design Methods",
        "Design for Commercially Profitable Project",
        "Digital Art Lab",
        "Fabric Construction in Textile",
        "Hand Embroidery",
        "Extension Programs for Women Empowerment",
        "FM Radio",
        "Informal Education",
        "Nutri Gardening and Post-Harvest Value Addition",
        "Jewellery Design",
        "Modernization of Ancient Art by Block Printing",
        "Photography Lab",
        "Soft Material Studies Lab",
        "Stencil Printing",
        "Surface Ornamentation",
        "Woven Design",
        "Yarn Craft",
        "Life Skills",
        "Social Intelligence and Conflict Resolution",
        "Personal Finance Advisory-I",
        "Personal Finance Advisory-II"
    ]
}

# Matching Venues (same length as activities)
PRACTICAL_EDUCATION_DATA["Venue"] = [
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Vani Mandir",
    "FM Radio, Vigyan Mandir",
    "Anopcharik Shiksha Kendra",
    "Department of Home Science (Gyan Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Room No. 108, Department of Design (Shilp Mandir)",
    "Department of Psychology (Vani Mandir)",
    "Department of Psychology (Vani Mandir)",
    "Department of Commerce and Management (Pragya Mandir)",
    "Department of Commerce and Management (Pragya Mandir)"
]


def practical_page():

    def go_back():
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.five_fold_page = None

    st.button("⬅ Back", on_click=go_back)

    st.markdown(
        """
        <h2 style='text-align:center; color:#00a0dc; margin-bottom:0;'>🎓 Five Fold Activity – Practical Education</h2>
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

    df = pd.DataFrame(PRACTICAL_EDUCATION_DATA).sort_values(by="Activity")

    # Header Row
    col1, col2 = st.columns([1.5, 2])

    col1.markdown("<b style='color:#00a0dc;'>Activity</b>", unsafe_allow_html=True)
    col2.markdown("<b style='color:#00a0dc;'>Venue</b>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Data Rows
    for _, row in df.iterrows():
        col1, col2 = st.columns([1.5, 2])

        col1.markdown(
            f"<span style='color:white;'>{row['Activity']}</span>",
            unsafe_allow_html=True
        )

        col2.markdown(
            f"<span style='color:white;'>{row['Venue']}</span>",
            unsafe_allow_html=True
        )
