Weather Data App
This is a simple and interactive weather data application built with Streamlit. The app fetches real-time weather data, stores it in a PostgreSQL database, and displays it using engaging visualizations.

Features
Interactive Weather Trends: Visualize temperature trends over time for selected cities.
Weather Trivia Quiz: Test your knowledge with fun and educational weather trivia questions.
Prerequisites
Python 3.6 or higher
Streamlit
Pandas
SQLAlchemy
Plotly
PostgreSQL
Requests
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/weather-data-app.git
cd weather-data-app
Install the required Python packages:

bash
Copy code
pip install streamlit pandas sqlalchemy plotly psycopg2-binary requests
Set up your PostgreSQL database and configure your connection details.

Running the App
Navigate to the project directory:

bash
Copy code
cd weather-data-app
Run the Streamlit app:

bash
Copy code
streamlit run streamlit_app.py