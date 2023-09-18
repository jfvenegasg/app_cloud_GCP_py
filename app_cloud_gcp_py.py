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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'apps-392022-8c353b675061.json'
    client = bigquery.Client()
    query_job = client.query(query)
    df = query_job.to_dataframe()
        
    return df

with st.sidebar:
    selected = menu.option_menu("App cloud gcp py", ["Inicio","Analisis datos Austin Trips","Analisis datos Austin Crime","Analisis datos Austin Waste","Analisis datos Austin Incident 2016"], 
        icons=['house', 'person-rolodex','person-rolodex','person-rolodex','person-rolodex'], menu_icon="cast", default_index=0)
    selected

if selected == "Inicio":
    st.title("Esta es una app de demostración que utiliza los servicios GCP.")

if selected == "Analisis datos Austin Trips":

    
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

        grouped_data = df.groupby('trip_id')['duration_minutes'].sum().reset_index()
        grouped_data = grouped_data.sort_values(by='duration_minutes', ascending=False)
        fig = px.bar(grouped_data, x='trip_id', y='duration_minutes')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

        
    if st.button("Carga"):
        df = pd.read_csv('trips_austin.csv')
        col1, col2 = st.columns(2)
        col1.text("Datos del sistema de bicicletas de la ciudad de Austin")
        col1.dataframe(df.head(10))

        grouped_data = df.groupby('trip_id')['duration_minutes'].sum().reset_index()
        grouped_data = grouped_data.sort_values(by='duration_minutes', ascending=False)
        fig = px.bar(grouped_data, x='trip_id', y='duration_minutes')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)    

        with st.container():
        #porcentajes = df['duration_minutes']/df['duration_minutes'].sum()*100
        #df['percentage'] = porcentajes
        #datos_porcentaje=df
        #grouped_data = grouped_data.sort_values(by='duration_minutes', ascending=False)
            porcentajes = grouped_data['duration_minutes']/grouped_data['duration_minutes'].sum()*100
            grouped_data['percentage'] = porcentajes
            fig_pie = px.pie(grouped_data, names='trip_id', values='percentage', title='Gráfico de Torta')
            st.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
            st.plotly_chart(fig_pie)

if selected == "Analisis datos Austin Crime":

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

if selected == "Analisis datos Austin Waste":

    if st.button("Descarga"):
        query = """ SELECT load_id,load_type,load_weight FROM `bigquery-public-data.austin_waste.waste_and_diversion` """
        df=fetch_data(query)
        df.to_csv('waste_austin.csv', index=False)
        
        col1, col2 = st.columns(2)
        col1.text("Datos Waste en la ciudad de Austin")
        col1.dataframe(df.head(10))

        grouped_data = df.groupby('load_type')['load_id'].sum().reset_index()
        grouped_data = grouped_data.sort_values(by='load_id', ascending=False)
        
        
        fig = px.bar(grouped_data, x='load_type', y='load_id')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

    if st.button("Carga"):
        df = pd.read_csv('waste_austin.csv')
        col1, col2 = st.columns(2)
        col1.text("Datos Waste en la ciudad de Austin")
        col1.dataframe(df.head(10))

        grouped_data = df.groupby('load_type')['load_id'].sum().reset_index()
        grouped_data = grouped_data.sort_values(by='load_id', ascending=False)

        fig = px.bar(grouped_data, x='load_type', y='load_id')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

if selected == "Analisis datos Austin Incident 2016":

    if st.button("Descarga"):
        query = """SELECT descript,date,time,address FROM `bigquery-public-data.austin_incidents.incidents_2016`"""
        df=fetch_data(query)
        df.to_csv('incident_2016_austin.csv', index=False)
        
        col1, col2 = st.columns(2)
        col1.text("Datos Incidentes 2016 en la ciudad de Austin")
        col1.dataframe(df.head(10))

        conteo = df['descript'].value_counts()
        df_conteo=pd.DataFrame({
            'descript':conteo.index,
            'total':conteo.values})        
        
        fig = px.bar(df_conteo, x='descript', y='total')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)

    if st.button("Carga"):
        df = pd.read_csv('incident_2016_austin.csv')
        col1, col2 = st.columns(2)
        col1.text("Datos Incidentes 2016 en la ciudad de Austin")
        col1.dataframe(df.head(10))

        conteo = df['descript'].value_counts()
        df_conteo=pd.DataFrame({
            'descript':conteo.index,
            'total':conteo.values}) 

        fig = px.bar(df_conteo, x='descript', y='total')
        col2.text("Grafico de la duracion de minutos de los viajes del sistema de bicicleta")
        col2.plotly_chart(fig)