import streamlit as st
import pandas as pd
from common.barra_lateral import renderizar_barra_lateral
from core.carga_datasets import cargar_dataset_procesado
from common.filtros import renderizar_busqueda_libre, renderizar_filtros_dwc, renderizar_resultados_paginados

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Búsqueda")
st.title("Búsqueda de registros")

#Capturo el nombre del dataset activo desde nuestra variable segura
dataset_seleccionado = st.session_state["dataset_actual"] 

try:
    # Cargo el DataFrame completo una sola vez
    df = cargar_dataset_procesado(dataset_seleccionado)
    
    # EJERCICIO 2.A: Búsqueda Libre
    renderizar_busqueda_libre(df)

    # EJERCICIO 2.B: Filtros Combinados (DwC)
    st.divider()
    st.markdown("### Ejercicio 2.B: Filtros Combinados (Darwin Core)")
    
    #Llamo a la segunda función modular
    df_filtrado_combinado = renderizar_filtros_dwc(df)
    
    # Le pasamos "comb" como prefijo
    st.markdown("### Ejercicio 2.C: Resultados paginado")
    renderizar_resultados_paginados(df_filtrado_combinado, key_prefix="comb")

except Exception as e:
    st.error(f"Error al cargar o procesar el dataset '{dataset_seleccionado}'. Detalle: {e}")