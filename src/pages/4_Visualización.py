import streamlit as st
from web.barra_lateral import renderizar_barra_lateral
from web.ejercicio3visualizacion import obtener_datos_barras, obtener_datos_lineas,obtener_datos_taxonomia
import matplotlib.pyplot as plt
import pandas as pd
import os

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Visualización")
st.title("Visualización")

# ------ COMPROBACIÓN DE DATASET  ------
if "dataset_actual" in st.session_state and st.session_state["dataset_actual"] is not None:
    df = st.session_state["dataset_actual"]
    
    
    #----------------Punto 3a----------------
  
    st.markdown("---")
    st.header("Distribución Geográfica de Registros(3A)")
    
    # Por defecto ponemos 10 elementos 
    top_n = st.slider("Seleccioná cuántos elementos principales mostrar (Top N):", min_value=1, max_value=20, value=10)

    # Procesamos los datos 
    datos_grafico, columna_usada = obtener_datos_barras(df, top_n)

    # Validamos el resultado del filtro 
    if not datos_grafico.empty:
        # Creamos el gráfico con Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Dibujamos las barras pasando los nombres (index) y las cantidades (values)
        ax.bar(datos_grafico.index, datos_grafico.values, color='#2b5c8f', edgecolor='black')
        
        # Requisito del PDF: Agregar título, etiquetas de ejes y rotación
        tipo_grafico = "Países" if columna_usada == 'country' else "Provincias/Localidades"
        ax.set_title(f"Top {top_n} de Registros por {tipo_grafico}", fontsize=14, fontweight='bold')
        ax.set_xlabel(f"Ubicación ({columna_usada})", fontsize=12)
        ax.set_ylabel("Cantidad de Registros", fontsize=12)
        
        # Rotamos las etiquetas del eje X a 45 grados para que no se superpongan los nombres
        plt.xticks(rotation=45, ha='right')
        
        # Ajustamos los márgenes del lienzo
        plt.tight_layout()
        
        # Mostramos el gráfico final en la interfaz de Streamlit
        st.pyplot(fig)
    else:
        st.info("No se encontraron datos geográficos suficientes en este dataset para generar el gráfico.")


   
    # ------------------Punto 3b----------------------
   
    st.markdown("--------")
    st.header("Evolución temporal de registros por anio(3B)")

    min_anio_ds = None
    max_anio_ds = None
    
    for celda in df['eventDate']: # Buscamos el anio maximo y minimo para poder hacer bien el st.slider
        if not pd.isna(celda):
            try:
                anio_num = int(str(celda)[:4])

                if min_anio_ds is None or anio_num < min_anio_ds:
                    min_anio_ds = anio_num

                if max_anio_ds is None or anio_num > max_anio_ds:
                    max_anio_ds = anio_num
            except:
                continue # Si se rompe que siga con la siguiente fecha

    # Chequeamos que los anios tengan valor
    if min_anio_ds is not None and max_anio_ds is not None:
        if min_anio_ds == max_anio_ds:
            min_anio_ds -= 1

        # Armamos el slider 
        rango_anios = st.slider(
            "Seleccioná el rango de años a analizar:",
            min_value=min_anio_ds,
            max_value=max_anio_ds,
            value=(min_anio_ds, max_anio_ds)
        )

        anio_ini, anio_fin = rango_anios # Este seria el rango elegido por el usuario
        
        # Llamamos a la funcion
        datos_lineas, excluidos = obtener_datos_lineas(df, anio_ini, anio_fin)

        if not datos_lineas.empty:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            # Hacemos la linea con marcadores redondos
            ax2.plot(datos_lineas.index, datos_lineas.values, color='#e056fd', marker='o', linestyle='-', linewidth=2)
            # Titulos de los ejes 
            ax2.set_title(f"Cantidad de Avistamientos por Año ({anio_ini} - {anio_fin})", fontsize=14, fontweight='bold')
            ax2.set_xlabel("Año de la Observación", fontsize=12)
            ax2.set_ylabel("Cantidad de Registros", fontsize=12)

            # El eje x = integer (para que sean numeros)
            ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
            plt.tight_layout()
            st.pyplot(fig2)

            # Devoluciones 
            st.info(f"ℹ️ Se excluyeron {excluidos} registros por presentar fechas nulas o inválidas.")
        else:
            st.info("No hay registros en el rango de años seleccionado.")
    else:
        st.info("No se encontraron fechas válidas en la columna 'eventDate' para armar la línea de tiempo.")


    
    # ---------------punto 3c---------------------
    
    st.markdown("----------")
    st.header("Distribución por Nivel Taxonómico (3C)")

    # Hacemos un diccionario con las opciones de nivel taxonomico que puede elegir el usuario 
    opciones_taxo = {
        "Clase": "class",
        "Orden": "order",
        "Familia": "family"
    }

    # Aca es donde ponemos visualmente en streamlit las opciones que se pueden elegir
    seleccion_usuario = st.selectbox(
        "Seleccioná el nivel taxonómico para analizar la distribución:",
        options=list(opciones_taxo.keys())
    )

    columna_elegida = opciones_taxo[seleccion_usuario] # Agarramos el valor de la categoria elegida

    datos_taxo = obtener_datos_taxonomia(df, columna_elegida) # Llamada a la funcion

    # Comenzamos con el armado del grafico
    if not datos_taxo.empty:
        top_datos = datos_taxo.head(15) # Ponemos solo 15 elementos para que no quede gigante el grafico

        fig3, ax3 = plt.subplots(figsize=(10, 6)) # Creamos el grafico de barras

        # Dibujamos las barras y les damos color
        ax3.bar(top_datos.index, top_datos.values, color='#45aaf2', edgecolor='black')
        
        # Ponemos el titulo junto con sus etiquetas
        ax3.set_title(f"Top 15 - Distribución de Registros por {seleccion_usuario}", fontsize=14, fontweight='bold')
        ax3.set_xlabel(seleccion_usuario, fontsize=12)
        ax3.set_ylabel("Cantidad de Registros", fontsize=12)

        # Rotamos las etiquetas en 45 para que no se superpongan
        plt.xticks(rotation=45, ha='right')
            
        plt.tight_layout()

        # Mostramos en streamlit
        st.pyplot(fig3)

        # Aca avisamos que solo mostramos las primeras 15 
        if len(datos_taxo) > 15:
            st.info(f"ℹ️ Mostrando las 15 categorías más frecuentes de un total de {len(datos_taxo)} encontradas.")
    else:
         st.info(f"No se encontraron datos para el nivel taxonómico {seleccion_usuario}.")

# ----------Si no se selcciono ningun dataset------------------
else:
    st.warning("Por favor, seleccioná un dataset en la barra lateral para empezar a visualizar los gráficos.")