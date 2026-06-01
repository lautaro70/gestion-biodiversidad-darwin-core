import streamlit as st
from common.barra_lateral import renderizar_barra_lateral
from core.carga_datasets import cargar_dataset_procesado
from core.ejercicio4_insercion_registros import insertar_registro_desde_diccionario

st.set_page_config(page_title="Gestión de registros")
st.title("Gestión de registros")

renderizar_barra_lateral()

dataset_seleccionado = st.session_state["dataset_actual"]

try:
    datos = cargar_dataset_procesado(dataset_seleccionado)
    st.info(f" Dataset: **{dataset_seleccionado}** - {len(datos)} registros")

    # EJERCICIO 4.A - Formulario de inserción
    # ============================================
    st.header("Insertar nuevo registro")

    # Mostrar nombres de columnas según el dataset 
    with st.expander("Ver columnas"):
        st.write(list(datos.columns))

    if dataset_seleccionado == "XenoCanto":
        nombre_columna_latitud = "latitudeDecimal"
        nombre_columna_longitud = "longitudeDecimal"
        nombre_columna_pais = "country"
        pais_es_codigo = False
    else:
        nombre_columna_latitud = "decimalLatitude"
        nombre_columna_longitud = "decimalLongitude"
        nombre_columna_pais = "countryCode"
        pais_es_codigo = True

    # Formulario
    with st.form("formulario_insercion"):
        nombre_cientifico = st.text_input("Nombre científico")
        latitud = st.number_input("Latitud", value=0.0, step=0.0001, format="%.6f")
        longitud = st.number_input("Longitud", value=0.0, step=0.0001, format="%.6f")
        fecha_evento = st.date_input("Fecha del evento")
        
        if pais_es_codigo:
            pais = st.text_input("Código de país (ej: AR)")
        else:
            pais = st.text_input("País")
        
        boton_guardar = st.form_submit_button("Guardar registro")
        
        if boton_guardar:
            # Armar el diccionario con los datos del formulario
            nuevo_registro = {
                "scientificName": nombre_cientifico if nombre_cientifico else None,
                nombre_columna_latitud: latitud,
                nombre_columna_longitud: longitud,
                "eventDate": str(fecha_evento),
                nombre_columna_pais: pais.upper() if pais_es_codigo and pais else pais,
            }
            
            exito, mensaje = insertar_registro_desde_diccionario(dataset_seleccionado, nuevo_registro)
            
            if exito:
                st.success(f" {mensaje}")
            else:
                st.error(f"{mensaje}")

except Exception as error:
    st.error(f"Error al cargar el dataset '{dataset_seleccionado}': {error}")