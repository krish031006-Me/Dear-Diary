# Dear-Diary
This is our project repo for WeMakeDevs FutureStack GenAI Hackathon.

dearDiary 📝✨
dearDiary is a smart mental health journaling application designed to help users track their emotional well-being through insightful analysis and AI-powered reflections. It provides a safe and private space to pen down thoughts, and in return, offers a deeper understanding of one's emotional patterns over time.

🚀 Introduction
In our fast-paced world, taking a moment for introspection is more important than ever. dearDiary is more than just a digital notebook; it's a personal mental wellness companion. By leveraging the power of a Large Language Model (Llama-3), it performs two key functions:

Real-time Reflection: Our AI assistant, Aura, provides live, empathetic feedback as you write, helping you explore your thoughts without giving direct advice.

Deep Emotional Analysis: After you save an entry, the AI performs a detailed analysis to extract key emotional metrics, which are then used to power your personal analytics dashboard.

✨ Features
Secure User Authentication: Safe and secure registration and login system with password hashing to ensure your journal remains private.

Dual AI System:

Live Reflections: Get real-time, thoughtful feedback from Aura, our integrated AI coach, as you write.

In-depth Analysis: Upon saving, entries are analyzed to identify primary emotions, sentiment scores, emotional intensity, and potential triggers.

Emotional Analytics Dashboard: Visualize your emotional journey with interactive charts:

Line Chart: Track your emotional intensity over time.

Bar Chart: See the frequency of different emotions (Happy, Sad, Angry, etc.).

Doughnut Chart: Understand the proportion of each emotion in your overall mood.

Intuitive Writing Space: A beautiful, distraction-free two-page layout that mimics a real diary.

Entry History: Easily browse, read, and revisit your past journal entries.

Demo Mode: New users can explore a demo dashboard to see the powerful analytics in action before signing up.

🛠️ Technologies Used
This project is built with a modern and robust stack:

Backend: Python, Flask, Werkzeug

Frontend: HTML, CSS, JavaScript, Jinja2

Database: SQLite (with the CS50 SQL library)

AI / LLM: Llama-3.3-70b via Cerebras API

Data Visualization: Chart.js

Deployment: Docker (optional)

📁 Project Structure
The project is organized into several key files that separate concerns:

/
├── app.py              # Main Flask application, handles all routes and logic.
├── reflection.py       # Contains all functions for AI interaction (reflection & analysis).
├── helpers.py          # Utility functions (e.g., login_required decorator, hashing).
├── users.db            # SQLite database file.
├── requirements.txt    # List of all Python dependencies.
├── schema.sql          # SQL commands to initialize the database schema.
│
├── static/
│   ├── style.css       # All CSS styles for the application.
│   └── script.js       # Core JavaScript for UI interactions and API calls.
│   └── charts.js       # JavaScript for rendering charts on the dashboard.
│
└── templates/
    ├── layout.html     # Base HTML template with header and navigation.
    ├── dashboard.html  # Main dashboard with charts.
    ├── login.html      # User login page.
    ├── register.html   # User registration page.
    ├── space.html      # The diary writing interface.
    └── ...             # Other HTML files.
