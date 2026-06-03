import streamlit as st
from web.barra_lateral import renderizar_barra_lateral
from web.carga_datasets import cargar_dataset_procesado
from core.ejercicio4_insercion_registros import insertar_registro_desde_diccionario
from core.ejercicio5_actualizacion_registros import buscar_registros

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

    # EJERCICIO 4.B - Búsqueda por identificador
    # ============================================
    
    st.header("Buscar registro para editar")
    
    # Seleccionar ID según el dataset
    if dataset_seleccionado == "IADIZA":
        columna_id = "occurrenceID"
        ejemplo_id = "IADIZA:COI:006861"
    elif dataset_seleccionado == "Inaturalist":
        columna_id = "id"
        ejemplo_id = "17063"
    else:  # XenoCanto
        columna_id = "id"
        ejemplo_id = "999540@XC"
    
    st.caption(f"Búsqueda en la columna **{columna_id}** (ejemplo: `{ejemplo_id}`)")
    
    id_buscar = st.text_input(f"Ingresá el {columna_id} del registro que querés editar:")
    
    if st.button("Buscar registro", key="boton_buscar"):
        if id_buscar:
            # Buscar el registro usando la función de la Parte 1
            filtros = {columna_id: id_buscar}
            resultados = buscar_registros(dataset_seleccionado, filtros)
            
            if resultados and len(resultados) > 0:
                st.success(f"Registro encontrado")
                # Guardamos el registro encontrado en session_state
                st.session_state["registro_a_editar"] = resultados[0]
                
                with st.expander("Ver registro completo"):
                    st.json(resultados[0])
            else:
                st.error(f"No se encontró ningún registro con {columna_id} = '{id_buscar}'")
                if "registro_a_editar" in st.session_state:
                    del st.session_state["registro_a_editar"]
        else:
            st.warning("Por favor, ingresá un ID")

except Exception as error:
    st.error(f"Error al cargar el dataset '{dataset_seleccionado}': {error}")