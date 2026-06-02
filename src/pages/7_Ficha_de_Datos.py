import streamlit as st
from common.barra_lateral import renderizar_barra_lateral


st.set_page_config(page_title="Ficha de datos")

renderizar_barra_lateral()

st.title("Ficha de datos")

# Protección ante acceso directo
if "resultados_busqueda" not in st.session_state:

    st.error(
        "Debe realizar una búsqueda antes de acceder a esta página."
    )

    if st.button("Volver a búsqueda"):
        st.switch_page("pages/2_Busqueda.py")

    st.stop()

df_resultados = st.session_state["resultados_busqueda"]
st.success(
    f"Se recibieron {len(df_resultados)} registros desde la búsqueda."
)


