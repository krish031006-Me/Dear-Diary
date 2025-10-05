# Dear Diary 📝

Dear Diary is a personal journaling web application that helps users track their thoughts, emotions, and daily reflections. Using AI analysis, it provides insights into mood patterns over time and visualizes trends with interactive charts.

---

## Features

- **User Accounts**: Secure sign-up and login functionality.
- **Daily Journaling**: Write reflections, thoughts, or experiences.
- **AI Mood Analysis**: Automatically analyze entries for primary emotions and triggers.
- **Pattern Visualization**: Display mood trends over time using interactive charts.
- **Responsive Design**: Works well on desktop and mobile devices.

---

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: SQLite
- **AI Integration**: LLMs for mood analysis (Cerebras / OpenAI models)
- **Session Management**: Flask-Session

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/dear-diary.git
   cd dear-diary
   ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app**
    ```bash
    python app.py
    ```
    Open http://127.0.0.1:5000 in your browser.

4. **Usage**
    Sign up or log in with your account.    
    Add daily journal entries.
    Let AI analyze your mood and emotions.
    Check your dashboard for mood patterns and insights.

**Project Structure**

    dear-diary/
    ├── app.py                # Main Flask application
    ├── helpers.py            # Contains the helper function 
    ├── reflection.py         # Contains the AI logic
    ├── templates/            # HTML templates
    ├── static/
    │   ├── style.css             # CSS files
    │   └── script.js             # main JS file
    │   └── demo.js               # for demo JS graphs
    │   └── charts.js             # for dynamic chart JS graphs
    ├── requirements.txt      # Python dependencies
    └── README.md             # Project documentation

**AI Mood Analysis**

    The AI model reads journal entries and extracts:
    Primary emotion (happy, sad, angry, etc.)
    Triggers or key topics
    Overall mood pattern over time
    These insights are displayed in the dashboard as interactive charts for easy visualization.

**Future Improvements**

    Add emotion-based reminders or notifications.
    Integrate with mobile apps.
    Enable exporting journals as PDFs.
    Add sentiment comparison between entries over weeks/months.
    Share the diaries with other user.

**License**

    This project is licensed under the MIT License.

**Author**

    Code Catalysts ~ Krish, Sahil, Hardik
    Computer Science Engineering Student
    Passionate about programming, AI, and web development
