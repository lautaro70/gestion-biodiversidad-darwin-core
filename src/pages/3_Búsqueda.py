import streamlit as st
from common.barra_lateral import renderizar_barra_lateral

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Búsqueda")
st.title("Búsqueda")