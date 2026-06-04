import streamlit as st
import pandas as pd
from datetime import datetime

from common.constants import DATASETS
from web.barra_lateral import renderizar_barra_lateral

#EJERCICIO 5A

st.set_page_config(page_title="Datasets")

renderizar_barra_lateral()

st.title("Exploración de datasets")

def obtener_info_datasets():
    
    datos = []

    for nombre, info in DATASETS.items():

        ruta = info["path"]

        tamanio_mb = ruta.stat().st_size / (1024 * 1024)

        fecha_modificacion = datetime.fromtimestamp(
            ruta.stat().st_mtime
        ).strftime("%d/%m/%Y %H:%M:%S")

        datos.append({
            "Dataset": nombre,
            "Archivo": ruta.name,
            "Tamaño (MB)": round(tamanio_mb, 2),
            "Última modificación": fecha_modificacion
        })

    return pd.DataFrame(datos)

st.header("5.A - Datasets disponibles")

df_datasets = obtener_info_datasets()

st.dataframe(
    df_datasets,
    use_container_width=True
)

