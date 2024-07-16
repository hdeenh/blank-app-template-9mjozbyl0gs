import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import os
import requests

# Database connection details from Streamlit secrets
HOST = st.secrets['DB_HOST']
PORT = st.secrets['DB_PORT']
NAME = st.secrets['DB_NAME']
USER = st.secrets['DB_USER']
PASS = st.secrets['DB_PASS']

# Function to create a connection to the PostgreSQL database
def create_engine_connection():
    # Create the engine URL
    engine_url = f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}'
    # Create and return the engine
    engine = create_engine(engine_url)
    return engine

# Function to fetch the most recent weather data from the database
def fetch_data(engine):
    # SQL query to select data
    query = 'SELECT * FROM student."Deens_weather" ORDER BY observation_time DESC, city ASC LIMIT 15;'
    # Execute the query and return the DataFrame
    df = pd.read_sql_query(query, engine)
    return df

# Function to fetch temperature data for a specific city
def fetch_temperature_data(engine, city):
    # SQL query to select data for the specified city
    query2 = f'SELECT observation_time, temperature, wind_speed, pressure, humidity FROM student."Deens_weather" WHERE city = \'{city}\' ORDER BY observation_time'
    # Execute the query and return the DataFrame
    df2 = pd.read_sql_query(query2, engine)
    return df2

###############################################################################################################################

# Main function for the Streamlit application
def main():
    # Display an image at the top of the app
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo6lCF19a-hKONJB6oyYs6rKA63bKln9O7dg&s")
    # Note: There is no st.logo function in Streamlit, so this line will be commented out
    # st.logo("https://www.creativefabrica.com/wp-content/uploads/2021/03/31/weather-icon-illustration03-Graphics-10205167-1.jpg")

    # Create a connection to the database
    engine = create_engine_connection()

    # Fetch the most recent weather data
    data = fetch_data(engine)

    # Dropdown menu to select a city
    city = st.selectbox("Select City", ["New York", "London", "Tokyo", "Dubai", "Cape Town", "Paris", "Mexico city", "Shanghai", "Cairo", "Lagos", "São Paulo", "Mumbai", "Moscow", "Istanbul", "Seoul"])
    # Dropdown menu to select a weather parameter
    params = st.selectbox("Select weather parameter", ["temperature", "wind_speed", "humidity", "pressure"])
    # Fetch temperature data for the selected city
    data2 = fetch_temperature_data(engine, city)

    # Display a line chart of the selected weather parameter over time for the selected city
    if not data2.empty:
        fig = px.line(data2, x='observation_time', y=f'{params}', title=f'{params} Trend in {city}')
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {city}.")

    # Display the most recent weather data in a table
    st.markdown(""":blue[**Most recent weather data:**]""")
    st.dataframe(data)

    # Display a scatter plot of temperature vs humidity, colored by city
    st.markdown(""":blue[**Scatter Graph 📊**]""")
    fig = px.scatter(data, x='temperature', y='humidity', color='city', hover_name='city')
    st.plotly_chart(fig)

    # Weather trivia quiz section
    st.markdown("### Weather Trivia Quiz")

    # Dictionary of trivia questions
    questions = {
        "What is the hottest temperature ever recorded on Earth?": {
            "options": ["54°C", "56.7°C", "58°C", "60°C"],
            "answer": "56.7°C"
        },
        "Which city is known as the wettest place on Earth?": {
            "options": ["Mawsynram, India", "London, UK", "Seattle, USA", "Bogotá, Colombia"],
            "answer": "Mawsynram, India"
        },
        "What type of cloud is known for producing thunderstorms?": {
            "options": ["Cumulus", "Stratus", "Cirrus", "Cumulonimbus"],
            "answer": "Cumulonimbus"
        },
        "Is the atmospheric pressure inside a tropical storm higher or lower than normal?": {
            "options": ["Higher", "Lower"],
            "answer": "Lower"
        },
        "What does the Enhanced Fujita scale measure?": {
            "options": ["Hurricanes", "Snowfall", "Tornadoes", "Humidity"],
            "answer": "Tornadoes"
        },
        "Which is NOT a layer of the atmosphere?": {
            "options": ["Stratosphere", "Thermosphere", "Troposphere", "Lithosphere"],
            "answer": "Lithosphere"
        }
    }

    # Loop through the questions and display each one with radio button options
    for question, q_data in questions.items():
        st.markdown(f"**{question}**")
        options = q_data["options"]
        answer = q_data["answer"]
        user_answer = st.radio("Choose your answer:", options, key=question)

        # Check the user's answer and display feedback
        if user_answer:
            if user_answer == answer:
                st.success("Correct!")
            else:
                st.error(f"Incorrect! The correct answer is: {answer}")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
