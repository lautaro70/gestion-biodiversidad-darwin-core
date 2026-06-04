import pandas as pd
import folium

from core.ejercicio3_validaciones import validar_par_coordenadas

def obtener_columnas_coordenadas(df):
    """
    Devuelve los nombres de las columnas de latitud y longitud
    según el dataset cargado.
    """

    col_latitud = None
    col_longitud = None

    if "decimalLatitude" in df.columns:
        col_latitud = "decimalLatitude"

    elif "latitudeDecimal" in df.columns:
        col_latitud = "latitudeDecimal"

    if "decimalLongitude" in df.columns:
        col_longitud = "decimalLongitude"

    elif "longitudeDecimal" in df.columns:
        col_longitud = "longitudeDecimal"

    return col_latitud, col_longitud

def obtener_registros_validos_para_mapa(df):
    """
    Devuelve:
    - DataFrame con coordenadas válidas
    - Cantidad de registros excluidos
    """

    registros_validos = []
    excluidos = 0

    col_latitud, col_longitud = obtener_columnas_coordenadas(df)

    for _, fila in df.iterrows():

        latitud = fila.get(col_latitud)
        longitud = fila.get(col_longitud)

        if pd.isna(latitud) or pd.isna(longitud):
            excluidos += 1
            continue

        es_valido, _ = validar_par_coordenadas(
            latitud,
            longitud
        )

        if es_valido:
            registros_validos.append(fila)

        else:
            excluidos += 1
    return pd.DataFrame(registros_validos), excluidos


def obtener_criterios_coloreo(df):

    criterios = []

    if "country" in df.columns:
        criterios.append("country")

    if "scientificName" in df.columns:
        criterios.append("scientificName")

    if "institutionCode" in df.columns:
        criterios.append("institutionCode")

    return criterios


def crear_mapa_folium(df, criterio_color):

    col_latitud, col_longitud = obtener_columnas_coordenadas(df)
    centro_latitud = (
        df[col_latitud]
        .astype(float)
        .mean()
    )

    centro_longitud = (
        df[col_longitud]
        .astype(float)
        .mean()
    )

    mapa = folium.Map(
        location=[centro_latitud, centro_longitud],
        zoom_start=4
    )

    colores = [
        "red",
        "blue",
        "green",
        "purple",
        "orange",
        "darkred",
        "cadetblue",
        "darkgreen"
    ]

    categorias = (
        df[criterio_color]
        .fillna("Sin dato")
        .unique()
    )

    mapeo_colores = {}

    for i, categoria in enumerate(categorias):

        mapeo_colores[categoria] = (
            colores[i % len(colores)]
        )

    for _, fila in df.iterrows():

        categoria = fila.get(
            criterio_color,
            "Sin dato"
        )
        popup = str(fila["occurrenceID"])

        folium.CircleMarker(

            location=[
                float(fila[col_latitud]),
                float(fila[col_longitud])
            ],

            radius=5,

            color=mapeo_colores[categoria],

            fill=True,

            fill_color=mapeo_colores[categoria],

            fill_opacity=0.8,

            popup=popup

        ).add_to(mapa)

    return mapa