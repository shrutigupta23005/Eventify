import streamlit as st
import pandas as pd

# --- MEDIA COURSE DATA ---
MEDIA_COURSE_DATA = [
    ("Certificate in Radio Production - RJing & Anchoring", "Certificate", "Media & Communication", 7000, "Vigyan Mandir (FM Radio Office)", 1, 1),
    ("Diploma in Audio Engineering", "Diploma", "Sound Technology", 7000, "Vigyan Mandir (FM Radio Office)", 1, 1),
    ("Diploma in Broadcast Journalism (Radio)", "Diploma", "Media Studies", 7000, "Vigyan Mandir (FM Radio Office)", 1, 1),
    ("Diploma in Advertising and Public Relations", "Diploma", "Communication Studies", 7000, "Vigyan Mandir (FM Radio Office)", 1, 1),
]

DISPLAY_DATA = [
    {
        "Course Name": item[0],
        "Fees (INR)": f"₹ {item[3]}",
        "Form Location": item[4]
    }
    for item in MEDIA_COURSE_DATA
]


def massmedia_page():

    # Back button + spacing style
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

    st.markdown(
        "<h2 style='text-align:center; color:#00a0dc;'>🎙️ Certificate & Diploma Courses – Media & Communication</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    df = pd.DataFrame(DISPLAY_DATA).sort_values(by="Course Name")

    # Header Row
    col1, col2, col3 = st.columns([2, 1, 2])

    col1.markdown("<b style='color:#00a0dc;'>Course Name</b>", unsafe_allow_html=True)
    col2.markdown("<b style='color:#00a0dc;'>Fees (INR)</b>", unsafe_allow_html=True)
    col3.markdown("<b style='color:#00a0dc;'>Form Location</b>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

    # Data Rows
    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([2, 1, 2])

        col1.markdown(
            f"<span style='color:white;'>{row['Course Name']}</span>",
            unsafe_allow_html=True
        )

        col2.markdown(
            f"<span style='color:white;'>{row['Fees (INR)']}</span>",
            unsafe_allow_html=True
        )

        col3.markdown(
            f"<span style='color:white;'>{row['Form Location']}</span>",
            unsafe_allow_html=True
        )
