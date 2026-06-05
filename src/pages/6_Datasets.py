import streamlit as st
import pandas as pd
from datetime import datetime

from common.constants import DATASETS
from web.barra_lateral import renderizar_barra_lateral
from web.carga_datasets import cargar_dataset_procesado
from core.ejercicio3_validaciones import validar_par_coordenadas
from pathlib import Path


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

df_nulos = df_nulos.sort_values(
    by="% Nulos",
    ascending=False
)

st.dataframe(
    df_nulos,
    use_container_width=True
)



# EJERCICIO 5C

st.divider()

st.header("5.C - Comparación de datasets")

datos_comparacion = []

for nombre_dataset in DATASETS.keys():

    try:

        df = cargar_dataset_procesado(
            nombre_dataset
        )

        cantidad_registros = len(df)

        # ------------------------
        # Coordenadas válidas
        # ------------------------

        columnas_lat = [
            "decimalLatitude",
            "latitudeDecimal"
        ]

        columnas_lon = [
            "decimalLongitude",
            "longitudeDecimal"
        ]

        col_lat = next(
            (c for c in columnas_lat if c in df.columns),
            None
        )

        col_lon = next(
            (c for c in columnas_lon if c in df.columns),
            None
        )
        
        
        if (
            col_lat and col_lon
            and df[col_lat].notna().sum() > 0
            and df[col_lon].notna().sum() > 0
        ):

            coordenadas_validas = 0

            for _, fila in df.iterrows():

                latitud = fila[col_lat]
                longitud = fila[col_lon]

                if pd.isna(latitud) or pd.isna(longitud):
                    continue

                es_valido, _ = validar_par_coordenadas(
                    latitud,
                    longitud
                )

                if es_valido:
                    coordenadas_validas += 1

            porcentaje_coord = round(
                coordenadas_validas /
                cantidad_registros * 100,
                2
            )

        else:
            porcentaje_coord = "-"

        # ------------------------
        # Fechas válidas
        # ------------------------

        if (
            "eventDate" in df.columns
            and df["eventDate"].notna().sum() > 0
        ):

            fechas_validas = (
                pd.to_datetime(
                    df["eventDate"],
                    errors="coerce"
                )
                .notna()
                .sum()
            )

            porcentaje_fechas = round(
                fechas_validas /
                cantidad_registros * 100,
                2
            )

        else:
            porcentaje_fechas = "-"

        # ------------------------
        # Campos completos
        # ------------------------

        total_celdas = (
            df.shape[0] *
            df.shape[1]
        )

        celdas_completas = (
            df.notna()
            .sum()
            .sum()
        )

        porcentaje_completitud = round(
            celdas_completas /
            total_celdas * 100,
            2
        )


        datos_comparacion.append({

            "Dataset": nombre_dataset,

            "Registros": cantidad_registros,

            "% Coord. válidas": porcentaje_coord,

            "% Fechas válidas": porcentaje_fechas,

            "% Campos completos": porcentaje_completitud

        })

    except Exception:

        datos_comparacion.append({

            "Dataset": nombre_dataset,

            "Registros": "Error",

            "% Coord. válidas": "-",

            "% Fechas válidas": "-",

            "% Campos completos": "-"

        })

df_comparacion = pd.DataFrame(
    datos_comparacion
)

st.dataframe(
    df_comparacion,
    use_container_width=True
)


# EJERCICIO 5D

st.divider()

st.header("5.D - Documentación")

ruta_documentacion = (
    Path(__file__).resolve().parent.parent.parent
    / "documentation"
)

archivos_md = list(
    ruta_documentacion.glob("*.md")
)


if not archivos_md:

    st.info(
        "No se encontraron archivos Markdown en la carpeta documentation."
    )

else:

    nombres_archivos = [
        archivo.name
        for archivo in archivos_md
    ]

    archivo_seleccionado = st.selectbox(
        "Seleccione un documento:",
        nombres_archivos
    )

    ruta_archivo = (
        ruta_documentacion
        / archivo_seleccionado
    )

    try:

        with open(
            ruta_archivo,
            "r",
            encoding="utf-8"
        ) as archivo:

            contenido = archivo.read()

        st.markdown(contenido)

    except Exception as e:

        st.error(
            f"Error al leer el archivo: {e}"
        )