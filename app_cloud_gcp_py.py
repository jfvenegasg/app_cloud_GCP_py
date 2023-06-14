from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import streamlit_option_menu as menu
import os
from google.cloud import bigquery
from google.cloud import storage
import plotly.express as px

st.set_page_config(layout="wide")
#pip install protobuf==3.20.*


def fetch_data(query):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shiny-apps-385622-08e5b9820326.json'
    client = bigquery.Client()
    query_job = client.query(query)
    df = query_job.to_dataframe()
        
    return df

with st.sidebar:
    selected = menu.option_menu("App cloud gcp py", ["Inicio","Analisis datos Bigquery Austin Trips","Analisis datos Bigquery Austin Crime"], 
        icons=['house', 'person-rolodex','person-rolodex'], menu_icon="cast", default_index=0)
    selected

if selected == "Inicio":
    st.title("Esta es una app de demostración que utiliza los servicios GCP.")

if selected == "Analisis datos Bigquery Austin Trips":

    
    #c=st.empty()
        
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shiny-apps-385622-0553170e693d.json'

    #storage_client = storage.Client()
    #bucket = storage_client.bucket("imagenes_app_uss")
    #blob = bucket.blob("uss.png")
    #blob.download_to_filename("uss_GCS.png")
            
    #c.image("uss_GCS.png")

    #Esta funcion ejecuta una consulta al servicio Bigquery de google


        
    if st.button("Descarga"):
        query = """ SELECT * from `bigquery-public-data.austin_bikeshare.bikeshare_trips` LIMIT 100"""
        df=fetch_data(query)
        df.to_csv('trips_austin.csv', index=False)

        col1, col2 = st.columns(2)
        col1.text("Datos del sistema de bicicletas de la ciudad de Austin")
        col1.dataframe(df.head(10))

        grouped_data = df.groupby('subscriber_type')['duration_minutes'].sum().reset_index()
        fig = px.bar(grouped_data, x='subscriber_type', y='duration_minutes')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

    if st.button("Carga"):
        df = pd.read_csv('trips_austin.csv')
        col1, col2 = st.columns(2)
        col1.text("Datos del sistema de bicicletas de la ciudad de Austin")
        col1.dataframe(df.head(10))

        grouped_data = df.groupby('subscriber_type')['duration_minutes'].sum().reset_index()
        fig = px.bar(grouped_data, x='subscriber_type', y='duration_minutes')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)    

if selected == "Analisis datos Bigquery Austin Crime":

    if st.button("Descarga"):
        query = """ SELECT description,latitude,longitude,timestamp FROM `bigquery-public-data.austin_crime.crime` LIMIT 1000 """
        df=fetch_data(query)
        df.to_csv('crime_austin.csv', index=False)
        
        col1, col2 = st.columns(2)
        col1.text("Datos del crimen en la ciudad de Austin")
        col1.dataframe(df.head(10))

        conteo = df['description'].value_counts()
        df_conteo=pd.DataFrame({
            'crimen':conteo.index,
            'conteo':conteo.values})
        
        fig = px.bar(df_conteo, x='crimen', y='conteo')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

    if st.button("Carga"):
        df = pd.read_csv('crime_austin.csv')
        col1, col2 = st.columns(2)
        col1.text("Datos del crimen en la ciudad de Austin")
        col1.dataframe(df.head(10))

        conteo = df['description'].value_counts()
        df_conteo=pd.DataFrame({
            'crimen':conteo.index,
            'conteo':conteo.values})
        
        fig = px.bar(df_conteo, x='crimen', y='conteo')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)