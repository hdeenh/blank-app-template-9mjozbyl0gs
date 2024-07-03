import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import psycopg2 as pg2
import plotly.express as px

# Set the theme
st.set_page_config(page_title="My Streamlit App", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")

# Change theme to dark
st.markdown(
    """
    <style>
    body {
        background-color: #429bf5;
        color: #a3ff96;
    }
    </style>
    """,
    unsafe_allow_html=True)

# Database connection configuration
DB_HOST = 'data-sandbox.c1tykfvfhpit.eu-west-2.rds.amazonaws.com'
DB_PORT = '5432'
DB_NAME = 'pagila'
DB_USER = 'de10_dehu'
DB_PASS = '5MSsaxSe'

# Function to create a SQLAlchemy engine
def create_engine_connection():
    engine_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(engine_url)
    return engine

# Function to fetch data from the PostgreSQL database
def fetch_data(engine):
    query = "SELECT * FROM student.\"Deens_weather\" ORDER BY observation_time DESC LIMIT 15;"
    df = pd.read_sql_query(query, engine)
    return df

def fetch_temperature_data(engine, city):
    query2 = f"SELECT observation_time, temperature FROM student.\"Deens_weather\" WHERE city = '{city}' ORDER BY observation_time"
    df2 = pd.read_sql_query(query2, engine)
    return df2

# Streamlit application
def main():
    st.title("Weather Data App🌦️🌡️")
    st.logo("https://cdn.jim-nielsen.com/ios/512/weather-2021-12-07.png?rf=1024")
    # Create SQLAlchemy engine
    engine = create_engine_connection()

    # Fetch data from PostgreSQL database
    data = fetch_data(engine)

    # Display data in Streamlit
    st.markdown(""":blue[**Most recent weather data:**]""")
    st.dataframe(data)

    st.markdown(""":blue[**Scatter Graph 📊**]""")
    fig = px.scatter(data, x='temperature', y='humidity', color='city', hover_name='city')
    st.plotly_chart(fig)

    # User input for city selection
    city = st.selectbox("Select City", ["New York", "London", "Tokyo", "Dubai", "Cape Town", "Paris", "Mexico city", "Shanghai", "Cairo", "Lagos", "São Paulo", "Mumbai", "Moscow", "Istanbul", "Seoul"])

    # Fetch temperature data based on selected city
    data2 = fetch_temperature_data(engine, city)

    # Display interactive line chart using Plotly Express
    if not data2.empty:
        fig = px.line(data2, x='observation_time', y='temperature', title=f'Temperature Trend in {city}')
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {city}.")

if __name__ == "__main__":
    main()
