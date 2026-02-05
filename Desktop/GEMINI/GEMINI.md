# EcoTrack - Energy Dashboard

## Project Overview

This project is an energy and air quality monitoring dashboard called "EcoTrack". It consists of a Python/Flask backend that serves a RESTful API and a vanilla HTML/CSS/JavaScript frontend that consumes the API to display data. The project is designed to monitor and visualize data from Tuya smart devices and air quality sensors.

**Key Technologies:**

*   **Backend:** Python, Flask, Flask-CORS, SQLite, `tuya-connector-python`, `requests`
*   **Frontend:** HTML, CSS, JavaScript, Chart.js
*   **Database:** SQLite (`ecotrack.db`)

**Architecture:**

*   **Backend:** A Flask application (`backend/app.py`) provides a RESTful API to store and retrieve data from a SQLite database. It has endpoints for AQI (Air Quality Index) and electricity consumption data.
*   **Frontend:** A single-page dashboard (`frontend/index.html`) that uses JavaScript (`frontend/script.js`) to fetch data from the backend API and visualize it using Chart.js.
*   **Data Integration:** The backend is set up to receive data from Tuya devices and AQI sensors, though the scripts for data ingestion (`tuya_integration.py`, `aqi_integration.py`) are not fully analyzed here.

## Building and Running

### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd Mini_project/backend
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the backend server:**
    ```bash
    python app.py
    ```
    The server will start on `http://localhost:5000`.

### Frontend

1.  **Open the `index.html` file in your web browser:**
    *   You can typically do this by double-clicking the file or using a command like:
        ```bash
        xdg-open Mini_project/frontend/index.html
        ```
        (on Linux) or `open Mini_project/frontend/index.html` (on macOS).

## Development Conventions

*   **Backend:** The backend follows a simple Flask application structure.
    *   The main application logic is in `app.py`.
    *   The database is a single SQLite file (`ecotrack.db`).
    *   The database schema is initialized automatically when the application starts.
*   **Frontend:**
    *   The frontend is a single HTML file with a corresponding CSS and JavaScript file.
    *   Chart.js is used for all data visualizations.
    *   The frontend fetches data from the backend API every 30 seconds to refresh the dashboard.
*   **API:**
    *   The API is documented at the root endpoint (`/`).
    *   The API returns JSON responses with a `status` field (`success` or `error`).
