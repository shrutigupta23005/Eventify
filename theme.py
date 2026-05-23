import streamlit as st

def apply_os_theme_css(bg1="", bg2=""):
    """
    Call once after set_page_config().
    Automatically switches dark/light based on the user's OS theme.
    No toggles, no session state, no Python logic needed.
    """
    st.markdown(f"""
<style>

/* ═══════════════════════════════════════
   DARK MODE  (default — your original look)
═══════════════════════════════════════ */

header[data-testid="stHeader"] {{ background-color: transparent !important; }}

.stApp {{
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
    position: relative;
}}

.stApp::after {{
    content: "";
    position: fixed; inset: 0; z-index: 0;
    background-size: cover; background-position: center; background-repeat: no-repeat;
    animation: slideShow 16s infinite; animation-timing-function: ease-in-out;
}}

@keyframes slideShow {{
    0%   {{ background-image: url("data:image/jpg;base64,{bg1}"); opacity: 1; }}
    40%  {{ background-image: url("data:image/jpg;base64,{bg1}"); opacity: 1; }}
    48%  {{ background-image: url("data:image/jpg;base64,{bg1}"); opacity: 0; }}
    50%  {{ background-image: url("data:image/jpg;base64,{bg2}"); opacity: 0; }}
    58%  {{ background-image: url("data:image/jpg;base64,{bg2}"); opacity: 1; }}
    90%  {{ background-image: url("data:image/jpg;base64,{bg2}"); opacity: 1; }}
    98%  {{ background-image: url("data:image/jpg;base64,{bg2}"); opacity: 0; }}
    100% {{ background-image: url("data:image/jpg;base64,{bg1}"); opacity: 0; }}
}}

.stApp::before {{
    content: ""; position: fixed; inset: 0;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    background: rgba(0,0,0,0.50); z-index: 1;
}}

.stApp > * {{ position: relative; z-index: 2; }}

section[data-testid="stSidebar"] {{ background-color: #1E2530 !important; }}
section[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}

.stMarkdown, p, label, span, div, h1, h2, h3, h4, h5 {{ color: #FFFFFF !important; }}

div[data-baseweb="select"] > div, div[data-baseweb="select"] span, div[data-baseweb="popover"] li {{
    background-color: #1E2530 !important; color: #FFFFFF !important;
}}

.logo-container {{
    display: flex; justify-content: center; font-size: 40px; font-weight: 800;
    color: #00A0DC !important; margin-top: 10px; margin-bottom: 30px; font-family: 'Inter', sans-serif;
}}

.stTextInput div[data-baseweb="input"] {{
    background-color: transparent !important; border: 2px solid #2D5A5C !important;
    border-radius: 12px !important; padding-right: 4px !important;
}}
.stTextInput input {{ color: #FFFFFF !important; background-color: transparent !important; }}
button[data-testid="stTextInputPasswordToggle"] {{
    margin-right: 0px !important; padding: 0px !important;
    background-color: transparent !important; border: none !important;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: #FFFFFF !important; border-width: 3px !important; border-style: solid !important;
    border-radius: 16px !important; padding: 30px !important; background-color: #1E2530 !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"] * {{ color: #FFFFFF !important; }}

div.stButton > button {{
    background-color: #006699 !important; color: #FFFFFF !important;
    border-radius: 12px !important; border: none !important; width: 100% !important;
    height: 50px !important; font-size: 18px !important; font-weight: 700 !important;
    transition: all 0.3s ease-in-out !important;
}}
div.stButton > button:hover {{
    background-color: #0088cc !important; box-shadow: 0px 4px 15px rgba(0,160,220,0.4) !important;
    transform: translateY(-2px) !important;
}}

div.stButton:has(> button[key="btn_forgot"]) > button,
div.stButton:has(> button[key="btn_signup"]) > button,
div.stButton:has(> button[key="btn_login_switch"]) > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    color: #aaaaaa !important; text-decoration: underline !important;
    font-size: 14px !important; font-weight: 400 !important; height: auto !important;
    min-height: unset !important; padding: 4px 0px !important; width: auto !important; transform: none !important;
}}
div.stButton:has(> button[key="btn_forgot"]) > button:hover,
div.stButton:has(> button[key="btn_signup"]) > button:hover,
div.stButton:has(> button[key="btn_login_switch"]) > button:hover {{
    color: #00A0DC !important; background: transparent !important;
    box-shadow: none !important; transform: none !important;
}}

div[data-testid="metric-container"] {{
    background-color: #1E2530 !important; border: 1px solid #2D5A5C !important;
    border-radius: 12px !important; padding: 10px !important;
}}
div[data-testid="metric-container"] * {{ color: #FFFFFF !important; }}

.stDataFrame {{ background-color: #1E2530 !important; }}
.stDataFrame * {{ color: #FFFFFF !important; }}

.chat-bubble {{ padding: 12px 16px; border-radius: 16px; margin: 8px 0; max-width: 80%; font-size: 15px; }}
.user-bubble {{ background-color: #1a472a !important; margin-left: auto; color: #FFFFFF !important; }}
.user-bubble * {{ color: #FFFFFF !important; }}
.bot-bubble {{ background-color: #1E2530 !important; border: 1px solid #2D5A5C; color: #FFFFFF !important; }}
.bot-bubble * {{ color: #FFFFFF !important; }}

hr {{ border-color: #2D5A5C !important; }}

div[data-testid="stAlert"] {{ background-color: #1E2530 !important; }}
div[data-testid="stAlert"] * {{ color: #FFFFFF !important; }}

div[data-baseweb="calendar"] *, div[data-baseweb="datepicker"] * {{
    color: #FFFFFF !important; background-color: #1E2530 !important;
}}

div[data-testid="stModal"] > div, div[role="dialog"] {{ background-color: #1E2530 !important; }}
div[role="dialog"] * {{ color: #FFFFFF !important; }}

div.element-container:has(.floating-auth-btn) + div.element-container {{
    position: fixed !important; top: 65px !important; right: 25px !important; z-index: 99999 !important; width: auto !important;
}}
div.element-container:has(.floating-auth-btn) + div.element-container button {{
    background-color: transparent !important; color: #00A0DC !important; border: none !important;
    box-shadow: none !important; font-size: 16px !important; font-weight: 600 !important;
    padding: 0px !important; height: auto !important; width: auto !important;
}}
div.element-container:has(.floating-auth-btn) + div.element-container button:hover {{
    color: #0088cc !important; text-decoration: underline !important;
    transform: none !important; background-color: transparent !important;
}}

div.element-container:has(.top-right-logout) + div.element-container {{
    position: fixed !important; top: 65px !important; right: 25px !important; z-index: 99999 !important; width: auto !important;
}}
div.element-container:has(.top-right-logout) + div.element-container button {{
    background-color: transparent !important; color: #000000 !important; border: none !important;
    box-shadow: none !important; font-size: 16px !important; font-weight: 700 !important;
    text-decoration: underline !important; padding: 0px !important; height: auto !important;
    min-height: 0px !important; width: auto !important; transition: all 0.3s ease !important;
}}
div.element-container:has(.top-right-logout) + div.element-container button:hover {{
    color: #FFFFFF !important; transform: scale(1.05) !important; background-color: transparent !important;
}}

div.element-container:has(.floating-back-btn) + div.element-container {{
    position: fixed !important; top: 65px !important; left: 20px !important; z-index: 99999 !important; width: auto !important;
}}
div.element-container:has(.floating-back-btn) + div.element-container button {{
    background-color: transparent !important; color: #00A0DC !important;
    border: 2px solid #00A0DC !important; border-radius: 50px !important;
    padding: 5px 20px !important; font-weight: 700 !important; height: auto !important; width: auto !important;
}}
div.element-container:has(.floating-back-btn) + div.element-container button:hover {{
    background-color: #00A0DC !important; color: white !important; transform: scale(1.05) !important;
}}

div.element-container:has(.popup-link-btn) + div.element-container button {{
    background-color: transparent !important; color: #00A0DC !important;
    border: 2px solid #00A0DC !important; border-radius: 8px !important; box-shadow: none !important;
    font-size: 16px !important; font-weight: 700 !important; padding: 8px 15px !important;
    height: auto !important; min-height: 0px !important; width: 100% !important;
    margin: 0 auto !important; display: block !important; transition: all 0.3s ease !important;
}}
div.element-container:has(.popup-link-btn) + div.element-container button:hover {{
    color: #FFFFFF !important; background-color: #00A0DC !important; transform: scale(1.02) !important;
}}



.stApp, .stApp * {{ cursor: pointer !important; }}
input[type="text"], input[type="password"], textarea {{ cursor: text !important; }}
div[data-baseweb="select"] input {{ cursor: pointer !important; }}


/* ═══════════════════════════════════════
   LIGHT MODE — auto when OS is light
   White background, black text
═══════════════════════════════════════ */

@media (prefers-color-scheme: light) {{

    .stApp {{
        background-color: #F5F5F5 !important;
        color: #0E1117 !important;
    }}

    .stApp::before {{ background: rgba(255,255,255,0.45) !important; backdrop-filter: blur(4px) !important; -webkit-backdrop-filter: blur(4px) !important; }}

    section[data-testid="stSidebar"] {{ background-color: #FFFFFF !important; }}
    section[data-testid="stSidebar"] * {{ color: #0E1117 !important; }}

    body, .stApp, .stApp *,
    .stMarkdown, .stMarkdown *,
    p, label, span, h1, h2, h3, h4, h5,
    div[data-testid="stText"],
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] * {{
        color: #0E1117 !important;
    }}

    div[data-baseweb="select"] > div, div[data-baseweb="select"] span, div[data-baseweb="popover"] li {{
        background-color: #FFFFFF !important; color: #0E1117 !important;
    }}

    .logo-container {{ color: #006699 !important; }}

    .stTextInput div[data-baseweb="input"] {{
        background-color: #FFFFFF !important; border: 2px solid #2D5A5C !important;
    }}
    .stTextInput input {{ color: #0E1117 !important; background-color: #FFFFFF !important; }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: #2D5A5C !important; background-color: #FFFFFF !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] * {{ color: #0E1117 !important; }}

    /* all blue buttons keep white text in light mode */
    div.stButton > button {{ color: #FFFFFF !important; }}
    div.stButton > button * {{ color: #FFFFFF !important; }}
    div.stButton > button p {{ color: #FFFFFF !important; }}

    div.stButton:has(> button[key="btn_forgot"]) > button,
    div.stButton:has(> button[key="btn_signup"]) > button,
    div.stButton:has(> button[key="btn_login_switch"]) > button {{ color: #004488 !important; }}
    div.stButton:has(> button[key="btn_forgot"]) > button:hover,
    div.stButton:has(> button[key="btn_signup"]) > button:hover,
    div.stButton:has(> button[key="btn_login_switch"]) > button:hover {{ color: #006699 !important; }}

    div[data-testid="metric-container"] {{ background-color: #FFFFFF !important; }}
    div[data-testid="metric-container"] * {{ color: #0E1117 !important; }}

    .stDataFrame {{ background-color: #FFFFFF !important; }}
    .stDataFrame * {{ color: #0E1117 !important; }}

    .user-bubble {{ background-color: #C8E6C9 !important; color: #0E1117 !important; }}
    .user-bubble * {{ color: #0E1117 !important; }}
    .bot-bubble {{ background-color: #FFFFFF !important; border: 1px solid #2D5A5C; color: #0E1117 !important; }}
    .bot-bubble * {{ color: #0E1117 !important; }}

    hr {{ border-color: #CCCCCC !important; }}

    div[data-testid="stAlert"] {{ background-color: #FFFFFF !important; }}
    div[data-testid="stAlert"] * {{ color: #0E1117 !important; }}

    div[data-baseweb="calendar"] *, div[data-baseweb="datepicker"] * {{
        color: #0E1117 !important; background-color: #FFFFFF !important;
    }}

    div[data-testid="stModal"] > div, div[role="dialog"] {{ background-color: #FFFFFF !important; }}
    div[role="dialog"] * {{ color: #0E1117 !important; }}

    div.element-container:has(.floating-auth-btn) + div.element-container button {{ color: #0E1117 !important; }}
    div.element-container:has(.floating-auth-btn) + div.element-container button * {{ color: #0E1117 !important; }}
    div.element-container:has(.top-right-logout) + div.element-container button,
    div.element-container:has(.top-right-logout) + div.element-container button *,
    div.element-container:has(.top-right-logout) + div.element-container button p {{ color: #000000 !important; }}
    div.element-container:has(.top-right-logout) + div.element-container button:hover,
    div.element-container:has(.top-right-logout) + div.element-container button:hover * {{ color: #000000 !important; }}
    div.element-container:has(.floating-back-btn) + div.element-container button {{
        color: #006699 !important; border-color: #006699 !important;
    }}
    div.element-container:has(.floating-back-btn) + div.element-container button:hover {{
        background-color: #006699 !important; color: white !important;
    }}
    div.element-container:has(.popup-link-btn) + div.element-container button {{
        color: #006699 !important; border-color: #006699 !important;
    }}
    div.element-container:has(.popup-link-btn) + div.element-container button:hover {{
        background-color: #006699 !important; color: #FFFFFF !important;
    }}
}}

</style>
""", unsafe_allow_html=True)