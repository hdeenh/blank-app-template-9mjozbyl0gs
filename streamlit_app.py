import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

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
    query = "SELECT * FROM Deens_weather"
    df = pd.read_sql_query(query, engine)
    return df

# Streamlit application
def main():
    st.title("Weather Data Viewer")

    # Create SQLAlchemy engine
    engine = create_engine_connection()

    # Fetch data from PostgreSQL database
    data = fetch_data(engine)

    # Display data in Streamlit
    st.write("Weather Data from SQL Database:")
    st.dataframe(data)

    # Additional features
    st.write("Descriptive Statistics:")
    st.write(data.describe())

    st.write("Data Visualization:")
    st.bar_chart(data[['temperature', 'wind_speed', 'pressure', 'humidity']])