import streamlit as st
import pandas as pd

# --- CRAFT COURSE DATA ---
CRAFT_COURSE_DATA = [
    ("Craft Certificate in Shibori (Tie & Dye)", "Certificate", "Textile Art", 1500, "Shilp Mandir, Room No. 108", 1, 1),
    ("Craft Certificate in Batik (Dyeing & Painting)", "Certificate", "Textile Art", 1500, "Shilp Mandir, Room No. 108", 1, 1),
    ("Craft Certificate in Surface Ornamentations", "Certificate", "Textile Design", 1500, "Shilp Mandir, Room No. 108", 1, 1),
    ("Craft Certificate in Block Printing", "Certificate", "Textile Printing", 1500, "Shilp Mandir, Room No. 108", 1, 1),
    ("Craft Certificate in Macrame & Knotting", "Certificate", "Handicraft", 1500, "Shilp Mandir, Room No. 108", 1, 1),
]

DISPLAY_DATA = [
    {
        "Course Name": item[0],
        "Fees (INR)": f"₹ {item[3]}",
        "Form Location": item[4],
        "Duration": "1 Year"
    }
    for item in CRAFT_COURSE_DATA
]


def craft_page():

    
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #ffffff50 !important;
            border-radius: 8px !important;
        }
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        div.row-widget.stHorizontal {
            margin-bottom: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    def go_back():
        st.session_state.certificate = "Certificate & Diploma Courses"
        st.session_state.certificate_page = None
        st.session_state.certificate_active = False

    col1, col2 = st.columns([1, 9])
    with col1:
        st.button("⬅ Back", on_click=go_back)

    with col2:
        st.markdown(
    "<h2 style='text-align:center; color:#00a0dc;'>🧵 Certificate & Diploma Courses – Art & Craft</h2>",
    unsafe_allow_html=True
)

    st.markdown(
        """
        <h4 style='text-align:center; color:#ffffff; margin-top:0;'>Session 2025-26</h4>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown(
        """
        <div style='background-color: rgba(255, 75, 75, 0.15); border: 1px solid #ff4b4b; border-radius: 8px; padding: 12px; text-align: center; margin: 10px 0 20px 0;'>
            <span style='color: #ff4b4b; font-weight: bold;'></span> 
            <span style='color: white;'>Admission forms for the current session were <b>closed in August</b>.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    df = pd.DataFrame(DISPLAY_DATA).sort_values(by="Course Name")

    
    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])

    col1.markdown("<b style='color:#00a0dc;'>Course Name</b>", unsafe_allow_html=True)
    col2.markdown("<b style='color:#00a0dc;'>Fees (INR)</b>", unsafe_allow_html=True)
    col3.markdown("<b style='color:#00a0dc;'>Form Location</b>", unsafe_allow_html=True)
    col4.markdown("<b style='color:#00a0dc;'>Duration</b>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    
    for _, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1, 2, 1])

        col1.markdown(f"<span style='color:white;'>{row['Course Name']}</span>", unsafe_allow_html=True)
        col2.markdown(f"<span style='color:white;'>{row['Fees (INR)']}</span>", unsafe_allow_html=True)
        col3.markdown(f"<span style='color:white;'>{row['Form Location']}</span>", unsafe_allow_html=True)
        col4.markdown(f"<span style='color:white;'>{row['Duration']}</span>", unsafe_allow_html=True)