# Rollercoaster Tracker

Rollercoaster Tracker is a web application that allows users to track rollercoasters they have ridden, want to ride, and view weather forecasts for their favorite amusement parks.

## Features

- User Registration and Login
- Track Rollercoasters by Park
- Mark Rollercoasters as Ridden
- View and Search Rollercoasters
- Weather Forecast for Amusement Parks

## Technologies Used

- Flask (Python web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (User session management)
- WTForms (Form handling)
- OpenWeatherMap API (Weather data)
- HTML, CSS, Bootstrap (Frontend)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On MacOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the database**:

    ```bash
    python init_db.py
    ```

6. **Populate the database with rollercoasters**:

    ```bash
    python populate_db.py
    ```

7. **Run the application**:

    ```bash
    python app.py
    ```

8. **Access the application**:

    Open your web browser and go to `http://127.0.0.1:5000`

## Usage

- Register a new account or log in with an existing account.
- Add rollercoasters to your tracker by entering the park and coaster details.
- View all rollercoasters, search by park, and mark coasters as ridden.
- Check the weather forecast for your favorite parks.

## Configuration

To use the weather feature, you need an API key from OpenWeatherMap. Add your API key to the `config.py` file:

```python
# config.py
WEATHER_API_KEY = 'your_openweathermap_api_key'
