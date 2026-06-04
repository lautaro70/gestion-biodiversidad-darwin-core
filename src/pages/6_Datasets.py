import streamlit as st
import pandas as pd
from datetime import datetime

from common.constants import DATASETS
from web.barra_lateral import renderizar_barra_lateral
from web.carga_datasets import cargar_dataset_procesado


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


#EJERCICIO 5B

st.divider()

st.header("5.B - Información detallada de datasets")

dataset_seleccionado = st.selectbox(
    "Seleccione un dataset:",
    options=list(DATASETS.keys())
)

try:
    df = cargar_dataset_procesado(
        dataset_seleccionado
    )

except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.subheader("Columnas disponibles")

with st.expander("Ver columnas"):
    st.write(
        df.columns.tolist()
    )

st.subheader("Cantidad total de registros")

st.metric(
    "Registros",
    len(df)
)

st.subheader(
    "Porcentaje de valores nulos por columna"
)

porcentaje_nulos = (
    df.isnull()
      .mean()
      .mul(100)
      .round(2)
)

df_nulos = porcentaje_nulos.reset_index()

df_nulos.columns = [
    "Columna",
    "% Nulos"
]

st.dataframe(
    df_nulos,
    use_container_width=True
)