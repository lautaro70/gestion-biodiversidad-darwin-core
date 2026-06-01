# src/common/sidebar.py
import streamlit as st
from common.constants import PROCESSED_DATASETS
import pandas as pd
from core.carga_datasets import cargar_dataset_procesado

def renderizar_barra_lateral():
    """Dibuja el selector y las métricas en tiempo real.
    Resuelve el lag en la misma página mediante el patrón de restauración de keys."""
    # .sidebar es el modificador de diseño de Streamlit para enviar componentes a la barra lateral.
    st.sidebar.title("Configuración del Sistema")
    
    datasets_disponibles = list(PROCESSED_DATASETS.keys())

    # st.session_state es la memoria global de Streamlit. La usamos para cumplir 
    # con el requisito del enunciado de que la selección persista entre páginas.
    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = datasets_disponibles[0]
        # Usamos pd.Timestamp.now() alineado al manejo de fechas de la Clase 11
        st.session_state["fecha_seleccion"] = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")

    # Busco en qué posición (0, 1 o 2) está el dataset que el usuario había elegido antes.
    indice_actual = datasets_disponibles.index(st.session_state.dataset_actual)

    # Selector estructurado mediante st.selectbox
    seleccion = st.sidebar.selectbox(
        "Seleccione el dataset para trabajar:",
        options=datasets_disponibles,
        index=indice_actual
    )

    hueco_nombre = st.sidebar.empty()
    hueco_cantidad = st.sidebar.empty()
    hueco_fecha = st.sidebar.empty()

    #Control del cambio: Si el usuario elige otro, se actualiza la fecha con pandas
    if seleccion != st.session_state["dataset_actual"]:
        st.session_state["dataset_actual"] = seleccion
        st.session_state["fecha_seleccion"] = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            df_temporal = cargar_dataset_procesado(seleccion)
            cant_registros = df_temporal.shape[0]
        except Exception:
            cant_registros = "Error al contabilizar."
            
        #Relleno los huecos con la data nueva ANTES de reiniciar
        hueco_nombre.write(f"**Nombre:** {seleccion}")
        hueco_cantidad.write(f"**Cantidad de registros:** {cant_registros}")
        hueco_fecha.write(f"**Fecha/Hora de selección:** {st.session_state['fecha_seleccion']}")
        #Esto hace que el "indice_actual" se recalcule en el acto y las métricas no tengan lag.
        st.rerun()

    try:
        df_activo = cargar_dataset_procesado(st.session_state["dataset_actual"])
        # .shape[0] nos devuelve la cantidad de filas (registros) del DataFrame
        cantidad_registros = df_activo.shape[0]
    except Exception as e:
        cantidad_registros = "Error al contabilizar."

    hueco_nombre.write(f"**Nombre:** {st.session_state['dataset_actual']}")
    hueco_cantidad.write(f"**Cantidad de registros:** {cantidad_registros}")
    hueco_fecha.write(f"**Fecha/Hora de selección:** {st.session_state['fecha_seleccion']}")  