import streamlit as st
import pandas as pd
from common.barra_lateral import renderizar_barra_lateral
from core.carga_datasets import cargar_dataset_procesado

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Búsqueda")
st.title("Búsqueda de registros")

#Capturo el nombre del dataset activo desde nuestra variable segura
dataset_seleccionado = st.session_state["dataset_actual"] 

try:
    #Cargo el DataFrame completo usando Pandas
    df = cargar_dataset_procesado(dataset_seleccionado)
    
    #Extraigo las columnas usando df.columns para el selector
    columnas_disponibles = df.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles
    )
    #Campo de texto libre
    texto_busqueda = st.text_input(f"Ingrese el valor a buscar en '{columna_seleccionada}':")

    #Lógica de filtrado
    if texto_busqueda: 
        # Le agrego 'case=False' nativo de Pandas para que cumpla el requisito "case-insensitive".
        # Le agrego 'na=False' para que no tire error si la columna tiene celdas vacías.
        # astype(str) asegura que se pueda buscar texto incluso en columnas numéricas.
        mascara = df[columna_seleccionada].astype(str).str.contains(texto_busqueda, case=False, na=False)
        
        # Aplico la máscara al DataFrame original
        df_filtrado = df[mascara]
        
        # Muestro la cantidad de coincidencias usando .shape[0]
        st.info(f"Se encontraron {df_filtrado.shape[0]} registros coincidentes.")
        
        # Muestro el resultado como tabla interactiva
        st.dataframe(df_filtrado)
        
    else:
        st.caption("Escriba un término en el buscador para visualizar los resultados.")

except Exception as e:
    st.error(f"Error al cargar o procesar el dataset '{dataset_seleccionado}'. Detalle: {e}")