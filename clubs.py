import streamlit as st
import pandas as pd
import mysql.connector
import os
import dotenv
dotenv.load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "university_chatbot")
    )

def show_clubs_page():

    def go_back():
        st.session_state.clubs = "Clubs"
        st.session_state.user_sub_page = "chat"

    col1, col2 = st.columns([1, 9])
    with col1:
        st.button("⬅ Back", on_click=go_back)

    st.markdown(
        "<h2 style='text-align:center; color:#00a0dc;'>🏛️ University Clubs</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")

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

    try:
        conn = get_connection()
        query = """
            SELECT 
                club_name AS 'Club Name',
                club_type AS 'Type',
                category AS 'Category',
                contact_person AS 'Contact Person',
                contact_number AS 'Contact',
                venue AS 'Venue',
                social_link AS 'Social Links'
            FROM clubs 
            ORDER BY club_name
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            st.warning("No clubs found in database.")
            return

        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1, 1, 1.5, 1, 1.5, 1.5])

        col1.markdown("<b style='color:#00a0dc;'>Club Name</b>", unsafe_allow_html=True)
        col2.markdown("<b style='color:#00a0dc;'>Type</b>", unsafe_allow_html=True)
        col3.markdown("<b style='color:#00a0dc;'>Category</b>", unsafe_allow_html=True)
        col4.markdown("<b style='color:#00a0dc;'>Contact Person</b>", unsafe_allow_html=True)
        col5.markdown("<b style='color:#00a0dc;'>Contact</b>", unsafe_allow_html=True)
        col6.markdown("<b style='color:#00a0dc;'>Venue</b>", unsafe_allow_html=True)
        col7.markdown("<b style='color:#00a0dc;'>Social Links</b>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

        for _, row in df.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1.5, 1, 1, 1.5, 1, 1.5, 1.5])

            col1.markdown(f"<span style='color:white;'>{row['Club Name']}</span>", unsafe_allow_html=True)
            col2.markdown(f"<span style='color:white;'>{row['Type']}</span>", unsafe_allow_html=True)
            col3.markdown(f"<span style='color:white;'>{row['Category']}</span>", unsafe_allow_html=True)
            col4.markdown(f"<span style='color:white;'>{row['Contact Person']}</span>", unsafe_allow_html=True)
            col5.markdown(f"<span style='color:white;'>{row['Contact']}</span>", unsafe_allow_html=True)
            col6.markdown(f"<span style='color:white;'>{row['Venue']}</span>", unsafe_allow_html=True)
            
            social_link = row['Social Links'] if pd.notna(row['Social Links']) and row['Social Links'] != "" else "N/A"
            if social_link != "N/A":
                col7.markdown(f"<a href='{social_link}' target='_blank' style='color:#00a0dc; text-decoration:underline;'>Link</a>", unsafe_allow_html=True)
            else:
                col7.markdown("<span style='color:#888888;'>N/A</span>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Database Error: {e}")
