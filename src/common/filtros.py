import streamlit as st
import pandas as pd

def renderizar_filtros_dwc(df):
    """Renderiza los selectores de filtrado en pantalla y calcula 
    la máscara combinada de Pandas según los criterios de Darwin Core.
    Retorna el DataFrame filtrado."""
    MAPEO_DWC = {
        "Nombre científico": "scientificName",
        "Observador": "recordedBy",
        "País": "country",
        "Provincia": "stateProvince",
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
    col_pais = MAPEO_DWC["País"]
    if col_pais in df.columns:
        opciones_pais = df[col_pais].dropna().unique().tolist()
        filtro_pais = col1.multiselect("País:", options=opciones_pais)
        if filtro_pais:
            mascara_combinada &= df[col_pais].isin(filtro_pais)

    col3, col4 = st.columns(2)

    # --- Filtro: Provincia ---
    col_prov = MAPEO_DWC["Provincia"]
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