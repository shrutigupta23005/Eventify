# 🎓 Eventify — University Event & Chatbot Platform

**Eventify** is a smart university portal built with **Streamlit** that helps students of Banasthali Vidyapith explore clubs, fests, events, and campus life — powered by an AI chatbot.

## ✨ Features
-  **AI Chatbot** — Powered by Groq (LLaMA 3), answers questions about clubs, fests, events, and campus policies
- **Event Calendar** — View and track upcoming workshops and university events
- **Campus Maps** — GPS navigation to key university locations
- **Clubs Directory** — Browse all official and non-official university clubs
- **Event Registration Forms** — Quick access to event registration links
- **Five-Fold Education** — Physical, Aesthetic, Practical, Moral, and Service activities
- **User Authentication** — Secure login, signup, OTP verification & forgot password
- **Admin Panel** — Manage events, notices, and registration forms

##  Tech Stack
- **Frontend & Backend**: Streamlit (Python)
- **Database**: MySQL
- **AI**: Groq API (LLaMA 3.1 8B Instant)
- **Email**: Gmail SMTP (OTP verification)

##  Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/shrutigupta23005/eventify.git
cd eventify
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your actual values:
- `GROQ_API_KEY` — Get from [console.groq.com](https://console.groq.com)
- `DB_PASSWORD` — Your MySQL root password
- `EMAIL_ADDRESS` & `EMAIL_PASSWORD` — Gmail + App Password

### 4. Set up the database
Import the SQL file into MySQL:
```bash
mysql -u root -p university_chatbot < university_chatbot.sql
```

### 5. Run the app
```bash
streamlit run page.py
```

## 📁 Project Structure
```
├── page.py              # Main application (all pages)
├── clubs.py             # Clubs directory page
├── theme.py             # UI theme & styling
├── db_config.py         # DB connection helper
├── aesthetic.py         # Aesthetic activities page
├── physical.py          # Physical activities page
├── practical.py         # Practical activities page
├── moral.py             # Moral activities page
├── dance.py / music.py  # Certificate course pages
├── craft.py / tech.py   # Certificate course pages
├── languagecd.py        # Language courses page
├── massmedia.py         # Media courses page
├── train_bot.py         # Chatbot training utilities
├── locations.json       # Campus map location data
├── university_chatbot.sql # Database schema & seed data
├── .env.example         # Environment variable template
└── background/          # Background images
```

##  Environment Variables
Never commit your `.env` file. Use `.env.example` as a reference.

## 📜 License
This project was developed as a 3rd year university project.
