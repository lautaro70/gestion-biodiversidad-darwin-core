import streamlit as st
from web.barra_lateral import renderizar_barra_lateral
import folium
from streamlit_folium import st_folium

from web.DataFrameCoordenadas6b import obtener_columnas_coordenadas,obtener_registros_validos_para_mapa,obtener_criterios_coloreo,crear_mapa_folium


st.set_page_config(page_title="Ficha de datos")

renderizar_barra_lateral()

st.title("Ficha de datos")

# Protección ante acceso directo
if "resultados_busqueda" not in st.session_state:

    st.error(
        "Debe realizar una búsqueda antes de acceder a esta página."
    )

    if st.button("Volver a búsqueda"):
        st.switch_page("pages/3_Búsqueda.py")

    st.stop()

df_resultados = st.session_state["resultados_busqueda"]
st.success(
    f"Se recibieron {len(df_resultados)} registros desde la búsqueda."
)

#------6b-----------

df_mapa, excluidos = (
    obtener_registros_validos_para_mapa(
        df_resultados
    )
)


st.info(
    f"Se excluyeron {excluidos} registros por coordenadas inválidas o nulas."
)

if df_mapa.empty:

    st.warning(
        "No existen registros con coordenadas válidas."
    )

    st.stop()

criterios = obtener_criterios_coloreo(
    df_mapa
)

criterio_color = st.selectbox(
    "Colorear puntos por:",
    criterios
)

mapa = crear_mapa_folium(
    df_mapa,
    criterio_color
)

st_folium(
    mapa,
    width=1000,
    height=600
)
