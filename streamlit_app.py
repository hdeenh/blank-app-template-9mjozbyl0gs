import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import psycopg2 as pg2
import plotly.express as px
import os
import requests

HOST = st.secrets['DB_HOST']
PORT = st.secrets['DB_PORT']
NAME = st.secrets['DB_NAME']
USER = st.secrets['DB_USER']
PASS = st.secrets['DB_PASS']


def create_engine_connection():
    engine_url = f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{NAME}'
    engine = create_engine(engine_url)
    return engine

def fetch_data(engine):
    query = "SELECT * FROM student.\"Deens_weather\" ORDER BY observation_time DESC, city ASC LIMIT 15;"
    df = pd.read_sql_query(query, engine)
    return df

def fetch_temperature_data(engine, city):
    query2 = f"SELECT observation_time, temperature, wind_speed, pressure, humidity FROM student.\"Deens_weather\" WHERE city = '{city}' ORDER BY observation_time"
    df2 = pd.read_sql_query(query2, engine)
    return df2


###############################################################################################################################

# Streamlit application
def main():
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo6lCF19a-hKONJB6oyYs6rKA63bKln9O7dg&s")
    #st.title("Weather Data App🌦️🌡️")
    st.logo("https://www.creativefabrica.com/wp-content/uploads/2021/03/31/weather-icon-illustration03-Graphics-10205167-1.jpg")

    engine = create_engine_connection()

    # Get data from Deens weather table
    data = fetch_data(engine)

    city = st.selectbox("Select City", ["New York", "London", "Tokyo", "Dubai", "Cape Town", "Paris", "Mexico city", "Shanghai", "Cairo", "Lagos", "São Paulo", "Mumbai", "Moscow", "Istanbul", "Seoul"])
    params = st.selectbox("Select weather parameter", ["temperature", "wind_speed", "humidity", "pressure"])
    data2 = fetch_temperature_data(engine, city)

    # line chart
    if not data2.empty:
        fig = px.line(data2, x='observation_time', y=f'{params}', title=f'Temperature Trend in {city}')
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {city}.")

    st.markdown(""":blue[**Most recent weather data:**]""")
    st.dataframe(data)

    st.markdown(""":blue[**Scatter Graph 📊**]""")
    fig = px.scatter(data, x='temperature', y='humidity', color='city', hover_name='city')
    st.plotly_chart(fig)

    st.markdown("### Weather Trivia Quiz")

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
        },
        "Is the atmospheric pressure inside a tropical storm higher or lower than normal?": {
            "options": ["Higher", "Lower"],
            "answer": "Cumulonimbus"
        }}

    for question, q_data in questions.items():
        st.markdown(f"**{question}**")
        options = q_data["options"]
        answer = q_data["answer"]
        user_answer = st.radio("Choose your answer:", options, key=question)

        if user_answer:
            if user_answer == answer:
                st.success("Correct!")
            else:
                st.error(f"Incorrect! The correct answer is: {answer}")


if __name__ == "__main__":
    main()
