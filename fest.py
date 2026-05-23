import streamlit as st
import pandas as pd

# --- FESTS DATA ---
FESTS_DATA = {
    "Fest Name": [
        "Adhyaay",
        "Mayukh",
        "Xeron",
        "Navotkash 2n0",
        "Cosmos",
        "Janus",
        "HUE",
        "Karvaan"
    ],
    "Category": [
        "Education, Economics, Journalism & Mass Communication, Languages, History & Indian Culture, Performing Arts, Political Science, Psychology, Sanskrit & Vedic Studies, Sociology, Design, Visual Arts, Architecture & Planning",
        "Computer Science, Automation, Mathematics & Statistics, Physical Sciences",
        "Chemical Engineering & Chemistry",
        "Legal Studies, Commerce & Management",
        "Earth Sciences",
        "Bioscience & Biotechnology, Pharmacy",
        "Home Science",
        "Journalism & Mass Communication"
    ],
    "Venue": [
        "Wisdom Pandal",
        "Surya Mandir",
        "Gyan Mandir",
        "Wisdom Pandal",
        "Wisdom Pandal",
        "Wisdom Pandal",
        "Gyan Mandir",
        "To be announced"
    ]
}

# --- CREATE DATAFRAME ---
df = pd.DataFrame(FESTS_DATA)

# --- SORT DATA ALPHABETICALLY BY FEST NAME ---
df_sorted = df.sort_values(by="Fest Name", ascending=True)

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="Eventify - Fests", layout="centered")

# --- MAIN CONTENT ---
st.markdown(
    "<h2 style='text-align:center; color:#00a0dc; font-size:30px;'>🎉 University Fests</h2>",
    unsafe_allow_html=True
)
st.markdown("---")

st.markdown("### Fest Details")
st.dataframe(df_sorted, hide_index=True, use_container_width=True)

# --- CUSTOM DARK THEME CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #00a0dc;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #00a0dc !important;
        text-align: center;
    }
    .stDataFrame .data-grid-header, .stDataFrame .data-grid-header th {
        background-color: #262730 !important;
        color: #ffffff !important;
        border-bottom: 2px solid #00a0dc !important;
    }
    .stDataFrame, .stDataFrame table, .stDataFrame .data-cell {
        background-color: #1a1a1a !important;
        color: #00a0dc !important;
        border: none !important;
    }
    .stDataFrame table tbody tr:nth-child(even) .data-cell {
        background-color: #0c0c0c !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
