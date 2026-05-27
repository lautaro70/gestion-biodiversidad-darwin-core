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
        
        # Muestro la cantidad de coincidencias usando .shape[0]
        st.info(f"Se encontraron {df_filtrado.shape[0]} registros coincidentes.")
        
        # Muestro el resultado como tabla interactiva
        st.dataframe(df_filtrado, use_container_width=True)    
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