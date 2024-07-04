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
    query2 = f"SELECT observation_time, temperature FROM student.\"Deens_weather\" WHERE city = '{city}' ORDER BY observation_time"
    df2 = pd.read_sql_query(query2, engine)
    return df2


###############################################################################################################################

# Streamlit application
def main():
    st.title("Weather Data App🌦️🌡️")
    st.logo("https://cdn.textstudio.com/output/sample/normal/2/5/4/6/weather-logo-600-16452.webp")
    
    engine = create_engine_connection()

    # Get data from Deens weather table
    data = fetch_data(engine)

    city = st.selectbox("Select City", ["New York", "London", "Tokyo", "Dubai", "Cape Town", "Paris", "Mexico city", "Shanghai", "Cairo", "Lagos", "São Paulo", "Mumbai", "Moscow", "Istanbul", "Seoul"])

    data2 = fetch_temperature_data(engine, city)

    # line chart
    if not data2.empty:
        fig = px.line(data2, x='observation_time', y=f'temperature', title=f'Temperature Trend in {city}')
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {city}.")

    st.markdown(""":blue[**Most recent weather data:**]""")
    st.dataframe(data)

    st.markdown(""":blue[**Scatter Graph 📊**]""")
    fig = px.scatter(data, x='temperature', y='humidity', color='city', hover_name='city')
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
