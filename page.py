import streamlit as st
import dotenv
dotenv.load_dotenv()
import mysql.connector
import random
import smtplib
import re
import pandas as pd
import speech_recognition as sr
from email.mime.text import MIMEText
from datetime import date
import datetime
import os
import json
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval
import base64
import difflib
import uuid
from groq import Groq

# Attempt to import OpenCV and Numpy for QR Code auto-scanning magic
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

import aesthetic
import physical
import practical
import moral
from clubs import show_clubs_page
import languagecd
import craft
import dance
import music
import tech
import massmedia

def get_base64_image(folder_name, file_base_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
        absolute_path = os.path.join(script_dir, folder_name, file_base_name + ext)
        try:
            with open(absolute_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except FileNotFoundError:
            continue
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

bg1 = get_base64_image("background", "cai")
bg2 = get_base64_image("background", "ai")
bg3 = get_base64_image("background", "class")
bg4 = get_base64_image("background", "rep")
bg5 = get_base64_image("background", "rep1")
bg6 = get_base64_image("background", "ori")

def load_intents():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "intents.json")
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"intents": []}

INTENTS = load_intents()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
try:
    from groq import Groq
    _groq_client = Groq(api_key=GROQ_API_KEY)
except ImportError:
    _groq_client = None
    pass

UNIVERSITY_CONTEXT = """
You are Eventify Bot, a university information chatbot and the strictly professional, official AI assistant for Banasthali Vidyapith University. Your goal is to help students find information about clubs and university fests. Always try to find the closest possible answer.

CRITICAL RULES:
1. DEFAULT LANGUAGE IS ENGLISH: You MUST reply in English by default.
   - ONLY IF the user explicitly requests you to speak in Hindi/Hinglish, you may reply in Hindi/Hinglish.
   - If the user speaks in English, strictly reply in English.
   - Do not automatically transition to Hindi or Hinglish just because the context contains Indian university names or terms.
2. TIME & LOGIC PROTOCOL: The database records below are tagged by the system as [PAST], [TODAY], [UPCOMING], or [EXPIRED]. 
   - If a user asks for "upcoming", "next", or "latest" events, you MUST ONLY provide events tagged as [UPCOMING] or [TODAY]. You are strictly forbidden from showing [PAST] events for these queries.
   - If a user asks for active forms, ONLY show forms tagged [ACTIVE].
3. CLUBS & FESTS INFORMATION PROVISION:
   - You answer ONLY from the university clubs and fests database and context provided.
   - Always answer in clear sentences. Do not say "I don't have information" if the information exists in the database.
   - When asked about a club, you must provide information about club name, type (official/non-official), category, contact person, phone number, email, venue, and description. 
   - When asked about a fest, provide information about their departments, venues, and activities.
   - If a user asks about contact, provide phone or email.
   - If a user asks about venue, provide venue.
   - If a user asks about category, provide category.
   - If a user asks about coordinator, provide contact person.
   - If a user asks "tell me about [club/fest]", provide full details.
   - If a user asks for a list (technical clubs, dance clubs, fests), map, fivefold activities, or a Certificate & Diploma Courses, provide a list of names.
4. ZERO HALLUCINATION & EXACT MATCHING: You must ONLY use the exact data provided in the database records below. DO NOT invent information.
5. FIVE-FOLD FORMS: State clearly that physical forms are collected IN-PERSON from the respective departments. THEY ARE NOT AVAILABLE ONLINE.
6. DIRECTIONS & MAPS: If a user asks "Where is [Location]", provide the textual location AND explicitly add: "For live GPS navigation, please select [Location] from the 'Search Maps' dropdown menu in the left sidebar."
7. VOICE-TO-TEXT TOLERANCE: The user may be using voice typing, which often mishears Hindi department names (e.g., "Bedula Madan" -> Vidula Maidan, "Mayo" -> Mayukh). Map them intelligently.
8. EVENT REGISTRATION RULES:
   - If a user asks about "How to register", "Registration process", "Event registration", "Escape Room registration", "Where to register", or "Participation form" (including for specific events), ALWAYS redirect them by stating: "To register for this event, please go to the Forms and Links section on the university portal and fill out the Event Registration Form."
   - Do NOT say "I don't have information" for these queries, even if the exact event or form link is not in the database.
9. MISSING INFORMATION FALLBACK:
   - For all other questions, if the answer is NOT in the database or text below, you MUST say: "I apologize, but I do not have that specific information in my database. Please contact the university administration."
10. ANSWER LENGTH & DIRECTNESS:
   - Keep your generic answers short and helpful.
   - If the user asks a one-word or very short question, give a very short answer.
   - If the user asks a full sentence question, give a medium answer.
   - ONLY give detailed, elaborate information when the user explicitly asks to "explain", "tell me about", or "tell me in detail".

=== FESTS & SPECIAL EVENTS ===
Adhyay: Education, Economics, Journalism, English, Hindi, History, Performing Arts, Political Science, Psychology, Design. Venue: Wisdom Pandal.
Mayukh: Computer Science, Automation, Mathematics, Physical Sciences. Venue: Surya Mandir. Features numerous technical events. A major cultural, technical, and talent festival showcasing student performances and creativity.
Xeron: Chemical Engineering, Chemistry.
HUE: Home Science. Venue: Gyan Mandir.
Navotkash: Legal Studies, Commerce, Management.
Cosmos: General university fest featuring spectacular cultural events, music, dance, and art.
Janus: This is the fest of BioTechnology of the department of banasthali vidyapith.
Convocation: The annual grand graduation ceremony where degrees are awarded to students. Usually held in late Winter or Spring.

=== FIVE-FOLD EDUCATION ===
Physical: Aerobics, Archery, Athletics, Badminton, Basketball, Cricket, Equestrian, Handball, Hockey, Martial Arts, Tennis, Kho-Kho, Net Ball, Rope Mallakhamb, Shooting, Soft Ball, Football, Gymnastics, Swimming, Table Tennis, Kabaddi, Throwball, Volleyball, Weight Training, Yoga, Combative Sports, Pole Mallakhamb, Squash, BSD, NSS, NCC. Timing: 6-8 AM / 5-8 PM at Vidula Maidan (most sports), Swimming Pool, Gymnasium, Badminton Hall, Yoga Hall.
Aesthetic: Classical Dance (Bharatanatyam/Kathak/Manipuri) at Dance Centre; Folk Dance at Dance Centre; Creative Art at Kala Mandir/Shilp Mandir; Music (Guitar/Sarod/Sitar/Tabla/Violin/Vocal) at Sur Mandir 4-6 PM; Theatre & Banasthali Band at Sur Mandir.
Practical: Art & Craft, FM Radio, Extension Programs, Photography Lab, Life Skills, Personal Finance Advisory, Social Intelligence — Shilp Mandir Room 108, Vani Mandir, Vigyan Mandir.
Moral: Banasthali Campus Ethics — Compliance of Vidyapith Rules, wearing Khadi, discipline, cultural festivals, social behavior.
Service & Leadership: BSD (Banasthali Seva Dal), NSS, NCC.

=== CERTIFICATE & DIPLOMA COURSES ===
Duration: All certificate and diploma courses are exactly 1 Year long.
Dance (₹1500, Nupur Mandir): Kathak, Manipuri, Bharatnatyam.
Music (₹1500, Sur Mandir): Sarod, Sitar, Tabla, Violin, Guitar, Vocal.
Craft (₹1500, Shilp Mandir Room 108): Shibori, Batik, Block Printing, Macrame & Knotting.
Language (₹1500, Vani Mandir Room 103): French, German, Sanskrit.
Tech (₹3500–₹7000, AAPJI Institute): Python, Android, Web Application, .NET, CCNA Networking, Medical Image Processing.
Media (₹7000, Vigyan Mandir FM Radio Office): Radio Production, Audio Engineering, Broadcast Journalism.

=== CLUBS ===
AAYAM: The official literary and creative club , and magazine of Faculty of MAthematics and computer , banasthali vidyapith
ACM Chapter:ACM Chapter is an unofficial coding club that focuses on programming, software development, and technical skill development. The club organizes coding workshops, hackathons, and technical sessions for students interested in computer science and programming. The contact person for ACM Chapter is Neelam Sharma Madam, and students can reach the club through the email acmchapter@banasthali.in
. The club is located at Apaji Institute.
Black Illuminators:It's a non-official dance club that promotes dance, creativity, and stage performances. The club regularly participates in cultural events and university performances. The contact person for Black Illuminators is Shreyanshi, and students can contact the club at 9569890529. The club practices and performs at Shri Shanta Uthjam.
E-Cell:E-Cell is an official entrepreneurship club that promotes innovation, startups, and business ideas among students. The club organizes business competitions, startup workshops, and entrepreneurship awareness programs. The contact person for E-Cell is Sanskriti Sharma Madam, and the contact email is sanskritisharma@banasthali.in
. The club is located at Nav Mandir.
Expressio:Expressio is an official public speaking club that helps students develop communication, public speaking, and presentation skills. The club organizes debates, speech competitions, and anchoring events. The contact person for Expressio is Alankritaa Saxena, and the contact number is 8103603589. The club venue is Nav Mandir Auditorium 1 and Prabha Mandir Auditorium 1.
Freezy Freaks:Freezy Freaks is a non-official dance club that encourages students to participate in dance performances and cultural activities. The contact person for Freezy Freaks is Kanika, and students can contact the club at 6350459117. The club is located at Shri Shanta Neri.
IEEE:IEEE is a non-official technical club related to Electrical, Electronics, Computer Science, IT, Robotics, Aerospace, Biomedical, and Artificial Intelligence. The club organizes technical workshops, seminars, and competitions for technical skill development. The contact person for IEEE is Adwika Singh, and the contact number is 6264823812. The club is located in the Automation Department.
MSC-BV:MSC-BV is an official Microsoft technical club that focuses on Microsoft technologies, programming, development, and technical training. The contact person for MSC-BV is Anushka, and the contact number is 9149128554. The club is located at Nav Mandir.
Street Dancers:Street Dancers is a non-official dance club that promotes street dance and stage performances in university cultural events. The contact person for Street Dancers is Yashvi, and the contact number is +91 9426189809. The club is located at Shri Shanta Saudh.
Therav:Therav is an official poetry club that encourages creative writing, poetry, and literary activities. The club organizes poetry sessions, writing competitions, and literary events. The contact person for Therav is Muskaan Vaswani, and the contact number is 8058681767. The club is located at Ratan Mandir.
Algobyter.bv :official open  source technical club of banasthali vidyapith .
Logos:The official debating and literary society of  banasthali vidyapith .
Litwits: The literary society of  banasthali vidyapith.
Teamtemple : It trains you for jobs, internships, employability , management , personality and leadership.

=== CAMPUS LIFE & POLICIES ===
Leaves: 10 leaves per semester.
Gate pass: Leave application + parent permission → Vani Mandir verification → Warden sign → HOD sign → Vani Mandir gate pass → Hostel authority sign → leave campus.
Hostel change: Allowed via swap with student from new hostel.
Parcels: Delivered to Kuter → distributed to hostels → warden gives to students. Returns also via Kuter.
WiFi: Available in academic + hostel areas, paid annually (not free).
Library: Central library + departmental libraries + online PYQs via library links.
Canteen/Mess: Vegetarian meals.
Semester exams: April and December.
Head of Department (HOD) : Dr Rajiv is the HOD of CS and IT department and Anshuman Shastri is HOD of CS-AI

"""

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "university_chatbot")
    )

def get_bot_response(user_text, chat_history=[]):
    if _groq_client is None:
        return "Chatbot AI is currently unavailable (Groq library missing)."
    
    today_obj = date.today()
    today_str = str(today_obj)
    
    dynamic_events_text = f"\n=== LIVE DATABASE RECORDS (TODAY'S DATE: {today_str}) ===\n"
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT workshop_name, category, venue, event_date, event_time FROM workshops ORDER BY event_date ASC")
        workshops = cursor.fetchall()
        dynamic_events_text += "\n-- NOTICES & WORKSHOPS --\n"
        if workshops:
            for w in workshops:
                w_date = w['event_date']
                if w_date:
                    if w_date < today_obj: tag = "[PAST]"
                    elif w_date == today_obj: tag = "[TODAY]"
                    else: tag = "[UPCOMING]"
                else:
                    tag = "[UNKNOWN DATE]"
                dynamic_events_text += f"{tag} Event: {w['workshop_name']} | Category: {w['category']} | Venue: {w['venue']} | Date: {w_date} | Time: {w['event_time']}\n"
        else:
            dynamic_events_text += "No workshops currently scheduled.\n"
            
        try:
            cursor.execute("SELECT event_name, reg_link, deadline FROM event_forms ORDER BY deadline ASC")
            forms = cursor.fetchall()
            dynamic_events_text += "\n-- REGISTRATION FORMS --\n"
            if forms:
                for f in forms:
                    f_date = f['deadline']
                    if f_date and f_date < today_obj: tag = "[EXPIRED]"
                    else: tag = "[ACTIVE]"
                    dynamic_events_text += f"{tag} Form: {f['event_name']} | Link: {f['reg_link']} | Deadline: {f_date}\n"
        except: pass 

        try:
            cursor.execute("SELECT event_name, event_date, category FROM calendar_events ORDER BY event_date ASC")
            cal_events = cursor.fetchall()
            dynamic_events_text += "\n-- CALENDAR EVENTS --\n"
            if cal_events:
                for c in cal_events:
                    c_date = c['event_date']
                    if c_date:
                        if c_date < today_obj: tag = "[PAST]"
                        elif c_date == today_obj: tag = "[TODAY]"
                        else: tag = "[UPCOMING]"
                    dynamic_events_text += f"{tag} Date: {c_date} | Event: {c['event_name']} | Category: {c['category']}\n"
        except: pass 

        conn.close()
    except Exception as e:
        dynamic_events_text += f"Live Database sync currently unavailable.\n"

    full_knowledge_base = UNIVERSITY_CONTEXT + dynamic_events_text

    try:
        messages = [{'role': 'system', 'content': full_knowledge_base}]
        
        for msg in chat_history[-4:]:
            role = 'user' if msg['role'] == 'user' else 'assistant'
            messages.append({'role': role, 'content': msg['content']})
            
        strict_prompt = f"{user_text}\n\n[SYSTEM COMMAND: Answer in English by default unless explicitly asked otherwise. TODAY IS {today_str}. Only use [UPCOMING]/[TODAY] for 'upcoming' events. CRITICAL RULE: For ANY registration queries (e.g., 'how to register', 'registration process', 'event registration', 'escape room registration', 'where to register', 'participation form'), you MUST respond EXACTLY with: 'To register for this event, please go to the Forms and Links section on the university portal and fill out the Event Registration Form.'. CRITICAL RULE: Keep answers short and helpful. Only give detailed information when the user asks 'tell me in detail'. If the exact answer is not in the context, do NOT guess. DO NOT add conversational filler.]"
            
        if len(chat_history) == 0 or chat_history[-1]['content'] != user_text:
            messages.append({'role': 'user', 'content': strict_prompt})
        else:
            messages[-1]['content'] = strict_prompt
            
        response = _groq_client.chat.completions.create(
            model='openai/gpt-oss-20b', 
            messages=messages, 
            max_tokens=1000, 
            temperature=0.0  
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq API Error on primary model: {e}")
        try:
            # Fallback 1 to avoid rate limits during presentation
            response = _groq_client.chat.completions.create(
                model='openai/gpt-oss-20b', 
                messages=messages, 
                max_tokens=1000, 
                temperature=0.0  
            )
            return response.choices[0].message.content.strip()
        except Exception as e2:
            print(f"Groq API Error on fallback 1: {e2}")
            try:
                # Fallback 2
                response = _groq_client.chat.completions.create(
                    model='openai/gpt-oss-20b', 
                    messages=messages, 
                    max_tokens=300, 
                    temperature=0.0  
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"Technical Error: {e}")
                return f"The system encountered an error: {e}"
st.session_state.theme = "Dark"
st.set_page_config(page_title="Eventify", layout="wide", initial_sidebar_state="collapsed")

bg_color = "#0E1117"
text_color = "#FFFFFF"
input_bg = "transparent"
card_bg = "#1E2530"
border_color = "#2D5A5C"
sidebar_bg = "#1E2530"
login_border = "#FFFFFF"

st.markdown(f"""
<style>
/* --- FONT SIZES (Projector Scale) --- */
p, label, span, li, td, th {{ font-size: 23px !important; line-height: 1.6 !important; }}
h1 {{ font-size: 3.1rem !important; }}
h2 {{ font-size: 2.7rem !important; }}
h3 {{ font-size: 2.1rem !important; }}
.stTextInput input {{ font-size: 23px !important; padding: 16px !important; }}
div[data-baseweb="select"] span {{ font-size: 21px !important; }}
.chat-bubble {{ padding: 18px 24px !important; border-radius: 16px; margin: 8px 0; max-width: 80%; font-size: 23px !important; }}

/* --- SIDEBAR --- */
[data-testid="stSidebar"] h1 {{ font-size: 26px !important; white-space: nowrap !important; overflow: hidden !important; text-overflow: clip !important; padding-bottom: 10px !important; }}
[data-testid="stSidebarUserContent"] {{ overflow-y: auto !important; }}

header[data-testid="stHeader"] {{ background-color: transparent !important; }}
.stApp {{
    background-image: url("data:image/jpg;base64,{bg1}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    animation: slideShow 36s infinite;
    animation-fill-mode: forwards;
    color: {text_color} !important;
}}
.stApp::before {{
    content: ""; position: fixed; inset: 0; backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px); background: rgba(0, 0, 0, 0.75); z-index: 0;
}}
.stApp > * {{ position: relative; z-index: 1; }}
@keyframes slideShow {{
    0%   {{ background-image: url("data:image/jpg;base64,{bg1}"); }}
    12%  {{ background-image: url("data:image/jpg;base64,{bg1}"); }}
    16%  {{ background-image: url("data:image/jpg;base64,{bg2}"); }}
    29%  {{ background-image: url("data:image/jpg;base64,{bg2}"); }}
    33%  {{ background-image: url("data:image/jpg;base64,{bg3}"); }}
    45%  {{ background-image: url("data:image/jpg;base64,{bg3}"); }}
    50%  {{ background-image: url("data:image/jpg;base64,{bg4}"); }}
    62%  {{ background-image: url("data:image/jpg;base64,{bg4}"); }}
    66%  {{ background-image: url("data:image/jpg;base64,{bg5}"); }}
    79%  {{ background-image: url("data:image/jpg;base64,{bg5}"); }}
    83%  {{ background-image: url("data:image/jpg;base64,{bg6}"); }}
    96%  {{ background-image: url("data:image/jpg;base64,{bg6}"); }}
    100% {{ background-image: url("data:image/jpg;base64,{bg1}"); }}
}}
section[data-testid="stSidebar"] {{ background-color: {sidebar_bg} !important; }}
section[data-testid="stSidebar"] * {{ color: {text_color} !important; }}
.logo-container {{ display: flex; justify-content: center; font-size: 48px; font-weight: 800; color: #FFFFFF; margin-top: 10px; margin-bottom: 30px; font-family: 'Inter', sans-serif; }}

/* Clean input boxes */
.stTextInput div[data-baseweb="input"] {{ background-color: transparent !important; border: 2px solid {border_color} !important; border-radius: 12px !important; }}
.stTextInput input {{ color: {text_color} !important; background-color: transparent !important; }}
button[data-testid="stTextInputPasswordToggle"] {{ background-color: transparent !important; border: none !important; margin-right: 10px !important; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ border-color: {login_border} !important; border-width: 3px !important; border-style: solid !important; border-radius: 16px !important; padding: 30px !important; background-color: {card_bg} !important; }}

/* ---------------------------------------------------- */
/* BUTTON STYLES                                         */
/* ---------------------------------------------------- */

/* PRIMARY — solid blue */
div.stButton > button[kind="primary"] {{
    background-color: #006699 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    height: 55px !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease-in-out !important;
}}
div.stButton > button[kind="primary"]:hover {{
    background-color: #0088cc !important;
    box-shadow: 0px 4px 15px rgba(0, 160, 220, 0.4) !important;
    transform: translateY(-2px) !important;
}}

/* SECONDARY — rounded pill outlined (matches image 2 style) */
div.stButton > button[kind="secondary"] {{
    background-color: #006699 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 25px !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    height: 52px !important;
    width: 100% !important;
    transition: all 0.3s ease-in-out !important;
}}
div.stButton > button[kind="secondary"]:hover {{
    background-color: #0088cc !important;
    box-shadow: 0px 4px 15px rgba(0, 160, 220, 0.4) !important;
    transform: translateY(-2px) !important;
}}

/* TERTIARY — plain text link */
div.stButton > button[kind="tertiary"] {{
    background-color: transparent !important;
    color: #00A0DC !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 0 !important;
    height: auto !important;
    min-height: unset !important;
    white-space: nowrap !important;
    text-decoration: underline !important;
}}
div.stButton > button[kind="tertiary"]:hover {{
    color: #FFFFFF !important;
    text-decoration: underline !important;
    background-color: transparent !important;
}}
div.stButton > button[kind="tertiary"] p {{ font-size: 20px !important; margin: 0 !important; white-space: nowrap !important; }}

/* --- SIDEBAR BUTTONS --- */
section[data-testid="stSidebar"] div.stButton > button {{
    background-color: #006699 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    font-size: 18px !important;
    height: 44px !important;
    padding: 4px 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}}
section[data-testid="stSidebar"] div.stButton > button:hover {{ background-color: #0088cc !important; }}

/* ---------------------------------------------------- */

div[data-testid="metric-container"] {{ background-color: {card_bg} !important; border: 1px solid {border_color} !important; border-radius: 12px !important; padding: 10px !important; }}
.stDataFrame {{ background-color: {card_bg} !important; }}
.user-bubble {{ background-color:#1a472a; margin-left:auto; }}
.bot-bubble {{ background-color: {card_bg}; border: 1px solid {border_color}; }}
hr {{ border-color: {border_color} !important; }}

div.element-container:has(.user-profile-badge) {{ position: fixed !important; top: 55px !important; right: 25px !important; z-index: 99999 !important; width: auto !important; }}
.user-profile-badge {{ display: flex; align-items: center; gap: 10px; background: rgba(30, 37, 48, 0.85); padding: 5px 15px 5px 5px; border-radius: 50px; border: 1px solid #00A0DC; box-shadow: 0 4px 10px rgba(0,0,0,0.3); backdrop-filter: blur(5px); cursor: pointer; transition: 0.3s; }}
.user-profile-badge:hover {{ transform: scale(1.02); background: rgba(30, 37, 48, 1); }}
.user-avatar {{ background: #00A0DC; color: white; font-weight: bold; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 18px; }}
.user-name {{ color: white; font-weight: 600; font-size: 18px; padding-right: 5px; }}

div.element-container:has(.top-right-logout-btn) + div.element-container {{ position: fixed !important; top: 110px !important; right: 25px !important; z-index: 99998 !important; background: rgba(30, 37, 48, 0.95) !important; border: 1px solid #00A0DC !important; border-radius: 12px !important; padding: 5px !important; min-width: 120px !important; width: auto !important; box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important; opacity: 0 !important; visibility: hidden !important; transform: translateY(-10px) !important; transition: all 0.3s ease !important; }}
div.element-container:has(.user-profile-badge):hover ~ div.element-container:has(.top-right-logout-btn) + div.element-container, div.element-container:has(.top-right-logout-btn) + div.element-container:hover {{ opacity: 1 !important; visibility: visible !important; transform: translateY(0px) !important; }}
div.element-container:has(.top-right-logout-btn) + div.element-container button {{ background-color: transparent !important; color: #FF3B30 !important; border: none !important; box-shadow: none !important; font-size: 15px !important; font-weight: 700 !important; text-decoration: none !important; width: 100% !important; height: auto !important; min-height: 0px !important; padding: 8px !important; cursor: pointer !important; text-align: center !important; }}
div.element-container:has(.top-right-logout-btn) + div.element-container button:hover {{ background-color: rgba(255, 59, 48, 0.1) !important; color: #FF3B30 !important; border-radius: 8px !important; }}

div.element-container:has(.floating-auth-btn) + div.element-container {{ position: fixed !important; top: 65px !important; right: 25px !important; z-index: 99999 !important; width: auto !important; }}
div.element-container:has(.floating-auth-btn) + div.element-container button {{ background-color: transparent !important; color: #FFFFFF !important; border: none !important; box-shadow: none !important; font-size: 24px !important; text-decoration: none !important; font-weight: 700 !important; padding: 0px !important; height: auto !important; width: auto !important; }}
div.element-container:has(.floating-auth-btn) + div.element-container button:hover {{ color: #CCCCCC !important; text-decoration: underline !important; transform: none !important; background-color: transparent !important; }}

div.element-container:has(.floating-back-btn) + div.element-container {{ position: fixed !important; top: 65px !important; left: 20px !important; z-index: 99999 !important; width: auto !important; }}
div.element-container:has(.floating-back-btn) + div.element-container button {{ background-color: transparent !important; color: #00A0DC !important; border: 2px solid #00A0DC !important; border-radius: 50px !important; padding: 10px 26px !important; font-size: 20px !important; font-weight: 700 !important; height: auto !important; width: auto !important; }}
div.element-container:has(.floating-back-btn) + div.element-container button:hover {{ background-color: #00A0DC !important; color: white !important; transform: scale(1.05) !important; }}
</style>
""", unsafe_allow_html=True)

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER DATABASE university_chatbot CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
        except: pass
        
        try:
            cursor.execute("SELECT event_date FROM workshops LIMIT 1")
            cursor.fetchall()
        except:
            cursor.execute("DROP TABLE IF EXISTS workshops")
            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workshops (
                id INT AUTO_INCREMENT PRIMARY KEY,
                workshop_name VARCHAR(255),
                category VARCHAR(255),
                venue VARCHAR(255),
                event_date DATE,
                event_time VARCHAR(255)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_forms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_name VARCHAR(255),
                reg_link VARCHAR(500),
                deadline DATE,
                qr_data LONGTEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255),
                user_message TEXT,
                bot_response TEXT,
                session_id VARCHAR(100),
                chat_title VARCHAR(100),
                is_pinned BOOLEAN DEFAULT FALSE,
                chat_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        try:
            cursor.execute("ALTER TABLE chat_history CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        except: pass

        try: cursor.execute("SELECT session_id FROM chat_history LIMIT 1"); cursor.fetchall()
        except: cursor.execute("ALTER TABLE chat_history ADD COLUMN session_id VARCHAR(100)")

        try: cursor.execute("SELECT chat_title FROM chat_history LIMIT 1"); cursor.fetchall()
        except: cursor.execute("ALTER TABLE chat_history ADD COLUMN chat_title VARCHAR(100)")
            
        try: cursor.execute("SELECT is_pinned FROM chat_history LIMIT 1"); cursor.fetchall()
        except: cursor.execute("ALTER TABLE chat_history ADD COLUMN is_pinned BOOLEAN DEFAULT FALSE")

        cursor.execute("SELECT COUNT(*) FROM workshops")
        count = cursor.fetchone()[0]
        
        if count == 0:
            initial_events = [
                ("Hack The Horizon-2", "General", "CAI-3 AUTOMATION", "2026-02-17", "9:00- 7:00 PM"),
                ("E-Game : BGMI", "Shadow Verse", "Aim n Act Lawn", "2026-02-18", "5:00-7:00 PM"),
                ("Takeshi's Castle", "Carnival Verse", "Vidula Maidan", "2026-02-19", "5:00-7:00 PM"),
                ("MayukhVerse: Explore the Verses", "General", "Aim n Act Room no-104", "2026-02-20", "5:00-7:00 PM")
            ]
            for evt in initial_events:
                cursor.execute("INSERT INTO workshops (workshop_name, category, venue, event_date, event_time) VALUES (%s, %s, %s, %s, %s)", evt)
            conn.commit()

        cursor.execute("SELECT COUNT(*) FROM event_forms")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO event_forms (event_name, reg_link, deadline, qr_data) VALUES (%s, %s, %s, %s)", 
                           ("Sample Hackathon 2026", "https://forms.gle/sample", "2026-12-31", ""))
            conn.commit()

        conn.close()
    except Exception as e:
        pass

def load_events_from_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT event_name, event_date, category FROM calendar_events")
        rows = cursor.fetchall()
        conn.close()
        events_dict = {}
        for name, date_obj, category in rows:
            if date_obj not in events_dict: events_dict[date_obj] = []
            events_dict[date_obj].append((name, category))
        return events_dict
    except: return {datetime.date(2026, 1, 26): [("Republic Day", "Holiday")]}

def save_event_to_db(name, date_obj, category):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO calendar_events (event_name, event_date, category) VALUES (%s, %s, %s)", (name, date_obj, category))
        conn.commit()
        conn.close()
        return True
    except: return False

def save_chat_to_db(email, user_msg, bot_msg):
    if not email or not user_msg or not bot_msg:
        return False

    if "current_session_id" not in st.session_state or not st.session_state.current_session_id:
        st.session_state.current_session_id = str(uuid.uuid4())
        st.session_state.chat_title = None

    session_id = st.session_state.current_session_id

    if "chat_title" not in st.session_state or not st.session_state.chat_title:
        try:
            title_prompt = f"Summarize this prompt into a very short 2 to 4 word title. No punctuation. Prompt: {user_msg}"
            res = _groq_client.chat.completions.create(
                model='openai/gpt-oss-20b',
                messages=[{"role": "user", "content": title_prompt}],
                max_tokens=10,
                temperature=0.3
            )
            st.session_state.chat_title = res.choices[0].message.content.strip().replace('"', '')
        except Exception:
            st.session_state.chat_title = user_msg[:25] + "..."

    title = st.session_state.chat_title
    if title: title = title[:95]

    last_error = None

    for attempt in range(3):
        conn = None
        try:
            conn = get_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO chat_history (email, user_message, bot_response, session_id, chat_title)
                VALUES (%s, %s, %s, %s, %s)
            """, (email, user_msg, bot_msg, session_id, title))

            conn.commit()
            return True

        except Exception as e:
            last_error = e
            if conn:
                try: conn.rollback()
                except: pass
            import time
            time.sleep(0.4 * (attempt + 1))
        finally:
            if conn:
                try: conn.close()
                except: pass

    st.toast(f"❌ Failed to save chat to history: {last_error}")
    return False

ALLOWED_EMAIL_REGEX = r"^(?!\.)(?!.*\.\.)[a-z0-9._]{6,30}(?<!\.)@(gmail\.com|banasthali\.in)$"
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")

def send_email_otp(to_email, otp):
    allowed_pattern = r"^[a-zA-Z0-9][a-zA-Z0-9_.+-]*@(gmail\.com|banasthali\.in)$"
    
    if not re.match(allowed_pattern, to_email.strip()):
        st.error(f"❌ Blocked: '{to_email}' is not a valid @gmail.com or @banasthali.in address.")
        return 
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Your Eventify OTP Code"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
    except Exception as e: 
        st.error(f"Error: {e}")
    
def is_valid_password(password: str) -> bool:
    if len(password) < 7: return False
    if not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password): return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False
    return True

def init_session_state():
    # --- Determine URL state FIRST so we can make smart initialization decisions ---
    url_page = st.query_params.get("page", "home")
    is_logged_in_url = st.query_params.get("logged_in") == "true"
    is_logout_url = st.query_params.get("logout") == "true"

    # --- SPLASH / WELCOME SCREEN ---
    # Only show splash when:
    #   1. It's a genuine first visit (no session state yet, AND no logged_in URL param)
    # Do NOT reset splash to True if the user is already authenticated (prevents redirect on reconnect)
    if "show_splash" not in st.session_state:
        # If the URL says logged_in=true, the user had an active session — skip splash
        st.session_state.show_splash = not is_logged_in_url

    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = str(uuid.uuid4())
    if "current_page" not in st.session_state:
        st.session_state.current_page = url_page

    # --- RESTORE SESSION FROM URL PARAMS (handles browser refresh / WebSocket reconnect) ---
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = is_logged_in_url
        if is_logged_in_url:
            st.session_state.role = st.query_params.get("role")
            st.session_state.create_email = st.query_params.get("email")
            # Restore current_page from URL so the right view is shown after reconnect
            if url_page and url_page != "home" or st.session_state.role == "admin":
                st.session_state.current_page = url_page if url_page else "home"
            if st.session_state.role == "user" and st.session_state.create_email:
                try:
                    conn = get_connection()
                    c = conn.cursor()
                    c.execute("SELECT user_name FROM users WHERE TRIM(email)=%s", (st.session_state.create_email,))
                    res = c.fetchone()
                    st.session_state.user_name = res[0] if res else "User"
                    conn.close()
                except:
                    st.session_state.user_name = "User"
            elif st.session_state.role == "admin":
                st.session_state.user_name = "Admin"
                st.session_state.current_page = "admin_dashboard"

    if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login"
    if "messages" not in st.session_state: st.session_state.messages = []
    if "calendar_events" not in st.session_state: st.session_state["calendar_events"] = load_events_from_db()
    if "maps" not in st.session_state: st.session_state.maps = "Search Maps"
    if "five_fold_select" not in st.session_state: st.session_state.five_fold_select = "Five Fold Activities"
    if "certificate" not in st.session_state: st.session_state.certificate = "Certificate & Diploma Courses"
    if "clubs" not in st.session_state: st.session_state.clubs = None
    if "forms" not in st.session_state: st.session_state.forms = None
    if "create_step" not in st.session_state: st.session_state.create_step = "email"
    if "forgot_step" not in st.session_state: st.session_state.forgot_step = "email"

def go_to(page):
    st.session_state.current_page = page
    st.query_params["page"] = page 

def handle_login(email, password):
    if not email or not password:
        st.warning("Please enter credentials")
        return
    
    email = email.strip().lower()

    # --- STRICT EMAIL VALIDATION LOGIC ---
    # 1. Check Domain Restriction
    if not (email.endswith("@gmail.com") or email.endswith("@banasthali.in")):
        st.error("❌ Invalid Domain. Only @gmail.com or @banasthali.in addresses are allowed.")
        return

    # 2. Extract Username (part before @)
    username_part = email.split('@')[0]

    # 3. Apply Specific Constraints (Length 6-30, no consecutive dots, etc.)
    # UPDATED: Added '_' to the allowed character class [a-z0-9._]
    valid_format = re.match(r"^(?!\.)(?!.*\.\.)[a-z0-9._]{6,30}(?<!\.)$", username_part)
    
    # 4. Check for at least one letter if length is 8 or more
    has_letter_if_long = True
    if len(username_part) >= 8:
        has_letter_if_long = any(c.isalpha() for c in username_part)

    if not valid_format or not has_letter_if_long:
        st.error("""
            ❌ Invalid Email Format.
            - Must be 6–30 characters long (before @).
            - Can include: Letters (a–z), Numbers (0–9), Periods (.), and Underscores (_).
            - Cannot include: Spaces or other special characters (@, #, $, etc.).
            - Cannot start or end with a dot (.).
            - Cannot have consecutive dots (..).
            - Usernames of 8 or more characters must include at least one letter.
        """)
        return

    # --- DATABASE CHECK ---
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check Admin Table
        cursor.execute("SELECT * FROM admin WHERE LOWER(TRIM(email)) = %s AND TRIM(password) = %s", (email, password.strip()))
        if cursor.fetchone():
            st.session_state.role = "admin"
            st.session_state.logged_in = True
            st.session_state.create_email = email
            st.session_state.user_name = "Admin"
            st.session_state.current_page = "admin_dashboard"
            st.query_params["logged_in"] = "true"
            st.query_params["role"] = "admin"
            st.query_params["email"] = email
            conn.close()
            st.rerun()
            return

        # Check Users Table
        cursor.execute("SELECT password, user_name FROM users WHERE LOWER(TRIM(email)) = %s", (email,))
        result = cursor.fetchone()
        if result:
            if result[0].strip() == password.strip():
                st.session_state.role = "user"
                st.session_state.logged_in = True
                st.session_state.create_email = email
                st.session_state.user_name = result[1].strip()
                st.session_state.user_sub_page = "chat"
                st.session_state.current_page = "home"
                st.query_params["logged_in"] = "true"
                st.query_params["role"] = "user"
                st.query_params["email"] = email
                conn.close()
                st.rerun()
            else:
                st.error("❌ Incorrect Credentials")
                conn.close()
        else:
            st.error("❌ Not registered. Please sign up.")
            conn.close()
            
    except Exception as e:
        st.error(f"DB Error: {e}")

def show_map_page(selected_place):
    def go_back_map():
        st.session_state.maps = "Search Maps"
        st.session_state.user_sub_page = "chat"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("⬅ Back", key="back_btn_map", on_click=go_back_map, use_container_width=True)

    st.markdown(f"<h2 style='text-align:center;color:#00a0dc;'>🗺️ Navigating to: {selected_place}</h2>", unsafe_allow_html=True)

    locations_data = [
        {"locID": 1, "name": "Nav Mandir", "lat": 26.4022004788927, "lng": 75.87827065128765},
        {"locID": 2, "name": "Prabha Mandir", "lat": 26.401602588370032 , "lng": 75.87762314261566 },
        {"locID": 3, "name": "Jamnalal Bajaj School Of Legal Studies", "lat": 26.40267789466391, "lng": 75.87675215615266 },
        {"locID": 4, "name": "Centre for Artificial Intelligence", "lat": 26.404046530783386, "lng": 75.87694790783368 },
        {"locID": 5, "name": "URJA MANDIR-Department of Physics", "lat": 26.403248379765536, "lng": 75.87553674276592},
        {"locID": 6, "name": "Bhu Mandir-Department Of Earth Sciences", "lat": 26.40390260232041, "lng": 75.87600128778898},
        {"locID": 7, "name": "Ratan Mandir", "lat": 26.404140738407083, "lng": 75.87541111109019},
        {"locID": 8, "name": "Vidya Mandir", "lat": 26.402717148309307, "lng": 75.87519490774764},
        {"locID": 9, "name": "Department of Education", "lat": 26.405514590875086, "lng": 75.87582598777884},
        {"locID": 10, "name": "Computer Science Department (CMS)", "lat": 26.403399722561353, "lng": 75.87472245326417},
        {"locID": 11, "name": "Vigyan Mandir", "lat": 26.403998782372376, "lng": 75.87396150882383},
        {"locID": 13, "name": "Vani Mandir", "lat": 26.404066938671107, "lng": 75.87295626116826},
        {"locID": 14, "name": "Surya Mandir", "lat": 26.404643577763203, "lng": 75.87159777617224},
        {"locID": 15, "name": "Jeev Mandir", "lat": 26.404858481759035, "lng": 75.8732283567598},
        {"locID": 16, "name": "Department of Pharmacy", "lat": 26.404336571345077, "lng": 75.87412933823272},
        {"locID": 17, "name": "Mahindra Pragya Mandir (FMS-WISDOM)", "lat": 26.402117329226172, "lng": 75.87668538346807},
        {"locID": 18, "name": "Shri Shanta Nigam", "lat": 26.399978348847895, "lng": 75.87794154819667 },
        {"locID": 19, "name": "Shri Shanta Teertham Hostel", "lat": 26.39727538038752, "lng": 75.87567540802432 },
        {"locID": 20, "name": "Shri Shanta Sadam", "lat": 26.4000432298736, "lng": 75.87578045366502 },
        {"locID": 21, "name": "Shri Shanta Ayanam", "lat": 26.399164070952818, "lng": 75.87643414147813},
        {"locID": 22, "name": "Shri Shanta Niveshnam", "lat": 26.399755959917798, "lng": 75.8756753523058},
        {"locID": 23, "name": "Shri Shanta Soudh", "lat": 26.400446868278166, "lng": 75.87654218099789},
        {"locID": 24, "name": "Shri Shanta Ajeeram", "lat": 26.39896152270994, "lng": 75.87539645959747},
        {"locID": 25, "name": "Shri Shanta Vasam", "lat": 26.3987814795234, "lng": 75.87631856431862},
        {"locID": 26, "name": "Shri Shanta Lok", "lat": 26.398110816181976, "lng": 75.87603967161203},
        {"locID": 27, "name": "Shri Shanta Uthjam", "lat": 26.397150513340346, "lng": 75.87684773072947},
        {"locID": 28, "name": "Shri Shanta vasti", "lat": 26.397621391314733, "lng": 75.87552512700093},
        {"locID": 29, "name": "Shri Shanta Sharanam", "lat": 26.39766713360121, "lng": 75.87723009273073},
        {"locID": 30, "name": "Shri Shanta Kulum", "lat": 26.400900932597345, "lng": 75.8718994384524},
        {"locID": 31, "name": "Shri Shanta Puri", "lat": 26.400548238775375, "lng": 75.87110628493573 },
        {"locID": 32, "name": "Shri Shanta Geham", "lat": 26.40148614607533, "lng": 75.87158330519321},
        {"locID": 33, "name": "Shri Shanta Vishwa Needam", "lat": 26.402493519503807, "lng": 75.87140490737008},
        {"locID": 34, "name": "Shri Shanta Gram", "lat": 26.400396029885943, "lng": 75.87189149518846},
        {"locID": 35, "name": "Shri Shanta Paleyam", "lat": 26.4058734672816, "lng": 75.86377755553995},
        {"locID": 36, "name": "Shri Shanta Prangan", "lat": 26.40484896916918, "lng": 75.86388281635446},
        {"locID": 37, "name": "Gliding and flying club", "lat": 26.406997157973006, "lng": 75.86974356824275},
        {"locID": 38, "name": "Swimming Pool ", "lat": 26.406070894082692, "lng": 75.87003296298396},
        {"locID": 40, "name": "Vidula maidan", "lat": 26.399531756859645, "lng": 75.87422127891813},
        {"locID": 41, "name": "Utkarsh Mandir", "lat": 26.404797080653772, "lng": 75.87704773472392},
        {"locID": 42, "name": "Sur Mandir", "lat": 26.404037306899582, "lng": 75.87460720481279},
        {"locID": 43, "name": "Shilp Mandir", "lat": 26.403777186877380, "lng": 75.87546790150602},
        {"locID": 44, "name": "Banasthali gym", "lat": 26.400454240810586, "lng": 75.87421434526907},
        {"locID": 45, "name": "Aapaji AIM & ACT ", "lat": 26.40266041994551, "lng": 75.87548677106426},
        {"locID": 46, "name": "Shri Shanta Bhuwnam", "lat": 26.39846968732872, "lng": 75.87701287395515},
        {"locID": 47, "name": "Shri Shanta Agar", "lat": 26.401632846454326, "lng": 75.87221449879162},
        {"locID": 48, "name": "Shri Shanta Dham", "lat": 26.401239873718193, "lng": 75.87489422292762},
        {"locID": 51, "name": "Shri Shanta Gangotri", "lat": 26.39884677211861, "lng": 75.87513887116002},
        {"locID": 52, "name": "Shri Shanta Sthanam", "lat": 26.39690432649606, "lng": 75.87628075669883},
        {"locID": 53, "name": "Shri Shanta Vastyam", "lat": 26.398839616054413, "lng": 75.87704271312164},
        {"locID": 54, "name": "Shri Shanta Vatika", "lat": 26.40076332637926, "lng": 75.8709233161746},
        {"locID": 55, "name": "Shri Shanta Vihar", "lat": 26.401655683686833, "lng": 75.87425856117247},
        {"locID": 57, "name": "Shri Shanta Neri", "lat": 26.397783420495763, "lng": 75.87660130097122},
        {"locID": 58, "name": "Shri Shanta Nikayee", "lat": 26.397409517747484, "lng": 75.87643308901667},
        {"locID": 59, "name": "Shri Shanta Nikunj", "lat": 26.40253143217188, "lng": 75.87198817384187},
        {"locID": 60, "name": "Shri Shanta Nishantam", "lat": 26.397631897813596, "lng": 75.87452045149242},
        {"locID": 61, "name": "Shri Shanta pattnam", "lat": 26.399086188060256, "lng":  75.8780069399949},
        {"locID": 62, "name": "Shri Shanta sangam", "lat": 26.39638885534673, "lng": 75.8761778117222},
        {"locID": 63, "name": "Shri Shanta Ashray", "lat": 26.404540595064194, "lng": 75.86513518845533}
    ]

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js"></script>
    <style>
        html, body {{ height: 100%; margin: 0; padding: 0; font-family: sans-serif; }}
        #map {{ height: calc(100% - 54px); }}
        #statusBar {{
            height: 54px; display: flex; align-items: center;
            gap: 10px; padding: 0 14px;
            background: #1a1a2e; color: white; font-size: 13px;
        }}
        #gpsBtn {{
            background: #00a0dc; color: white; border: none;
            padding: 8px 16px; border-radius: 20px; font-size: 13px;
            cursor: pointer; white-space: nowrap;
        }}
        #gpsBtn:hover {{ background: #0080b0; }}
        #gpsBtn.loading {{ background: #cc7700; }}
        #gpsBtn.success {{ background: #00aa44; }}
        #gpsBtn.error   {{ background: #cc2200; }}
        #statusText {{ color: #aac8e0; flex: 1; }}
        .leaflet-routing-container h2,
        .leaflet-routing-container h3,
        .leaflet-routing-alt h2,
        .leaflet-routing-alt h3 {{ display: none !important; }}
        .leaflet-routing-container {{
            max-width: 270px; font-size: 12px; background: white;
            border-radius: 10px; padding: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
<div id="statusBar">
    <button id="gpsBtn" onclick="getFreshLocation()">📍 Get My Location</button>
    <span id="statusText">Click the button to get your live location</span>
</div>
<div id="map"></div>
<script>
    const LOCATIONS  = {json.dumps(locations_data)};
    const AUTO_TARGET = "{selected_place}";
    const map = L.map('map').setView([26.4022, 75.8770], 16);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '© OpenStreetMap'
    }}).addTo(map);
    const routing = L.Routing.control({{
        waypoints: [],
        routeWhileDragging: false,
        showAlternatives: false,
        fitSelectedRoutes: true,
        lineOptions: {{ styles: [{{ color: '#00a0dc', weight: 5 }}] }},
        createMarker: function(i, wp) {{
            const emoji = i === 0 ? '🔵' : '🏁';
            return L.marker(wp.latLng, {{
                icon: L.divIcon({{ html: '<div style="font-size:22px">' + emoji + '</div>', className: '', iconAnchor: [11,11] }})
            }});
        }}
    }}).addTo(map);
    routing.on('routesfound', function(e) {{
        const dist = e.routes[0].summary.totalDistance;
        const walkingSpeed = 67;
        const rawMins = dist / walkingSpeed;
        const finalMins = dist < 100 ? Math.ceil(rawMins + 1) : Math.ceil(rawMins);
        const distStr = dist >= 1000 ? (dist / 1000).toFixed(2) + ' km' : Math.round(dist) + ' m';
        let timeStr = '';
        if (finalMins < 1) {{ timeStr = 'less than 1 min'; }}
        else if (finalMins === 1) {{ timeStr = '1 min'; }}
        else if (finalMins >= 60) {{
            const hrs = Math.floor(finalMins / 60);
            const mins = finalMins % 60;
            timeStr = hrs + ' hr' + (mins > 0 ? ' ' + mins + ' min' : '');
        }} else {{ timeStr = finalMins + ' mins'; }}
        document.getElementById('statusText').innerText = '🚶 Distance: ' + distStr + '   ·   ⏱️ ~' + timeStr + ' walking';
        const routingContainer = document.querySelector('.leaflet-routing-container');
        if (routingContainer) {{
            const old = routingContainer.querySelector('#custom-time-header');
            if (old) old.remove();
            const header = document.createElement('div');
            header.id = 'custom-time-header';
            header.style.cssText = 'background:#1a1a2e;color:white;padding:6px 10px;border-radius:6px;margin-bottom:6px;font-size:13px;font-weight:600;';
            header.innerText = '📍 ' + distStr + '  ·  ⏱️ ~' + timeStr + ' walking';
            routingContainer.insertBefore(header, routingContainer.firstChild);
        }}
    }});
    let hasAttemptedFallback = false;
    routing.on('routingerror', function(e) {{
        if (!hasAttemptedFallback && destLat !== null && destLng !== null) {{
            hasAttemptedFallback = true;
            document.getElementById('statusText').innerText = '⚠️ Hostel Wi-Fi location glitch detected. Routing from Campus Center...';
            const fallbackStart = L.latLng(26.4022, 75.8770);
            if (userMarker) {{ map.removeLayer(userMarker); }}
            userMarker = L.marker(fallbackStart, {{
                icon: L.divIcon({{ html: '<div style="font-size:24px">🔵</div>', className: '', iconAnchor: [12, 12] }})
            }}).addTo(map).bindPopup('📍 Simulated Start (Campus Center)').openPopup();
            map.setView(fallbackStart, 16);
            routing.setWaypoints([fallbackStart, L.latLng(destLat, destLng)]);
        }} else {{
            document.getElementById('statusText').innerText = '⚠️ Route not found. Try again.';
        }}
    }});
    let userMarker = null;
    let watchId = null;
    let destLat = null;
    let destLng = null;
    let bestAccuracy = Infinity;
    function getFreshLocation() {{
        const btn = document.getElementById('gpsBtn');
        const stat = document.getElementById('statusText');
        if (!navigator.geolocation) {{
            stat.innerText = '❌ Geolocation not supported by this browser.';
            btn.className = 'error';
            return;
        }}
        if (watchId !== null) {{ navigator.geolocation.clearWatch(watchId); watchId = null; }}
        bestAccuracy = Infinity;
        btn.innerText = '⏳ Getting GPS...';
        btn.className = 'loading';
        stat.innerText = '🛰️ Acquiring GPS signal...';
        watchId = navigator.geolocation.watchPosition(
            function(pos) {{
                const lat = pos.coords.latitude;
                const lng = pos.coords.longitude;
                const acc = Math.round(pos.coords.accuracy);
                const userPt = L.latLng(lat, lng);
                if (userMarker) {{ map.removeLayer(userMarker); }}
                userMarker = L.marker(userPt, {{
                    icon: L.divIcon({{ html: '<div style="font-size:24px">🔵</div>', className: '', iconAnchor: [12, 12] }})
                }}).addTo(map).bindPopup('📍 You are here<br>Accuracy: ±' + acc + ' m').openPopup();
                btn.innerText = '✅ Live Location';
                btn.className = 'success';
                stat.innerText = '📍 Accuracy: ±' + acc + ' m  (live updating)';
                if (acc < bestAccuracy - 20) {{ bestAccuracy = acc; map.setView(userPt, 17); }}
                if (destLat !== null && destLng !== null) {{ routing.setWaypoints([userPt, L.latLng(destLat, destLng)]); }}
            }},
            function(err) {{
                if (watchId !== null) {{ navigator.geolocation.clearWatch(watchId); watchId = null; }}
                btn.innerText = '❌ GPS Failed — Tap to Retry';
                btn.className = 'error';
                const msgs = {{ 1: 'Permission denied. Allow location in browser settings.', 2: 'Position unavailable. Move to open area.', 3: 'GPS timed out. Try again.' }};
                stat.innerText = msgs[err.code] || 'GPS error: ' + err.message;
                if (destLat !== null) {{
                    routing.setWaypoints([L.latLng(26.4022, 75.8770), L.latLng(destLat, destLng)]);
                    stat.innerText += ' — Using campus center as start point.';
                }}
            }},
            {{ enableHighAccuracy: true, timeout: 30000, maximumAge: 0 }}
        );
    }}
    function navigateTo(lat, lng) {{
        destLat = lat; destLng = lng; hasAttemptedFallback = false;
        const stat = document.getElementById('statusText');
        if (userMarker) {{
            const userPos = userMarker.getLatLng();
            routing.setWaypoints([userPos, L.latLng(lat, lng)]);
            stat.innerText = '🗺️ Drawing route to destination...';
        }} else {{
            stat.innerText = '📍 Getting your location first...';
            getFreshLocation();
        }}
    }}
    LOCATIONS.forEach(l => {{
        let emoji = '🎓';
        const n = l.name.trim().toLowerCase();
        if (l.name.startsWith('Shri Shanta')) emoji = '🏠';
        else if (n.includes('gym')) emoji = '🏋️';
        else if (n.includes('flying')) emoji = '✈️';
        else if (n.includes('vidula maidan')) emoji = '⚽';
        else if (n.includes('swimming')) emoji = '🏊';
        else if (n.includes('library')) emoji = '📚';
        else if (n.includes('canteen')) emoji = '🍽️';
        const icon = L.divIcon({{
            html: '<div style="font-size:20px;filter:drop-shadow(0 1px 2px #000)">' + emoji + '</div>',
            className: '', iconSize: [26, 26], iconAnchor: [13, 13]
        }});
        const marker = L.marker([l.lat, l.lng], {{ icon }}).addTo(map);
        marker.bindPopup(
            '<b style="font-size:14px">' + l.name + '</b><br>' +
            '<button onclick="navigateTo(' + l.lat + ',' + l.lng + ')" ' +
            'style="margin-top:6px;background:#00a0dc;color:white;border:none;padding:5px 12px;border-radius:12px;cursor:pointer;font-size:12px;">' +
            '🗺️ Navigate Here</button>'
        );
    }});
    if (AUTO_TARGET && AUTO_TARGET !== "Search Maps") {{
        const target = LOCATIONS.find(x => x.name.toLowerCase().includes(AUTO_TARGET.toLowerCase()));
        if (target) {{ destLat = target.lat; destLng = target.lng; map.setView([target.lat, target.lng], 17); }}
    }}
    window.addEventListener('load', function() {{ setTimeout(getFreshLocation, 500); }});
</script>
</body>
</html>
"""
    components.html(html, height=720)

def show_notices_page():
    def go_back_notices():
        st.session_state.user_sub_page = "chat"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("⬅ Back", key="back_btn_notices", type="secondary", on_click=go_back_notices, use_container_width=True)
        
    st.markdown("<h1 style='text-align:center; color:#00e5ff;'>📢 Notices & Workshops</h1>", unsafe_allow_html=True)
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as cnt FROM workshops")
        db_count = cursor.fetchone()['cnt']
        cursor.execute("SELECT workshop_name, category, venue, event_date, event_time FROM workshops ORDER BY event_date DESC, id DESC")
        notices = cursor.fetchall()
        conn.close()
        user_email = st.session_state.get("create_email", "guest")
        components.html(f"<script>window.parent.localStorage.setItem('seenEventsCount_{user_email}', '{db_count}');</script>", height=0, width=0)
    except Exception as e:
        notices = []
        st.error(f"Database sync error: {e}")
        
    if not notices:
        st.info("No new notices or workshops at the moment.")
    else:
        for n in notices:
            with st.container(border=True):
                e_date = n.get('event_date', '')
                e_time = n.get('event_time', '')
                st.caption(f"🏷️ Category: {n.get('category', 'General')} &nbsp;&nbsp;|&nbsp;&nbsp; 📍 Venue: {n.get('venue', 'TBA')} &nbsp;&nbsp;|&nbsp;&nbsp; 📅 Date: {e_date} &nbsp;&nbsp;|&nbsp;&nbsp; ⏰ Time: {e_time}")
                st.markdown(f"**{n.get('workshop_name', '')}**")

@st.dialog("📷 Event Poster", width="large")
def show_qr_popup(qr_b64, event_name):
    st.markdown(f"<h2 style='text-align:center; color:#00A0DC; margin-top: -10px;'>{event_name}</h2>", unsafe_allow_html=True)
    st.markdown(f'''
        <div style="display:flex; justify-content:center; align-items: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{qr_b64}" style="max-width: 100%; max-height: 75vh; border-radius: 12px; border: 2px solid #00A0DC; box-shadow: 0px 10px 30px rgba(0,0,0,0.7);">
        </div>
    ''', unsafe_allow_html=True)
    if st.button("❌ Close Poster", type="secondary", use_container_width=True):
        st.rerun()

def show_forms_page():
    def go_back_forms():
        st.session_state.forms = None
        st.session_state.user_sub_page = "chat"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("⬅ Back", key="back_btn_forms", type="secondary", on_click=go_back_forms, use_container_width=True)
        
    st.markdown("<h1 style='text-align:center; color:#00e5ff;'>🔗 Forms & Registration</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM event_forms ORDER BY deadline ASC")
        forms_data = cursor.fetchall()
        conn.close()
    except Exception as e:
        forms_data = []
        
    if not forms_data:
        st.info("No active registration forms available right now.")
    else:
        for i in range(0, len(forms_data), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(forms_data):
                    form = forms_data[i + j]
                    with cols[j].container(border=True, height=260):
                        st.markdown(f"<div style='height: 55px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;'><h3 style='color:#FFFFFF; margin-top:0px; line-height:1.2;' title='{form['event_name']}'>{form['event_name']}</h3></div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='height: 35px;'><p style='color:#FF3B30; font-weight:bold; margin-bottom: 0px;'>⏳ Last Date: {form['deadline']}</p></div>", unsafe_allow_html=True)
                        if form['reg_link']:
                            st.link_button("📝 Register Here", url=form['reg_link'], use_container_width=True)
                        elif not form['reg_link'] and not form['qr_data']:
                            st.button("🚫 No Link Available", type="secondary", disabled=True, key=f"no_link_{form['id']}", use_container_width=True)
                        if form['qr_data']:
                            if st.button("📷 View Poster", type="secondary", key=f"qr_btn_{form['id']}", use_container_width=True):
                                show_qr_popup(form['qr_data'], form['event_name'])

@st.dialog("🔒 Access Restricted")
def show_login_popup():
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 0.2, 1])
    with c1:
        st.markdown("<p style='text-align:center; font-size: 18px; margin-bottom: 15px;'>Already a user?</p>", unsafe_allow_html=True)
        if st.button("Login", type="primary", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.session_state.current_page = "login_main"
            st.rerun()
    with c2:
        st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-weight:bold; color:#888888;'>or</p>", unsafe_allow_html=True)
    with c3:
        st.markdown("<p style='text-align:center; font-size: 18px; margin-bottom: 15px;'>New user?</p>", unsafe_allow_html=True)
        if st.button("Sign up", type="primary", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.session_state.current_page = "login_main"
            st.rerun()

def show_user_dashboard():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM workshops")
        current_workshops_count = cursor.fetchone()[0]
        conn.close()
    except:
        current_workshops_count = 0

    user_email = st.session_state.get("create_email", "guest")

    def handle_nav(active_menu):
        st.session_state.user_sub_page = "chat"
        if active_menu != "maps": st.session_state.maps = "Search Maps"
        if active_menu != "five_fold_select": st.session_state.five_fold_select = "Five Fold Activities"
        if active_menu != "certificate": st.session_state.certificate = "Certificate & Diploma Courses"
        if active_menu != "clubs": st.session_state.clubs = None
        if active_menu != "forms": st.session_state.forms = None

    def click_notices():
        st.session_state.user_sub_page = "notices"
        st.session_state.maps = "Search Maps"
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.certificate = "Certificate & Diploma Courses"
        st.session_state.clubs = None
        st.session_state.forms = None

    def click_history():
        st.session_state.user_sub_page = "history"
        st.session_state.maps = "Search Maps"
        st.session_state.five_fold_select = "Five Fold Activities"
        st.session_state.certificate = "Certificate & Diploma Courses"

    if not st.session_state.logged_in:
        st.markdown('<span class="floating-auth-btn" style="display:none;"></span>', unsafe_allow_html=True)
        if st.button("Login / Sign up"):
            st.session_state.auth_mode = "login"
            st.session_state.current_page = "login_main"
            st.rerun()

    col1, col2 = st.sidebar.columns([1, 1])
    if not st.session_state.logged_in:
        if col1.button("History", use_container_width=True): show_login_popup()
        if col2.button("Notices", use_container_width=True): show_login_popup()
    else:
        with col1: st.button("History", use_container_width=True, on_click=click_history)
        with col2: st.button("Notices", use_container_width=True, on_click=click_notices)

    components.html(f"""
        <script>
            const updateBadge = () => {{
                const dbCount = {current_workshops_count};
                const email = '{user_email}';
                const storageKey = 'seenEventsCount_' + email;
                let seenCount = window.parent.localStorage.getItem(storageKey);
                if (seenCount === null) {{ seenCount = 47; window.parent.localStorage.setItem(storageKey, seenCount); }}
                else {{ seenCount = parseInt(seenCount); }}
                if (dbCount < seenCount) {{ seenCount = dbCount; window.parent.localStorage.setItem(storageKey, seenCount); }}
                const unread = dbCount - seenCount;
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(b => {{
                    const textContent = b.innerText || b.textContent || '';
                    if (textContent.trim() === 'Notices') {{
                        b.style.position = 'relative'; b.style.overflow = 'visible';
                        b.addEventListener('click', () => {{
                            window.parent.localStorage.setItem(storageKey, dbCount);
                            const badge = b.querySelector('.notices-badge');
                            if (badge) badge.style.display = 'none';
                        }});
                        let badge = b.querySelector('.notices-badge');
                        if (!badge) {{
                            badge = window.parent.document.createElement('div');
                            badge.className = 'notices-badge';
                            badge.style.cssText = 'position:absolute; top:-8px; right:-8px; background-color:#FF3B30; color:white; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px; box-shadow:0 2px 5px rgba(0,0,0,0.4); pointer-events:none; z-index:9999; line-height:1; font-family:sans-serif; border: 2px solid #1E2530;';
                            b.appendChild(badge);
                        }}
                        if (unread > 0) {{ badge.innerText = unread > 99 ? '99+' : unread; badge.style.display = 'flex'; }}
                        else {{ badge.style.display = 'none'; }}
                    }}
                }});
            }};
            updateBadge();
            setTimeout(updateBadge, 500);
            setTimeout(updateBadge, 1500);
            setTimeout(updateBadge, 3000);
        </script>
    """, height=0, width=0)

    st.sidebar.title("🎓 Eventify Menu")

    st.sidebar.selectbox("Search Maps", [
        "Search Maps", "Aapaji AIM & ACT ", "Banasthali gym","Bhu Mandir-Department Of Earth Sciences", "Centre for Artificial Intelligence",
        "Computer Science Department (CMS)", "Department of Education", "Department of Pharmacy","Gliding and flying club", "Jamnalal Bajaj School Of Legal Studies", "Jeev Mandir",
        "Mahindra Pragya Mandir (FMS-WISDOM)", "Nav Mandir", "Prabha Mandir", "Ratan Mandir","Shilp Mandir", "Shri Shanta Agar", "Shri Shanta Ajeeram", "Shri Shanta Ashray",
        "Shri Shanta Ayanam", "Shri Shanta Bhuwnam", "Shri Shanta Dham", "Shri Shanta Gangotri","Shri Shanta Geham", "Shri Shanta Gram", "Shri Shanta Kulum", "Shri Shanta Lok",
        "Shri Shanta Neri", "Shri Shanta Nigam", "Shri Shanta Nikayee", "Shri Shanta Niketan","Shri Shanta Nikunj", "Shri Shanta Nishantam", "Shri Shanta Niveshnam",
        "Shri Shanta Paleyam", "Shri Shanta Prangan", "Shri Shanta Puri", "Shri Shanta Sadam","Shri Shanta Sharanam", "Shri Shanta Soudh", "Shri Shanta Sthanam",
        "Shri Shanta Teertham Hostel", "Shri Shanta Uthjam", "Shri Shanta Vasam","Shri Shanta Vastyam", "Shri Shanta Vatika", "Shri Shanta Vihar",
        "Shri Shanta Vishwa Needam", "Shri Shanta pattnam", "Shri Shanta sangam","Shri Shanta vasti", "Sur Mandir", "Surya Mandir", "Swimming Pool ",
        "URJA MANDIR-Department of Physics", "Utkarsh Mandir", "Vani Mandir","Vidula maidan", "Vidya Mandir", "Vigyan Mandir"
    ], key="maps", on_change=handle_nav, args=("maps",))

    five_fold_choice = st.sidebar.selectbox(
        "Five Fold Activities",
        ["Five Fold Activities", "Aesthetic Education", "Physical Education", "Practical Education", "Moral Education"],
        key="five_fold_select", on_change=handle_nav, args=("five_fold_select",)
    )

    certificate_choice = st.sidebar.selectbox(
        "Certificate & Diploma Courses",
        ["Certificate & Diploma Courses", "Language", "Music", "Dance", "Art & Craft", "Tech", "Radio, Journalism & Media"],
        key="certificate", on_change=handle_nav, args=("certificate",)
    )

    club_choice = st.sidebar.selectbox(
        "Clubs", ["View All Clubs"],
        index=None, placeholder="Clubs",
        key="clubs", on_change=handle_nav, args=("clubs",)
    )

    forms_choice = st.sidebar.selectbox(
        "Forms & Links", ["Event Registration Form"],
        index=None, placeholder="Forms & Links",
        key="forms", on_change=handle_nav, args=("forms",)
    )

    if st.session_state.maps != "Search Maps": show_map_page(st.session_state.maps)
    elif st.session_state.get("user_sub_page") == "notices": show_notices_page()
    elif st.session_state.get("user_sub_page") == "history": show_history_page()
    elif forms_choice == "Event Registration Form": show_forms_page()
    elif five_fold_choice == "Aesthetic Education":
        try: aesthetic.aesthetic_page()
        except: pass
    elif five_fold_choice == "Physical Education":
        try: physical.physical_page()
        except: pass
    elif five_fold_choice == "Practical Education":
        try: practical.practical_page()
        except: pass
    elif five_fold_choice == "Moral Education":
        try: moral.moral_page()
        except: pass
    elif certificate_choice == "Language":
        try: languagecd.language_page()
        except: pass
    elif certificate_choice == "Music":
        try: music.music_page()
        except: pass
    elif certificate_choice == "Dance":
        try: dance.dance_page()
        except: pass
    elif certificate_choice == "Art & Craft":
        try: craft.craft_page()
        except: pass
    elif certificate_choice == "Tech":
        try: tech.tech_page()
        except: pass
    elif certificate_choice == "Radio, Journalism & Media":
        try: massmedia.massmedia_page()
        except: pass
    elif club_choice == "View All Clubs":
        try: show_clubs_page()
        except: pass
    else: show_chatbot_interface()

def handle_user_input():
    if st.session_state.user_input_box.strip():
        st.session_state.pending_msg = st.session_state.user_input_box.strip()
        st.session_state.user_input_box = ""

def show_chatbot_interface():
    st.title("🎓 Eventify")

    if "mic_counter" not in st.session_state: st.session_state.mic_counter = 0
    if "pending_msg" not in st.session_state: st.session_state.pending_msg = ""
    if "mic_error" not in st.session_state: st.session_state.mic_error = None

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble user-bubble'><b>You:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble bot-bubble'><b>Bot:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.text_input(
            "💬 Ask anything:",
            placeholder="Ask or speak your message...",
            key="user_input_box",
            on_change=handle_user_input
        )

        mic_clicked = streamlit_js_eval(
            js_expressions=f"""
            new Promise((resolve) => {{
                let clicked = false;
                const checkAndAdd = () => {{
                    if (clicked) return;
                    const inputBox = window.parent.document.querySelector('input[placeholder="Ask or speak your message..."]');
                    if (inputBox) {{
                        let baseWebInput = inputBox.closest('div[data-baseweb="input"]');
                        baseWebInput.style.paddingRight = '45px';
                        baseWebInput.style.position = 'relative';
                        let micBtn = baseWebInput.querySelector('.mic-button');
                        if (!micBtn) {{
                            micBtn = window.parent.document.createElement('button');
                            micBtn.className = 'mic-button';
                            micBtn.innerHTML = '🎙️';
                            micBtn.style.cssText = 'position:absolute; right:8px; top:50%; transform:translateY(-50%); border:none; background:none; font-size:24px; cursor:pointer; color:#00A0DC; z-index:100; transition: 0.2s;';
                            micBtn.onclick = () => {{
                                clicked = true;
                                micBtn.innerHTML = '🔴';
                                resolve(true);
                            }};
                            baseWebInput.appendChild(micBtn);
                        }}
                    }}
                }};
                checkAndAdd();
                setInterval(checkAndAdd, 1000);
            }})
            """, key=f"mic_eval_{st.session_state.mic_counter}"
        )

        if st.session_state.mic_error:
            st.warning(st.session_state.mic_error)
            st.session_state.mic_error = None

    with col2:
        selected_date = st.date_input("📅 Pick a date:", datetime.date.today())

    all_events = st.session_state.get("calendar_events", {})
    if selected_date in all_events:
        st.success(f"📌 Events on {selected_date}:")
        for event_name, category in all_events[selected_date]:
            st.markdown(f'<div style="font-size:22px; color:white; font-weight:bold;">📅 {event_name}</div>', unsafe_allow_html=True)
    else:
        st.info("No event on this date.")

    # --- Upcoming Events Section ---
    # Fetch upcoming events dynamically from calendar_events where category='Upcoming'
    upcoming_events_list = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT event_name FROM calendar_events WHERE LOWER(TRIM(category)) = 'upcoming' ORDER BY event_date ASC")
        for row in cursor.fetchall():
            upcoming_events_list.append(row[0].strip())
        conn.close()
    except:
        pass

    # Fallback defaults if nothing in DB yet
    if not upcoming_events_list:
        upcoming_events_list = ["Hackathon", "Five Fold Activities 2026-2027", "Adhyay 2026", "Escape Room"]

    st.markdown("<div style='color:#FFFFFF; font-size:24px; font-weight:700; margin-top:18px; margin-bottom:10px; font-family:Inter,sans-serif;'>Upcoming Events</div>", unsafe_allow_html=True)

    if "upcoming_event_message" not in st.session_state:
        st.session_state.upcoming_event_message = None

    def handle_upcoming_click(event_name):
        found = False
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM event_forms WHERE LOWER(TRIM(event_name)) LIKE %s", (f"%{event_name.lower().strip()}%",))
            count = cursor.fetchone()[0]
            conn.close()
            if count > 0:
                found = True
        except:
            pass

        if found:
            st.session_state.user_sub_page = "chat"
            st.session_state.maps = "Search Maps"
            st.session_state.five_fold_select = "Five Fold Activities"
            st.session_state.certificate = "Certificate & Diploma Courses"
            st.session_state.clubs = None
            st.session_state.forms = "Event Registration Form"
            st.session_state.upcoming_event_message = None
        else:
            st.session_state.upcoming_event_message = event_name

    with st.container():
        st.markdown("""
        <span class="upcoming-marker"></span>
        <style>
            span.upcoming-marker { display: none; }
            div.element-container:has(span.upcoming-marker) ~ div.element-container button {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: #00A0DC !important;
                font-family: Inter, sans-serif !important;
                font-size: 20px !important;
                font-weight: 500 !important;
                padding: 0 !important;
                margin: 0 !important;
                margin-left: 0px !important;
                min-height: 0 !important;
                height: auto !important;
                justify-content: flex-start !important;
                text-align: left !important;
            }
            div.element-container:has(span.upcoming-marker) ~ div.element-container button:hover {
                color: #FFFFFF !important;
                text-decoration: underline !important;
                background: transparent !important;
            }
            div.element-container:has(span.upcoming-marker) ~ div.element-container button p {
                font-size: 20px !important;
                margin: 0 !important;
                padding: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        for evt in upcoming_events_list:
            safe_key = "".join(c if c.isalnum() else "_" for c in evt)
            st.button(f"• \u00A0{evt}", key=f"upcoming_link_{safe_key}", on_click=handle_upcoming_click, args=(evt,))
            
            if st.session_state.upcoming_event_message == evt:
                st.markdown(f"<div style='color:#FFD700; font-size:18px; margin-top:-5px; margin-bottom:8px; font-style:italic; padding-left:18px;'>🕐 Coming soon ! no official information has been uploaded on this event yet</div>", unsafe_allow_html=True)

    if mic_clicked:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 200
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 1.5
        status_box = st.empty()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                status_box.info("🔴 Listening... Speak now!")
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=20)
            status_box.info("⏳ Transcribing...")
            text = recognizer.recognize_google(audio, language="en-IN")
            corrections = {
                "my oak": "Mayukh", "mayo": "Mayukh", "banas thali": "Banasthali", "up a g": "Aapaji",
                "vidula madan": "Vidula Maidan", "shilp mandir": "Shilp Mandir", "sadam": "Sadam"
            }
            for wrong, right in corrections.items():
                text = re.sub(r'(?i)\b' + wrong + r'\b', right, text)
            if text.strip():
                st.session_state.pending_msg = f"🗣️ {text}"
        except sr.UnknownValueError:
            st.session_state.mic_error = "🤷‍♀️ Didn't catch that. Please speak a bit louder!"
        except sr.WaitTimeoutError:
            st.session_state.mic_error = "⏰ Mic timed out. You didn't say anything."
        except sr.RequestError:
            st.session_state.mic_error = "🚫 Network Error connecting to Google Speech."
        except Exception as e:
            st.session_state.mic_error = f"❌ Voice error: {e}"
        st.session_state.mic_counter += 1
        st.rerun()

    if st.session_state.pending_msg:
        msg = st.session_state.pending_msg
        st.session_state.pending_msg = ""
        st.session_state.messages.append({"role": "user", "content": msg})
        with st.spinner("🤖 Thinking..."):
            bot_reply = get_bot_response(msg, st.session_state.messages)
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        if st.session_state.get("logged_in"):
            user_email = st.session_state.get("create_email")
            save_chat_to_db(user_email, msg, bot_reply)
        st.rerun()

def load_session_chat(session_id):
    try:
        conn = get_connection()
        user_email = st.session_state.get("create_email")
        query = "SELECT user_message, bot_response FROM chat_history WHERE session_id = %s AND email = %s ORDER BY chat_time ASC"
        df = pd.read_sql(query, conn, params=(session_id, user_email))
        conn.close()
        st.session_state.messages = []
        for _, row in df.iterrows():
            st.session_state.messages.append({"role": "user", "content": row['user_message']})
            st.session_state.messages.append({"role": "bot", "content": row['bot_response']})
        st.session_state.current_session_id = session_id
    except Exception as e:
        st.error(f"Error loading chat: {e}")

def show_history_page():
    def go_back_history():
        st.session_state.user_sub_page = "chat"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("⬅ Back", key="back_btn_history", type="secondary", on_click=go_back_history, use_container_width=True)

    st.title("📜 Your Chat History")

    c1, c2 = st.columns([3, 1])
    with c1:
        search_query = st.text_input("🔍 Search conversations...", placeholder="Type to search...", label_visibility="collapsed")
    with c2:
        if st.button("➕ New Chat", type="primary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.chat_title = None
            st.session_state.user_sub_page = "chat"
            st.rerun()

    user_email = st.session_state.get("create_email")
    if not user_email:
        st.error("Please login to view history.")
        return

    try:
        conn = get_connection()
        query = """
            SELECT ch.session_id, ch.chat_title, COALESCE(ch.is_pinned, 0) as is_pinned, ch.chat_time as chat_time
            FROM chat_history ch
            INNER JOIN (
                SELECT session_id, MIN(id) as first_id
                FROM chat_history WHERE email = %s GROUP BY session_id
            ) first_msgs ON ch.id = first_msgs.first_id
        """
        params = [user_email]
        if search_query.strip():
            query += " WHERE (ch.chat_title LIKE %s OR ch.user_message LIKE %s) AND ch.email = %s"
            params.extend([f"%{search_query.strip()}%", f"%{search_query.strip()}%", user_email])
        query += " ORDER BY is_pinned DESC, ch.chat_time DESC"
        df_sessions = pd.read_sql(query, conn, params=params)
        conn.close()

        if df_sessions.empty:
            if search_query: st.info("No chats match your search.")
            else: st.info("No past chats found!")
        else:
            for index, row in df_sessions.iterrows():
                session_id = row['session_id']
                is_pinned = bool(row['is_pinned'])
                title = row['chat_title'] if row['chat_title'] else 'Untitled Chat'
                with st.container(border=True):
                    if st.session_state.get(f"rename_mode_{session_id}"):
                        new_title = st.text_input("Rename Chat", value=title, key=f"rn_in_{session_id}", label_visibility="collapsed")
                        r1, r2, r3 = st.columns([1, 1, 4])
                        if r1.button("✅ Save", key=f"sv_{session_id}"):
                            cn = get_connection(); cr = cn.cursor()
                            cr.execute("UPDATE chat_history SET chat_title = %s WHERE session_id = %s", (new_title, session_id))
                            cn.commit(); cn.close()
                            st.session_state[f"rename_mode_{session_id}"] = False
                            st.rerun()
                        if r2.button("❌ Cancel", key=f"cn_{session_id}"):
                            st.session_state[f"rename_mode_{session_id}"] = False
                            st.rerun()
                    else:
                        col_a, col_b, col_dots = st.columns([6, 2, 1])
                        with col_a:
                            st.markdown(f"**{'📌 ' if is_pinned else ''}{title}**")
                            st.caption(f"🕒 {row['chat_time']}")
                        with col_b:
                            if st.button("Open ↗️", key=f"op_{session_id}", use_container_width=True):
                                load_session_chat(session_id)
                                st.session_state.current_session_id = session_id
                                st.session_state.chat_title = title
                                st.session_state.user_sub_page = "chat"
                                st.rerun()
                        with col_dots:
                            with st.popover("⋮"):
                                if st.button("Unpin" if is_pinned else "📌 Pin", key=f"p_{session_id}"):
                                    cn = get_connection(); cr = cn.cursor()
                                    cr.execute("UPDATE chat_history SET is_pinned = %s WHERE session_id = %s", (not is_pinned, session_id))
                                    cn.commit(); cn.close(); st.rerun()
                                if st.button("✏️ Rename", key=f"r_{session_id}"):
                                    st.session_state[f"rename_mode_{session_id}"] = True; st.rerun()
                                if st.button("🗑️ Delete", key=f"d_{session_id}"):
                                    cn = get_connection(); cr = cn.cursor()
                                    cr.execute("DELETE FROM chat_history WHERE session_id = %s", (session_id,))
                                    cn.commit(); cn.close(); st.rerun()
    except Exception as e:
        st.error(f"Database Error: {e}")

def handle_create_account():
    if st.session_state.create_step == "email":
        email_input = st.text_input("Enter your email", placeholder="Email", label_visibility="collapsed").strip().lower()
        
        if st.button("Send OTP", type="primary", use_container_width=True):
            if not email_input:
                st.warning("Please enter your email")
                return

            # --- STRICT EMAIL VALIDATION LOGIC ---
            # 1. Check Domain Restriction
            if not (email_input.endswith("@gmail.com") or email_input.endswith("@banasthali.in")):
                st.error("❌ Invalid Domain. Only @gmail.com or @banasthali.in addresses are allowed.")
                return

            # 2. Extract Username (part before @)
            username_part = email_input.split('@')[0]

            # 3. Check specific formatting rules:
            # UPDATED: Added '_' to the allowed character class [a-z0-9._]
            valid_format = re.match(r"^(?!\.)(?!.*\.\.)[a-z0-9._]{6,30}(?<!\.)$", username_part)
            
            # Logic check: If 8 or more characters, must have at least one letter [a-z]
            has_letter_if_long = True
            if len(username_part) >= 8:
                has_letter_if_long = any(c.isalpha() for c in username_part)

            if not valid_format or not has_letter_if_long:
                st.error("""
                    ❌ Invalid Email Format. 
                    - Must be 6–30 characters long (before @).
                    - Can include: Letters (a–z), Numbers (0–9), Periods (.), and Underscores (_).
                    - Cannot include: Spaces or other special characters (@, #, $, etc.).
                    - Cannot start or end with a dot (.).
                    - Cannot have consecutive dots (..).
                    - Usernames of 8 or more characters must include at least one letter.
                """)
                return

            # --- DATABASE CHECK (Only runs if email format is valid) ---
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE LOWER(TRIM(email)) = %s", (email_input,))
                if cursor.fetchone():
                    st.error("⚠️ User already exists. Please Login.")
                    return
            except Exception as e:
                st.error(f"Database Error: {e}")
                return
            finally:
                if 'conn' in locals():
                    conn.close()

            # --- SUCCESS: PROCEED TO SEND OTP ---
            st.session_state.create_otp = str(random.randint(100000, 999999))
            st.session_state.create_email = email_input
            send_email_otp(email_input, st.session_state.create_otp)
            st.session_state.create_step = "otp"
            st.success("OTP sent!")
            st.rerun()

    elif st.session_state.create_step == "otp":
        st.info(f"OTP sent to: {st.session_state.create_email}")
        otp = st.text_input("Enter the 6-digit OTP", placeholder="OTP", label_visibility="collapsed")
        if st.button("Verify OTP", type="primary", use_container_width=True):
            if otp == st.session_state.create_otp:
                st.session_state.create_step = "setpwd"
                st.success("✅ OTP Verified")
                st.rerun()
            else:
                st.error("❌ Incorrect OTP.")

    elif st.session_state.create_step == "setpwd":
        user_name = st.text_input("Full Name", placeholder="Full Name", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        pwd = st.text_input("Set password", type="password", placeholder="Set Password", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        cpwd = st.text_input("Confirm password", type="password", placeholder="Confirm Password", label_visibility="collapsed")
        
        if st.button("Create Account", type="primary", use_container_width=True):
            if not user_name:
                st.error("Name is required.")
            return
        if pwd != cpwd:
            st.error("❌ Passwords do not match")
            return
        if not is_valid_password(pwd):
            st.error("⚠️ Password must contain at least 7 characters...")
            return
    
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_name, email, password, status) VALUES (%s, %s, %s, 'Active')", 
               (user_name.strip(), st.session_state.create_email, pwd))
            conn.commit()
            st.success("🎉 Account created successfully!")

            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.session_state.user_name = user_name.strip()
            st.session_state.current_page = "home"
            st.session_state.create_step = "email"
            st.session_state.auth_mode = "login"
            st.session_state.user_sub_page = "chat"
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.show_splash = False  # ✅ ADD THIS LINE

            st.query_params["logged_in"] = "true"
            st.query_params["role"] = "user"
            st.query_params["email"] = st.session_state.create_email
            st.query_params["page"] = "home"  # ✅ ADD THIS LINE TOO

            st.rerun()
        except Exception as e:
            st.error(f"Database Error: {e}")
        finally:
            if 'conn' in locals():
                conn.close()

def handle_forgot_password():
    if st.session_state.forgot_step == "email":
        email_input = st.text_input("Enter your registered email", placeholder="Email", label_visibility="collapsed").strip().lower()
        
        if st.button("Send Verification Link", type="primary", use_container_width=True):
            if not email_input:
                st.warning("Please enter your email")
                return

            # --- STRICT VALIDATION LOGIC ---
            # 1. Check domain first
            if not (email_input.endswith("@gmail.com") or email_input.endswith("@banasthali.in")):
                st.error("❌ Invalid Domain. Only @gmail.com or @banasthali.in addresses are allowed.")
                return

            # 2. Extract the username part (before the @)
            username_part = email_input.split('@')[0]

            # 3. Apply Specific Constraints
            # UPDATED: Added '_' to the allowed characters [a-z0-9._]
            strict_regex = r"^(?!\.)(?!.*\.\.)[a-z0-9._]{6,30}(?<!\.)$"

            # 4. Check for at least one letter if length is 8 or more
            has_letter_if_long = True
            if len(username_part) >= 8:
                has_letter_if_long = any(c.isalpha() for c in username_part)

            if not re.match(strict_regex, username_part) or not has_letter_if_long:
                st.error("""
                    ❌ Invalid Email Format.
                    - Must be 6–30 characters long (before @).
                    - Can include: Letters (a–z), Numbers (0–9), Periods (.), and Underscores (_).
                    - Cannot include: Spaces or other special characters (@, #, $, etc.).
                    - Cannot start or end with a dot (.).
                    - Cannot have consecutive dots (..).
                    - Usernames of 8 or more characters must include at least one letter.
                """)
                return

            # --- DATABASE CHECK ---
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Check Users Table
                cursor.execute("SELECT * FROM users WHERE LOWER(TRIM(email)) = %s", (email_input,))
                
                if not cursor.fetchone():
                    st.error("❌ This email is not registered. Please sign up.")
                    return
                
                # Success: Proceed
                st.session_state.forgot_email = email_input
                st.session_state.forgot_step = "link_sent"
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if 'conn' in locals():
                    conn.close()

    elif st.session_state.forgot_step == "link_sent":
        st.success(f"✅ Link sent to {st.session_state.forgot_email}")
        if st.button("🔗 Simulate Clicking Email Link", type="secondary", use_container_width=True):
            st.session_state.forgot_step = "reset_password"
            st.rerun()

    elif st.session_state.forgot_step == "reset_password":
        new_pwd = st.text_input("New Password", type="password", placeholder="New Password", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        confirm_pwd = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed")
        
        if st.button("Change Password", type="primary", use_container_width=True):
            if new_pwd != confirm_pwd:
                st.error("❌ Passwords mismatch")
                return
            if not is_valid_password(new_pwd):
                st.error("⚠️ Password must contain at least 7 characters, an uppercase letter, a lowercase letter, a digit, and a special character.")
                return
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password = %s WHERE LOWER(TRIM(email)) = %s", (new_pwd, st.session_state.forgot_email))
                conn.commit()
                st.session_state.forgot_step = "reset_success"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if 'conn' in locals():
                    conn.close()

    elif st.session_state.forgot_step == "reset_success":
        st.success("✅ Password changed!")
        if st.button("Go to Login Page", type="secondary", use_container_width=True):
            st.session_state.forgot_step = "email"
            st.session_state.auth_mode = "login"
            st.rerun()
def show_admin_login():
    st.markdown('<div class="logo-container">🎓 Admin Portal</div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1.5, 1, 1.5])
    with col:
        with st.container(border=True):
            st.markdown("<h2 style='text-align:center; margin-bottom: 20px;'>Admin Login</h2>", unsafe_allow_html=True)
            adm_e = st.text_input("Admin Email", key="admin_email", placeholder="Email", label_visibility="collapsed")
            adm_p = st.text_input("Password", type="password", key="admin_password", placeholder="Password", label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login as Admin", type="primary", use_container_width=True):
                try:
                    conn = get_connection(); cursor = conn.cursor()
                    cursor.execute("SELECT * FROM admin WHERE TRIM(email) = %s AND TRIM(password) = %s", (adm_e.strip(), adm_p.strip()))
                    if cursor.fetchone():
                        st.session_state.role = "admin"; st.session_state.logged_in = True
                        st.session_state.create_email = adm_e.strip(); st.session_state.user_name = "Admin"
                        st.session_state.current_page = "admin_dashboard"
                        st.rerun()
                    else: st.error("❌ Invalid Admin Credentials")
                except Exception as e: st.error(f"Database Error: {e}")
            if st.button("Back to User Login", type="secondary", use_container_width=True):
                st.session_state.current_page = "login_main"; st.rerun()

@st.dialog("➕ Add New Event (Notice/Workshop)")
def add_workshop_dialog():
    st.markdown("Fill in the details for the new event below:")
    w_name = st.text_input("New Event Name", placeholder="e.g., AI Summit")
    categories = [
        "Tech", 
        "Cultural", 
        "Aesthetic", 
        "Physical", 
        "Practical", 
        "Moral", 
        "Literary", 
        "Social",
        "Upcoming Events" ,
        "Others"
    ]
    w_cat = st.selectbox("Category", categories)
    w_ven = st.text_input("Venue", placeholder="e.g., Lab 1")
    w_date = st.date_input("Event Date", date.today())
    w_time = st.text_input("Time", placeholder="e.g., 10:00 AM - 1:00 PM")
    if st.button("Add Event to Database", type="primary", use_container_width=True):
        if w_name.strip():
            try:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute("INSERT INTO workshops (workshop_name, category, venue, event_date, event_time) VALUES (%s, %s, %s, %s, %s)", (w_name.strip(), w_cat.strip(), w_ven.strip(), str(w_date), w_time.strip()))
                conn.commit(); conn.close(); st.rerun()
            except Exception as e: st.error(f"Error saving to database: {e}")
        else: st.warning("Event Name is required!")

def show_admin_dashboard():
    st.markdown("<h1 style='text-align:center; color:#00f7ff; font-weight:700;'>🧩 Eventify Admin Dashboard</h1>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<h2 style='color:#00deeb;'>🔗 Manage Forms & Links</h2>", unsafe_allow_html=True)
    try:
        conn = get_connection(); cursor = conn.cursor()
        cursor.execute("SELECT workshop_name FROM workshops ORDER BY id DESC")
        ws_names = [row[0] for row in cursor.fetchall()]; conn.close()
    except: ws_names = []

    with st.form("add_form_link"):
        st.write("Select an existing event, OR type a new one if it's not in the list:")
        c1, c2 = st.columns(2)
        with c1:
            f_event_dropdown = st.selectbox("Select Existing Event", ["-- Add Custom Event --"] + (ws_names if ws_names else []))
            f_event_custom = st.text_input("Or Type New Event Name", placeholder="e.g., Spring Fest 2026")
            f_date = st.date_input("Last Date to Register", date.today())
        with c2:
            f_link = st.text_input("Registration Link (Optional)", placeholder="https://forms.gle/...")
            f_qr = st.file_uploader("Upload QR Code/Poster (Optional)", type=['png', 'jpg', 'jpeg'])
            st.markdown("<br>", unsafe_allow_html=True)
            submit_form = st.form_submit_button("🔗 Save Form / Poster", use_container_width=True)

        if submit_form:
            final_event_name = f_event_custom.strip() if f_event_custom.strip() else f_event_dropdown
            if final_event_name != "-- Add Custom Event --" and (f_link or f_qr is not None):
                qr_b64 = ""; auto_link = f_link.strip()
                if f_qr is not None:
                    if not auto_link and CV2_AVAILABLE:
                        try:
                            file_bytes = np.asarray(bytearray(f_qr.read()), dtype=np.uint8)
                            img = cv2.imdecode(file_bytes, 1)
                            detector = cv2.QRCodeDetector()
                            data, bbox, _ = detector.detectAndDecode(img)
                            if data: auto_link = data; st.toast("🪄 Magic! Link automatically extracted from QR Code.")
                            f_qr.seek(0)
                        except: f_qr.seek(0)
                    qr_b64 = base64.b64encode(f_qr.read()).decode()
                try:
                    conn = get_connection(); cursor = conn.cursor()
                    cursor.execute("INSERT INTO event_forms (event_name, reg_link, deadline, qr_data) VALUES (%s, %s, %s, %s)", (final_event_name, auto_link, str(f_date), qr_b64))
                    conn.commit(); conn.close()
                    st.success(f"✅ Saved Form/Poster for {final_event_name} successfully!"); st.rerun()
                except Exception as e: st.error(f"Error saving to database: {e}")
            elif final_event_name == "-- Add Custom Event --" or not final_event_name: st.warning("Please provide an Event Name.")
            else: st.warning("Please provide either a Registration Link or a QR Code/Poster.")

    st.write("### 📋 Current Active Forms")
    try:
        conn = get_connection()
        df_forms = pd.read_sql("SELECT id, event_name, reg_link, deadline FROM event_forms ORDER BY id DESC", conn); conn.close()
        if not df_forms.empty:
            df_forms["Delete"] = False
            df_forms = df_forms[["Delete", "event_name", "reg_link", "deadline", "id"]]
            edited_f_df = st.data_editor(df_forms, use_container_width=True, hide_index=True,
                column_config={"id": None, "Delete": st.column_config.CheckboxColumn("Delete 🗑️", default=False),
                    "event_name": "Event Name", "reg_link": "Link URL", "deadline": "Deadline"},
                disabled=["id", "event_name", "deadline"])
            if st.button("💾 Save Form Deletions/Edits", type="primary", use_container_width=True):
                conn = get_connection(); cursor = conn.cursor()
                for _, row in edited_f_df.iterrows():
                    if row["Delete"]: cursor.execute("DELETE FROM event_forms WHERE id = %s", (row["id"],))
                    else: cursor.execute("UPDATE event_forms SET reg_link=%s WHERE id=%s", (row["reg_link"], row["id"]))
                conn.commit(); conn.close(); st.success("✅ Updated Forms Database!"); st.rerun()
        else: st.info("No forms added yet.")
    except: st.info("No forms added yet.")

    st.divider()
    st.markdown("<h2 style='color:#00deeb;'>📅 Manage Calendar Events</h2>", unsafe_allow_html=True)
    with st.form("add_event_form"):
        col1, col2 = st.columns(2)
        with col1:
            evt_name = st.text_input("Event Name (e.g., 'Makar Sankranti')")
            evt_cat = st.selectbox("Category", ["Holiday", "Academic", "Exam", "Special", "Vacation", "Upcoming"])
        with col2:
            evt_date = st.date_input("Event Date", date.today())
        if st.form_submit_button("➕ Add to Calendar"):
            # For "Upcoming" category, event name is not mandatory — use a default label if empty
            final_evt_name = evt_name.strip()
            if evt_cat == "Upcoming" and not final_evt_name:
                final_evt_name = f"Upcoming Event ({evt_date})"
            if not final_evt_name:
                st.error("❌ Please enter a valid Event Name.")
            elif save_event_to_db(final_evt_name, evt_date, evt_cat):
                st.session_state["calendar_events"] = load_events_from_db()
                st.success(f"✅ Permanently saved '{final_evt_name}' for {evt_date}"); st.rerun()
            else: st.error("Failed to save event.")

    st.write("### 📋 Currently Saved in Database:")
    try:
        conn = get_connection()
        df_cal = pd.read_sql("SELECT id, event_name, event_date, category FROM calendar_events ORDER BY event_date ASC", conn)
        conn.close()
        
        if not df_cal.empty:
            df_cal["Delete"] = False
            df_cal = df_cal[["Delete", "event_name", "category", "event_date", "id"]]
            df_cal['event_date'] = pd.to_datetime(df_cal['event_date']).dt.date
            
            edited_cal = st.data_editor(df_cal, use_container_width=True, hide_index=True,
                column_config={"id": None, "Delete": st.column_config.CheckboxColumn("Delete 🗑️", default=False),
                    "event_name": "Event Name", "category": "Category", "event_date": st.column_config.DateColumn("Date")},
                disabled=["id"])
                
            if st.button("💾 Save Calendar Changes", type="primary", use_container_width=True):
                conn = get_connection(); cursor = conn.cursor()
                for _, row in edited_cal.iterrows():
                    if row["Delete"]:
                        cursor.execute("DELETE FROM calendar_events WHERE id = %s", (row["id"],))
                    else:
                        e_n = str(row.get("event_name", "")).strip()
                        c_t = str(row.get("category", "")).strip()
                        e_d = row.get("event_date", None)
                        if pd.isna(e_d): 
                            e_d = None
                        else: 
                            e_d = str(e_d)
                        cursor.execute("UPDATE calendar_events SET event_name=%s, category=%s, event_date=%s WHERE id=%s", (e_n, c_t, e_d, row["id"]))
                        
                conn.commit(); conn.close()
                st.session_state["calendar_events"] = load_events_from_db()
                st.success("✅ Updated Calendar Database!"); st.rerun()
        else:
            st.info("No calendar events added yet.")
    except Exception as e:
        st.error(f"Error loading calendar events: {e}")

    st.divider()
    st.markdown("<h2 style='color:#00deeb;'>📰 Manage Notices (Workshops)</h2>", unsafe_allow_html=True)
    if st.button("➕ Add New Event (Notice/Workshop)", type="primary", use_container_width=True):
        add_workshop_dialog()

    st.write("✏️ **To Edit:** Click directly on any text to change it.  \n🗑️ **To Delete:** Check the box in the 'Delete' column.  \n💾 Click **Save Changes** below when you are done.")
    try:
        conn = get_connection()
        df_workshops = pd.read_sql("SELECT id, workshop_name, category, venue, event_date, event_time FROM workshops ORDER BY event_date DESC, id DESC", conn); conn.close()
    except Exception as e:
        df_workshops = pd.DataFrame(columns=["id", "workshop_name", "category", "venue", "event_date", "event_time"])

    if not df_workshops.empty:
        df_workshops["Delete"] = False
        cols = ["Delete", "workshop_name", "category", "venue", "event_date", "event_time", "id"]
        df_workshops = df_workshops[cols]
        df_workshops['event_date'] = pd.to_datetime(df_workshops['event_date']).dt.date
        edited_df = st.data_editor(df_workshops, use_container_width=True, hide_index=True,
            column_config={"id": None, "Delete": st.column_config.CheckboxColumn("Delete 🗑️", default=False),
                "workshop_name": "Event Name", "category": "Category", "venue": "Venue",
                "event_date": st.column_config.DateColumn("Date"), "event_time": "Time"},
            disabled=["id"])
        if st.button("💾 Save Notices Changes", type="primary", use_container_width=True):
            try:
                conn = get_connection(); cursor = conn.cursor()
                for _, row in edited_df.iterrows():
                    r_id = row["id"]
                    if row["Delete"]: cursor.execute("DELETE FROM workshops WHERE id = %s", (r_id,))
                    else:
                        w_n = str(row.get("workshop_name", "")).strip(); c_n = str(row.get("category", "")).strip()
                        v_n = str(row.get("venue", "")).strip(); e_d = row.get("event_date", None)
                        if pd.isna(e_d): e_d = None
                        else: e_d = str(e_d)
                        e_t = str(row.get("event_time", "")).strip()
                        cursor.execute("UPDATE workshops SET workshop_name=%s, category=%s, venue=%s, event_date=%s, event_time=%s WHERE id=%s", (w_n, c_n, v_n, e_d, e_t, r_id))
                conn.commit(); conn.close(); st.success("✅ Database Updated!"); st.rerun()
            except Exception as e: st.error(f"Failed: {e}")

    st.divider()
    st.markdown("<h2 style='color:#00deeb;'>📂 Backend Database View</h2>", unsafe_allow_html=True)

    if st.button("Open Database Tables"):
        try:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            st.session_state["db_tables"] = [t[0] for t in cursor.fetchall()]; conn.close()
        except Exception as e: st.error(f"Failed: {e}")

    if "db_tables" in st.session_state:
        selected_table = st.selectbox("Table:", st.session_state["db_tables"])
        if st.button("Show Data"):
            conn = get_connection()
            df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
            st.dataframe(df, use_container_width=True, hide_index=True); conn.close()
def show_welcome_page():
    img_b64 = ""
    try:
        import os, base64
        img_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
    except:
        pass

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Outfit:wght@800&display=swap');
            
            .stApp {{
                background-color: #000000 !important;
            }}
            
            /* TRUE IMAGE LAYER: The exact logo restored natively as a centralized icon, perfectly uncut and un-stretched */
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background-image: url("data:image/jpeg;base64,{img_b64}");
                background-size: contain !important; /* Forces the image to behave like a standard localized logo without stretching into a generic picture background */
                background-position: center;
                background-repeat: no-repeat;
                filter: brightness(0.5); /* Keeps true colors while allowing the white text to pierce */
                z-index: -1 !important; 
            }}
            
            [data-testid="stSidebar"] {{ display: none !important; }}
            header[data-testid="stHeader"] {{ display: none !important; }}
            
            .block-container {{
                position: relative; 
                z-index: 10 !important;
                padding-top: 5vh !important;
            }}
            
            @keyframes intenseWhiteGlow {{
                0% {{ opacity: 0; filter: blur(5px); transform: scale(1.1); text-shadow: 0 0 0px transparent; }}
                100% {{ 
                    opacity: 1; 
                    filter: blur(0px); 
                    transform: scale(1); 
                    text-shadow: 
                        0 0 10px rgba(255, 255, 255, 0.8),
                        0 0 20px rgba(255, 255, 255, 0.6),
                        0 0 40px rgba(255, 255, 255, 0.4) !important;
                }}
            }}
            
            .welcome-wrap {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                width: 100%;
                margin-top: 25vh !important;
                margin-bottom: 25px !important;
            }}
            
            h1.welcome-banner {{ 
                font-family: 'Montserrat', sans-serif;
                font-size: clamp(40px, 6.5vw, 100px) !important; 
                font-weight: 900;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 5px;
                color: #FFFFFF !important;
                -webkit-text-fill-color: #FFFFFF !important; /* Forces strict white regardless of Streamlit theme */
                animation: intenseWhiteGlow 2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
                padding: 0;
            }}
            
            /* Clean up any stButton layout overrides to let Streamlit Columns naturally center it */
            div.stButton {{
                width: 100% !important;
                text-align: center;
            }}
            
            div.stButton > button[kind="primary"] {{
                height: 65px !important;
                font-family: 'Outfit', sans-serif !important;
                font-size: 22px !important;
                font-weight: 800 !important;
                border-radius: 50px !important;
                background: rgba(0, 0, 0, 0.4) !important;
                color: #FFFFFF !important;
                border: 2px solid rgba(255, 255, 255, 0.8) !important;
                backdrop-filter: blur(10px);
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.6) !important;
                letter-spacing: 4px;
                text-transform: uppercase;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}
            div.stButton > button[kind="primary"]:hover {{
                box-shadow: 0px 15px 40px rgba(255, 255, 255, 0.8) !important;
                transform: scale(1.05) translateY(-4px) !important;
                background: rgba(255, 255, 255, 0.15) !important;
                border-color: #ffffff !important;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="welcome-wrap"><h1 class="welcome-banner">WELCOME TO EVENTIFY</h1></div>', unsafe_allow_html=True)
    
    # Use tightly squeezed external columns to fundamentally FORCE the middle column to absolute dead center
    _, col, _ = st.columns([2, 1.5, 2])
    with col:
        # use_container_width=True forces the button to fill the correctly-centered column, completely stopping leftward drifting
        if st.button("GET STARTED", type="primary", key="start_btn", use_container_width=True):
            st.session_state.show_splash = False
            st.rerun()
def main():
    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state.db_initialized = True

    init_session_state()

    # --- LANDING PAGE GATEKEEPER ---
    if st.session_state.get("show_splash", True):
        show_welcome_page()
        return 
    # -------------------------------

    url_page = st.query_params.get("page")
    if url_page and url_page != st.session_state.current_page:
        st.session_state.current_page = url_page

    if st.session_state.get("logged_in"):
        user_name = st.session_state.get("user_name", "User").title()
        
        # Load the logo dynamically to use as the user avatar badge
        logo_b64 = ""
        try:
            import os, base64
            img_path = os.path.join(os.path.dirname(__file__), "logo.jpg")
            with open(img_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
        except:
            pass
            
        if logo_b64:
            avatar_html = f'<div class="user-avatar" style="background-image: url(data:image/jpeg;base64,{logo_b64}); background-size: cover; background-position: center;"></div>'
        else:
            initial = user_name[0].upper() if user_name else "U"
            avatar_html = f'<div class="user-avatar">{initial}</div>'

        st.markdown(f'''<div class="user-profile-badge">{avatar_html}<div class="user-name">{user_name} ▼</div></div>''', unsafe_allow_html=True)

        # Check for logout query param
        if st.query_params.get("logout") == "true":
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.current_page = "home"
            st.session_state.messages = []
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.show_splash = True # Reset for next time
            st.query_params.clear()
            st.rerun()

        # The hidden span enables the global CSS to target the element IMMEDIATELY following it as the dropdown
        st.markdown('<span class="top-right-logout-btn" style="display:none;"></span>', unsafe_allow_html=True)
        # The hyperlink itself mimicking the button's style
        st.markdown('''
            <a href="/?logout=true" target="_self" style="
                display: block; 
                width: 100%; 
                text-decoration: none; 
                text-align: center; 
                cursor: pointer; 
                font-family: 'Inter', sans-serif;
                background-color: transparent; 
                color: #FF3B30; 
                font-size: 15px; 
                font-weight: 700; 
                padding: 8px; 
                transition: 0.2s;" 
                onmouseover="this.style.backgroundColor='rgba(255, 59, 48, 0.1)'; this.style.borderRadius='8px';" 
                onmouseout="this.style.backgroundColor='transparent'; this.style.borderRadius='0px';">
                Logout
            </a>
        ''', unsafe_allow_html=True)

    if st.session_state.logged_in and st.session_state.role == "admin":
        show_admin_dashboard()
        return

    if st.session_state.current_page == "home":
        show_user_dashboard()
        
    elif st.session_state.current_page == "login_main":

        st.markdown('<div class="logo-container">🎓 Eventify 🔗</div>', unsafe_allow_html=True)
        st.markdown("""
        <style>
        div.stButton > button[kind="tertiary"] {
            font-size: 22px !important; padding: 0 !important; background: transparent !important;
            color: #00A0DC !important; border: none !important; box-shadow: none !important;
            min-height: unset !important; height: auto !important; line-height: 1.2 !important;
            margin: 0 !important; text-decoration: underline !important;
        }
        div.stButton > button[kind="tertiary"] p { font-size: 22px !important; margin: 0 !important; }
        div.stButton > button[kind="tertiary"]:hover { color: #FFFFFF !important; text-decoration: underline !important; }
        
        /* Adjust alignment for the "Don't have an account" row without harsh negative margins */
        [data-testid="column"]:has(button[kind="tertiary"]) {
            display: flex;
            align-items: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        _, col, _ = st.columns([1.2, 1.0, 1.2]) # Slimmer
        with col:
            with st.container(border=True):
                if st.session_state.auth_mode == "login":
                    st.markdown("<h2 style='text-align:center; margin-bottom: 20px;'>Login</h2>", unsafe_allow_html=True)
                    email = st.text_input("Email", placeholder="Email", label_visibility="collapsed")
                    st.markdown("<br>", unsafe_allow_html=True)
                    password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Login", type="primary", use_container_width=True): handle_login(email, password)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.write("") # spacer before forgot password
                    c_fp1, c_fp2, c_fp3 = st.columns([1, 1, 1])
                    with c_fp2:
                        if st.button("Forgot Password?", type="tertiary", use_container_width=True): go_to("forgot_password")
                    
                    c_text, c_btn = st.columns([1.3, 1])
                    with c_text: st.markdown("<div style='text-align:right; font-size:19px; color:#c7c7c7; margin-top:2px; margin-right:-15px;'>Don't have an account?</div>", unsafe_allow_html=True)
                    with c_btn:
                        if st.button("Sign up", type="tertiary", key="trigger_signup"):
                            st.session_state.auth_mode = "signup"; st.rerun()
                            
                    st.markdown("<hr style='margin: 15px 0px; border-color: #2D5A5C;'>", unsafe_allow_html=True)
                    if st.button("Back to Chat", type="primary", use_container_width=True):
                        st.session_state.current_page = "home"; st.rerun()

                elif st.session_state.auth_mode == "signup":
                    st.markdown("<h2 style='text-align:center; margin-bottom: 20px;'>Sign Up</h2>", unsafe_allow_html=True)
                    handle_create_account()
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    c_text, c_btn = st.columns([1.3, 1])
                    with c_text: st.markdown("<div style='text-align:right; font-size:19px; color:#c7c7c7; margin-top:2px; margin-right:-15px;'>Already have an account?</div>", unsafe_allow_html=True)
                    with c_btn:
                        if st.button("Login", type="tertiary", key="trigger_login"):
                            st.session_state.auth_mode = "login"; st.rerun()
                            
                    st.markdown("<hr style='margin: 15px 0px; border-color: #2D5A5C;'>", unsafe_allow_html=True)
                    if st.button("Back to Chat", type="primary", use_container_width=True):
                        st.session_state.current_page = "home"; st.rerun()
        
    elif st.session_state.current_page == "forgot_password":
        st.markdown('<div class="logo-container">🎓 Eventify</div>', unsafe_allow_html=True)
        _, col, _ = st.columns([0.8, 1.5, 0.8])
        with col:
            with st.container(border=True):
                st.markdown("<h2 style='text-align:center; margin-bottom: 20px;'>Forgot Password</h2>", unsafe_allow_html=True)
                handle_forgot_password()
                if st.session_state.forgot_step != "reset_success":
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Back to Login", type="tertiary", use_container_width=True):
                        st.session_state.forgot_step = "email"; go_to("login_main")

# The final execution call
if __name__ == "__main__":
    main()
