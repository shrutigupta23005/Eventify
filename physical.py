import streamlit as st
import pandas as pd

PHYSICAL_EDUCATION_DATA = {
    "Activity": [
        "Aerobics", "Archery", "Athletics", "Badminton", "Basketball",
        "Cricket", "Equestrian", "Handball", "Hockey", "Martial Arts",
        "Tennis", "Kho-Kho", "Net Ball", "Rope Mallakhamb", "Shooting",
        "Soft Ball", "Football", "Gymnastics", "Swimming", "Table Tennis",
        "Kabaddi", "Throwball", "Volleyball", "Weight Training", "Yoga",
        "Combative Sports", "Pole Mallakhamb", "Squash",
        "Banasthali Sewa Dal (BSD)", "National Service Scheme (NSS)",
        "National Cadet Corps (NCC)"
    ],
    "Venue": [
        "Aerobics Hall (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Athletics Track (6:00–8:00 AM / 5:00–8:00 PM)",
        "Badminton Hall (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Gymnasium",
        "Swimming Pool",
        "Table Tennis Hall",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Gymnasium",
        "Yoga Hall",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "Vidula Maidan (6:00–8:00 AM / 5:00–8:00 PM)",
        "In front of Vani Mandir (5:00–7:00 PM)",
        "NSS Office, Vidya Mandir",
        "Selected Students",
        "Parade Ground"
    ]
}


def physical_page():

    def go_back():
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.five_fold_page = None

    st.button("⬅ Back", on_click=go_back)

    st.markdown(
        """
        <h2 style='text-align:center; color:#00a0dc; margin-bottom:0;'>🏃🏻‍♀️ Five Fold Activity – Physical Education</h2>
        <h4 style='text-align:center; color:#ffffff; margin-top:0;'>Session 2025-2026</h4>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Remove extra spacing globally
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

    df = pd.DataFrame(PHYSICAL_EDUCATION_DATA).sort_values(by="Activity")

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
