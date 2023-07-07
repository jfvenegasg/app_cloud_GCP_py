import os
import pandas as pd
from sqlalchemy import create_engine

# Primero, creas tu DataFrame
df = pd.DataFrame({
    'nombre': ['Juan', 'Ana', 'Carlos'],
    'edad': [25, 30, 35]
})

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'shiny-apps-385622-779b98ef3c14.json'
# Configuración de la conexión a la base de datos
username = 'shiny-apps-385622:us-central1:datos-bicicleta-austin'
password = '1234'
database = 'bicicletas-austin'
hostname = '34.72.43.11'  # Aquí puedes poner la dirección IP del servidor de Cloud SQL

# Crear la conexión
engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database}')

# Guardar el DataFrame en la base de datos
df.to_sql('bicicletas-austin', engine, if_exists='replace', index=False)
