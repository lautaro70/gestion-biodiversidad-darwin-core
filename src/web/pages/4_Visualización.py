import streamlit as st
from web.barra_lateral import renderizar_barra_lateral
from web.ejercicio3visualizacion import obtener_datos_barras, obtener_datos_lineas, obtener_datos_taxonomia
import matplotlib.pyplot as plt
from core.ejercicio2_lectura_dataset import porcentaje_nulos
import pandas as pd
import os
from web.carga_datasets import cargar_dataset_procesado

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Visualización")
st.title("Visualización")

df = None

if "dataset_actual" in st.session_state and st.session_state["dataset_actual"] is not None:
    nombre_dataset = st.session_state["dataset_actual"]
    
    try:
        # Usamos la función  para cargar la tabla real de Pandas de los dataset
        df = cargar_dataset_procesado(nombre_dataset)
    except Exception as e:
        st.error(f"Error al procesar el dataset con la función del grupo: {e}")

# ------ si se carga el dataframe elegido entonces procede a mostrar los datos ------
if df is not None:
    # ---------------- Punto 3a ----------------
    st.markdown("---")
    st.header("Distribución Geográfica de Registros(3A)")
    
    # Por defecto ponemos 10 elementos 
    top_n = st.slider("Seleccioná cuántos elementos principales mostrar (Top N):", min_value=1, max_value=20, value=10)

    # Procesamos los datos 
    datos_grafico, columna_usada = obtener_datos_barras(df, top_n)

    # Validamos el resultado del filtro 
    if not datos_grafico.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(datos_grafico.index, datos_grafico.values, color='#2b5c8f', edgecolor='black')
        
        tipo_grafico = "Países" if columna_usada == 'country' else "Provincias/Localidades"
        ax.set_title(f"Top {top_n} de Registros por {tipo_grafico}", fontsize=14, fontweight='bold')
        ax.set_xlabel(f"Ubicación ({columna_usada})", fontsize=12)
        ax.set_ylabel("Cantidad de Registros", fontsize=12)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No se encontraron datos geográficos suficientes en este dataset para generar el gráfico.")

    # ------------------ Punto 3b ----------------------
    
    st.markdown("--------")
    st.header("Evolución temporal de registros por anio(3B)")

   
# Definimos un rango de años largo y seguro para el selector
    min_anio_ds = 1900
    max_anio_ds = 2026
# Armamos el slider
    rango_anios = st.slider(
        "Seleccioná el rango de años a analizar:",
        min_value=min_anio_ds,
        max_value=max_anio_ds,
        value=(1970, 2026)
    )

    anio_ini, anio_fin = rango_anios# Este seria el rango elegido por el usuario
    
    # LLAMADA DIRECTA CON EL DF ORIGINAL
    datos_lineas, excluidos = obtener_datos_lineas(df, anio_ini, anio_fin)# Llamamos a la funcion

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
        st.info(f"ℹ️ Se procesaron correctamente los registros del rango seleccionado.")
    else:
        st.info("No hay registros con fechas válidas en el rango de años seleccionado. Probá moviendo el slider a otros años.")


    # --------------- punto 3c ---------------------
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
# Agarramos el valor de la categoria elegida
    columna_elegida = opciones_taxo[seleccion_usuario]

    if columna_elegida in df.columns: #Agrego esto porque en el caso de xenocanto no tiene clases, entonces para que no explote lo encerramos en el if
        datos_taxo = obtener_datos_taxonomia(df, columna_elegida)# Llamada a la funcion

# Comenzamos con el armado del grafico
        if not datos_taxo.empty:
            top_datos = datos_taxo.head(15)# Ponemos solo 15 elementos para que no quede gigante el grafico
            fig3, ax3 = plt.subplots(figsize=(10, 6))# Creamos el grafico de barras
            # Dibujamos las barras y les damos color
            ax3.bar(top_datos.index, top_datos.values, color='#45aaf2', edgecolor='black')
            # Ponemos el titulo junto con sus etiquetas
            ax3.set_title(f"Top 15 - Distribución de Registros por {seleccion_usuario}", fontsize=14, fontweight='bold')
            ax3.set_xlabel(seleccion_usuario, fontsize=12)
            ax3.set_ylabel("Cantidad de Registros", fontsize=12)
            plt.xticks(rotation=45, ha='right')# Rotamos las etiquetas en 45 para que no se superpongan
            plt.tight_layout()# Mostramos en streamlit
            st.pyplot(fig3)

            if len(datos_taxo) > 15:# Aca avisamos que solo mostramos las primeras 15
                 st.info(f"ℹ️ Mostrando las 15 categorías más frecuentes de un total de {len(datos_taxo)} encontradas.")
        else:
             st.info(f"No se encontraron datos para el nivel taxonómico {seleccion_usuario}.")
    else:
        # Si el dataset no tiene la columna (como le pasa a XenoCanto con 'class'), mostramos este cartel
        st.warning(f"⚠️ El dataset seleccionado no cuenta con la información de la columna '{columna_elegida}' para el nivel '{seleccion_usuario}'.")

#-----------------Punto 3d-------------------

    st.markdown("--------")
    st.header("Nivel de completitud por columna (3D)")

    # Llamamos a la función del 2f pasándole el nombre del dataset seleccionado
    diccionario_nulos = porcentaje_nulos(nombre_dataset)

    # Verificamos que la función haya devuelto un diccionario válido y no un error
    if isinstance(diccionario_nulos, dict) and diccionario_nulos:

        diccionario_completitud = {
            columna: 100 - porcentaje_nulo # Hacemos esto porque la funcion calculaba el porcentaje de nulos
            for columna, porcentaje_nulo in diccionario_nulos.items() #Y nosotros queremos los no nulos
        }

        # Ordenamos las columnas de mayor a menor completitud
        datos_ordenados = sorted(diccionario_completitud.items(), key=lambda x: x[1], reverse=False)

        # --- amontonamiento
        # Como hay más de 200 columnas, si graficamos todas se superpone todo el texto.
        # Filtramos para quedarnos solo con las columnas que SÍ tienen datos (completitud > 0)
        datos_con_datos = [elemento for elemento in datos_ordenados if elemento[1] > 0]
        
        # Si aun así son demasiadas, nos quedamos con las 30 más representativas para que sea legible
        if len(datos_con_datos) > 30:
            datos_grafico = datos_con_datos[-30:] # Agarramos las 30 con mayor completitud
            subtitulo_grafico = "(Top 30 columnas más completas)"
        else:
            datos_grafico = datos_con_datos
            subtitulo_grafico = "(Columnas con datos presentes)"

        # Separamos los nombres de las columnas por un lado y los porcentajes por el otro
        columnas_finales = [elemento[0] for elemento in datos_grafico]
        porcentajes_finales = [elemento[1] for elemento in datos_grafico]

        # Calculamos una altura dinámica proporcional a la cantidad de barras a mostrar
        altura_figura = max(6, len(columnas_finales) * 0.4)

        # Creamos la figura de Matplotlib dándole un tamaño vertical generoso
        fig3, ax3 = plt.subplots(figsize=(10, altura_figura))
        
        # Dibujamos barras horizontales con barh() agregandole color celeste/azul
        barras = ax3.barh(columnas_finales, porcentajes_finales, color='#00a8ff', edgecolor='black')

        # Ponemos los títulos del gráfico y de los ejes
        ax3.set_title(f"Porcentaje de Completitud por Columna\n{subtitulo_grafico}", fontsize=14, fontweight='bold')
        ax3.set_xlabel("Porcentaje de Datos Presentes (%)", fontsize=12)
        ax3.set_ylabel("Columnas del Dataset", fontsize=12)

        # Modificamos el tamaño de la letra de las columnas para que no se choque
        ax3.tick_params(axis='y', labelsize=10)

        # Forzamos el límite del eje X para que vaya siempre de 0 a 100%
        ax3.set_xlim(0, 115) # Le damos hasta 115 para que el texto del % no quede cortado a la derecha

        # Le agregamos una cuadrícula de fondo  solo en el eje X para facilitar la lectura
        ax3.grid(axis='x', linestyle='--', alpha=0.7)

        # Agregamos el texto con el porcentaje exacto al final de cada barra 
        for barra in barras:
            ancho_barra = barra.get_width()
            ax3.text(
                ancho_barra + 1, # Posición un poquito a la derecha del final de la barra
                barra.get_y() + barra.get_height()/2, # Centrado verticalmente en la barra
                f'{ancho_barra:.1f}%', # Texto con un decimal
                va='center', 
                ha='left', 
                fontsize=9, 
                fontweight='bold'
            )

        plt.tight_layout()
        st.pyplot(fig3) # Mostramos el gráfico en la web de Streamlit
        
        st.info("ℹ️ El gráfico muestra las columnas que contienen datos válidos, ordenadas por su nivel de llenado.")

        
    else:
        st.error(f"No se pudieron calcular los nulos: {diccionario_nulos}")


#-------------Ejercicio 3E------------------------------

    st.markdown("--------")
    st.header("Tabla Comparativa de los Datasets (3E)")

    lista_datasets = ["IADIZA", "XenoCanto", "Inaturalist"]

    filas_tabla = []

    for name_ds in lista_datasets:
        try:
            #  Cargamos el dataset actual usando la función de carga 
            #  usamos una carga temporal para extraer los datos de la tabla comparativa
            df_temp = cargar_dataset_procesado(name_ds)

            if df_temp is not None and not df_temp.empty:
                total_reg = len(df_temp)
                #  Calculamos porcentaje de coordenadas válidas
            
                # Un registro es válido si ambas coordenadas no son nulas 
                coor_validas = 0
                if 'decimalLatitude' in df_temp.columns and 'decimalLongitude' in df_temp.columns:
                    for lat, lon in zip(df_temp['decimalLatitude'], df_temp['decimalLongitude']):
                        if (not pd.isna(lat) and str(lat).strip() not in ["None", "nan", ""]) and \
                           (not pd.isna(lon) and str(lon).strip() not in ["None", "nan", ""]):
                            coor_validas += 1
                porc_coor = (coor_validas / total_reg) * 100 if total_reg > 0 else 0.0


                # Calculamos el  porcentaje de fechas válidas
                # Usamos la misma lógica del 3B, si tiene año en eventDate o en 'year'
                fechas_validas = 0
                tiene_col_year = 'year' in df_temp.columns
                
                for i, celda in enumerate(df_temp['eventDate']):
                    es_valido = False
                    if not pd.isna(celda) and str(celda).strip() not in ["None", "nan", "<NA>", ""]:
                        try:
                            int(str(celda)[:4])
                            es_valido = True
                        except:
                            pass
                    if not es_valido and tiene_col_year:
                        val_year = df_temp['year'].iloc[i]
                        if not pd.isna(val_year) and str(val_year).strip() not in ["None", "nan", "", "0"]:
                            try:
                                int(float(val_year))
                                es_valido = True
                            except:
                                pass
                    if es_valido:
                        fechas_validas += 1
                        
                porc_fechas = (fechas_validas / total_reg) * 100 if total_reg > 0 else 0.0

                #  Guardamos los resultados formateados en un diccionario 
                filas_tabla.append({
                    "Dataset": name_ds,
                    "Cantidad de Registros": f"{total_reg:,}".replace(",", "."), # Formato con punto de miles
                    "Coordenadas Válidas (%)": f"{porc_coor:.2f}%",
                    "Fechas Válidas (%)": f"{porc_fechas:.2f}%"
                })
        except Exception as e:
            # Si algún dataset falla en cargarse, no rompemos la app, solo avisamos
            pass

    # Si logramos recolectar datos, armamos el DataFrame básico y lo mostramos
    if filas_tabla:
        df_comparativo = pd.DataFrame(filas_tabla)
        
        # Seteamos el nombre del dataset como el índice para que la tabla quede súper limpia
        df_comparativo.set_index("Dataset", inplace=True)
        
        # st.table() muestra una tabla e sencilla y sin barras de scroll 
        st.table(df_comparativo)
    else:
        st.warning("No hay suficientes datasets procesados disponibles para mostrar la tabla comparativa.")







# ---------- Si no se pudo cargar el dataset ----------


else:
    st.warning("Por favor, seleccioná un dataset en la barra lateral para empezar a visualizar los gráficos.")