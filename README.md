🎢 Rollercoaster Tracker - Flask Web Application
🚀 Overview

Rollercoaster Tracker is a Flask-based web application that allows users to track rollercoasters they've ridden, maintain a wishlist of coasters they want to ride, view the average ratings for coasters, and check the weather forecasts for amusement parks. Users can register, log in, and maintain their personal coaster list while contributing to a global leaderboard ranking coasters based on popularity and reviews.
🌟 Features

    User Authentication: Sign up, log in, and securely manage accounts using Flask-Login and Flask-Bcrypt.
    Coaster Tracking: Users can add rollercoasters to their personal list, mark them as "ridden" or "wishlist."
    Global Ratings: Displays average ratings based on all user reviews.
    Weather Integration: Fetches real-time 7-day weather forecasts for amusement parks using the OpenWeatherMap API.
    Leaderboard: Shows the most popular and highest-rated rollercoasters based on user reviews.
    Database Management: Stores coasters and user data using Flask-SQLAlchemy.
    CSV Import: Automatically populates the database with rollercoaster data from a CSV file.
    Responsive UI: Uses Bootstrap for a mobile-friendly experience.

🛠️ Tech Stack
Technology	Purpose
Python (Flask)	Web framework
Flask-Login	User authentication
Flask-SQLAlchemy	ORM for database management
Flask-WTF	Form handling
Bootstrap	Frontend styling
OpenWeatherMap API	Weather forecasts
SQLite / PostgreSQL	Database
WTForms	Form validation
Jinja2	Templating engine
📸 Screenshots

🔹 Include some screenshots of your app's interface here.
🔧 Installation & Setup
1️⃣ Clone the Repository

git clone https://github.com/yourusername/rollercoaster-tracker.git
cd rollercoaster-tracker

2️⃣ Create & Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up the Database

python init_db.py  # Initializes the database
python populate_db.py  # Populates the database with coaster data

5️⃣ Set Up API Keys 

Create a .env file and add your OpenWeatherMap API key:

WEATHER_API_KEY=your_api_key_here

6️⃣ Run the Application

python app.py

Then open http://127.0.0.1:5000 in your browser.
📜 API Integration

This project integrates the OpenWeatherMap API for real-time weather forecasts. To enable this feature:

    Get a free API key from OpenWeatherMap.
    Add it to your .env file or update the WEATHER_API_KEY variable in routes.py.

💡 Future Enhancements

    🌎 Deploy to the cloud (Heroku/Render).
    📊 Advanced analytics & ride stats for users.
    🏆 Badges & achievements for tracking progress.
    🔔 Notifications for upcoming park events.
    📍 Map integration to visualize coasters worldwide.

