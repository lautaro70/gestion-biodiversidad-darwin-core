# src/common/sidebar.py
import streamlit as st
from common.constants import PROCESSED_DATASETS

def renderizar_barra_lateral():
    """Ejercicio 1.B: Agrega un selector en el sidebar que permite elegir 
    el dataset y mantiene la selección persistente durante la sesión."""
    # .sidebar es el modificador de diseño de Streamlit para enviar componentes a la barra lateral.
    st.sidebar.title("Configuración del Sistema")
    
    datasets_disponibles = list(PROCESSED_DATASETS.keys())

    # st.session_state es la memoria global de Streamlit. La usamos para cumplir 
    # con el requisito del enunciado de que la selección persista entre páginas.
    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = datasets_disponibles[0]

    # Busco en qué posición (0, 1 o 2) está el dataset que el usuario había elegido antes.
    indice_actual = datasets_disponibles.index(st.session_state.dataset_actual)

    # Selector estructurado mediante st.selectbox
    seleccion = st.sidebar.selectbox(
        "Seleccione el dataset para trabajar:",
        options=datasets_disponibles,
        index=indice_actual
    )

    # Guardo la selección actual en la memoria global de la sesión
    st.session_state.dataset_actual = seleccion