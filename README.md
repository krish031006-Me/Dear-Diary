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

⚙️ Getting Started
To get a local copy up and running, follow these simple steps.

Prerequisites
Python 3.8+

pip (Python package installer)

Installation & Setup
Clone the repository:

Bash

git clone https://github.com/your-username/dearDiary.git
cd dearDiary
Set up your Cerebras API Key:
Create a file named .env in the root of the project directory. Add your API key to this file.

CEREBRAS_API_KEY="your-secret-api-key-goes-here"
The reflection.py file is already configured to load this key.

Create and activate a virtual environment:

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
Install Python dependencies:

Bash

pip install -r requirements.txt
Initialize the database:
Run the following command in your terminal to create the users.db file and set up all the necessary tables using the schema.sql file.

Bash

sqlite3 users.db < schema.sql
Running the Application
Start the Flask server:

Bash

flask run
Open your browser and navigate to http://127.0.0.1:5000 to see the application in action!

🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

requirements.txt
Plaintext

Flask
Flask-Session
cs50
Werkzeug
cerebras-cloud-sdk
schema.sql
SQL

CREATE TABLE "users" (
    "user_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "status" TEXT DEFAULT 'done'
);

CREATE TABLE "entries" (
    "entry_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "entry" TEXT NOT NULL,
    "written_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "date_only" DATE DEFAULT (date('now')),
    FOREIGN KEY ("user_id") REFERENCES "users" ("user_id")
);

CREATE TABLE "analysis" (
    "analysis_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "analysis" TEXT, -- Storing the JSON as TEXT
    "date_created" DATE DEFAULT (date('now')),
    FOREIGN KEY ("user_id") REFERENCES "users" ("user_id")
);

CREATE TABLE "recent_summary" (
    "summary_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "email" TEXT NOT NULL,
    "summary" TEXT,
    "date_summarized" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("user_id") REFERENCES "users" ("user_id")
);