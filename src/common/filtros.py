import streamlit as st
import pandas as pd

def renderizar_busqueda_libre(df):
    """Ejercicio 2.A: Renderiza el buscador de texto libre por columna.
    Muestra la cantidad de coincidencias y la tabla interactiva resultante."""
    
    # Extraigo las columnas usando df.columns para el selector
    columnas_disponibles = df.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles)
    
    # Campo de texto libre
    texto_busqueda = st.text_input(f"Ingrese el valor a buscar en '{columna_seleccionada}':")

    # Lógica de filtrado
    if texto_busqueda: 
        # Le agrego 'case=False' nativo de Pandas para que cumpla el requisito "case-insensitive".
        # Le agrego 'na=False' para que no tire error si la columna tiene celdas vacías.
        # astype(str) asegura que se pueda buscar texto incluso en columnas numéricas.
        mascara = df[columna_seleccionada].astype(str).str.contains(texto_busqueda, case=False, na=False)
        
        # Aplico la máscara al DataFrame original
        df_filtrado = df[mascara]
        
        #LA FUNCIÓN DEL 2.C
        # Le paso "libre" como prefijo para que las variables internas no choquen
        st.markdown("#### Resultados (Vista Paginada)")
        renderizar_resultados_paginados(df_filtrado, key_prefix="libre")    
    else:
        st.caption("Escriba un término en el buscador para visualizar los resultados.")

def renderizar_filtros_dwc(df):
    """Ejercicio 2)b): Renderiza los selectores de filtrado en pantalla y calcula 
    la máscara combinada de Pandas según los criterios de Darwin Core.
    Retorna el DataFrame filtrado."""
    MAPEO_DWC = {
        "Nombre científico": "scientificName",
        "Observador": "recordedBy",
        "Fecha": "eventDate"}

    #Máscara base
    mascara_combinada = pd.Series(True, index=df.index)
    col1, col2 = st.columns(2)

    # --- Filtro: Nombre Científico ---
    col_nc = MAPEO_DWC["Nombre científico"]
    if col_nc in df.columns:
        opciones_nc = df[col_nc].dropna().unique().tolist()
        filtro_nc = col1.multiselect("Nombre científico:", options=opciones_nc)
        if filtro_nc:
            mascara_combinada &= df[col_nc].isin(filtro_nc)

    # --- Filtro: País ---
    # Buscamos si existe "country" o si existe "countryCode"
    col_pais = None
    if "country" in df.columns:
        col_pais = "country"
    elif "countryCode" in df.columns:
        col_pais = "countryCode"

    if col_pais in df.columns:
        opciones_pais = df[col_pais].dropna().unique().tolist()
        filtro_pais = col1.multiselect("País:", options=opciones_pais)
        if filtro_pais:
            mascara_combinada &= df[col_pais].isin(filtro_pais)

    col3, col4 = st.columns(2)

    # --- Filtro: Provincia ---
    # Buscamos si existe "stateProvince" o si usamos "locality" como plan B
    col_prov = None
    if "stateProvince" in df.columns:
        col_prov = "stateProvince"
    elif "locality" in df.columns:
        col_prov = "locality"

    if col_prov in df.columns:
        opciones_prov = df[col_prov].dropna().unique().tolist()
        filtro_prov = col3.multiselect("Provincia:", options=opciones_prov)
        if filtro_prov:
            mascara_combinada &= df[col_prov].isin(filtro_prov)

    # --- Filtro: Observador ---
    col_obs = MAPEO_DWC["Observador"]
    if col_obs in df.columns:
        filtro_obs = col4.text_input("Observador (Texto libre):")
        if filtro_obs:
            mascara_combinada &= df[col_obs].astype(str).str.contains(filtro_obs, case=False, na=False)

    # --- Filtro: Rango de Fechas ---
    col_fecha = MAPEO_DWC["Fecha"]
    fechas_validas = False

    if col_fecha in df.columns:
        #errors para que no se frene si encuentra un dato vacío o cualquier error convirtiendolo a nulo
        df['fecha_dt'] = pd.to_datetime(df[col_fecha], errors='coerce')
        if not df['fecha_dt'].isna().all():
            fechas_validas = True
            min_fecha = df['fecha_dt'].min().date()
            max_fecha = df['fecha_dt'].max().date()

    if fechas_validas:
        filtro_fecha = st.date_input(
            "Rango de fechas de observación:",
            value=(min_fecha, max_fecha),
            min_value=min_fecha,
            max_value=max_fecha
        )
        if isinstance(filtro_fecha, tuple) and len(filtro_fecha) == 2:
            fecha_inicio, fecha_fin = filtro_fecha
            mascara_fechas = (df['fecha_dt'].dt.date >= fecha_inicio) & (df['fecha_dt'].dt.date <= fecha_fin)
            mascara_combinada &= mascara_fechas
    else:
        st.date_input("Rango de fechas de observación:", disabled=True, help="No hay datos de fecha disponibles en este dataset.")

    # Retornamos el DataFrame ya recortado con las condiciones activas
    return df[mascara_combinada]

def boton_exportar(df_exportar, key_prefix):
    """Ejercicio 2.D: Genera el archivo CSV en memoria y dibuja el botón de descarga."""
    
    #Recupero el nombre del dataset desde la memoria global
    dataset_actual = st.session_state.get("dataset_actual", "Dataset")
    
    #Genero la fecha y hora actual para el nombre del archivo
    fecha_descarga = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"{dataset_actual}_{fecha_descarga}.csv"

    #Convierto el DataFrame a CSV (en bytes para Streamlit)
    csv_data = df_exportar.to_csv(index=False).encode('utf-8')

    #Dibujo el botón
    st.download_button(
        label= "Exportar resultados (CSV)",
        data=csv_data,
        file_name=nombre_archivo,
        mime='text/csv',
        key=f"exportar_{key_prefix}" 
    )

def renderizar_resultados_paginados(df_filtrado, key_prefix):
    """Ejercicio 2.C: Renderiza una tabla interactiva con paginación, 
    columnas relevantes y vista de detalle."""
    
    if df_filtrado.empty:
        st.warning("No se encontraron registros que coincidan con la búsqueda.")
        return
    
    #Uso columnas para alinear el mensaje de éxito y el botón de descarga
    col_info, col_descarga = st.columns([2, 1])
    
    with col_info:
        st.success(f"Se encontraron {df_filtrado.shape[0]} registros.")
        
    with col_descarga:
        #LLamo funcion del 2)D)
        boton_exportar(df_filtrado, key_prefix)

    #Ejercicio 2)c)
    #Selección de columnas relevantes
    columnas_preferidas = [
        "occurrenceID", "scientificName", "eventDate", "recordedBy",
        "country", "countryCode", "stateProvince", "locality"
    ]
    #Intersecto para evitar errores si alguna columna no existe en este dataset
    cols_a_mostrar = [col for col in columnas_preferidas if col in df_filtrado.columns]

    st.markdown("#### Resultados (Vista Paginada)")
    
    #Lógica de Paginación Matemática
    tamano_pagina = 15
    total_registros = len(df_filtrado)
    total_paginas = (total_registros // tamano_pagina) + (1 if total_registros % tamano_pagina > 0 else 0)

    #Creo columnas para que el selector de página no ocupe toda la pantalla
    col_pag1, col_pag2 = st.columns([1, 3])
    with col_pag1:
        # Usamos key_prefix para que Streamlit no produzca error si usamos la función dos veces en la página
        pagina_actual = st.number_input(
            "Página:", 
            min_value=1, 
            max_value=total_paginas, 
            step=1, 
            key=f"pag_{key_prefix}"
        )

    inicio = (pagina_actual - 1) * tamano_pagina
    fin = inicio + tamano_pagina

    #Recorto el DataFrame: solo las columnas relevantes y solo las 15 filas de esta página
    df_pagina = df_filtrado[cols_a_mostrar].iloc[inicio:fin]

    #Tabla interactiva para el ordenamiento
    st.dataframe(df_pagina)

    #Acceso al detalle completo de un registro
    st.markdown("#### Ver Detalle Completo")
    if "occurrenceID" in df_pagina.columns:
        # Usamos los IDs que se están mostrando en esta página específica
        opciones_ids = ["Seleccione un registro..."] + df_pagina["occurrenceID"].tolist()
        id_seleccionado = st.selectbox(
            "Seleccione el ID de la observación para desplegar todos sus atributos:", 
            options=opciones_ids,
            key=f"detalle_{key_prefix}"
        )
        
        if id_seleccionado != "Seleccione un registro...":
            #Busco la fila exacta en el DataFrame filtrado original (para tener todas las columnas)
            detalle_registro = df_filtrado[df_filtrado["occurrenceID"] == id_seleccionado].iloc[0]
            #st.json dibuja los datos como un diccionario muy prolijo y fácil de leer
            st.json(detalle_registro.dropna().to_dict())
    else:
        st.info("El dataset no posee la columna 'occurrenceID' para identificar el detalle.")