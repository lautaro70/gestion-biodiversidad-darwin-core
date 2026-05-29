import streamlit as st
from common.barra_lateral import renderizar_barra_lateral
from core.ejercicio3visualizacion import obtener_datos_barras 
import matplotlib.pyplot as plt

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Visualización")
st.title("Visualización")

#------Implementacion 3a

if "df_actual" in st.session_state and st.session_state["df_actual"] is not None:
    df = st.session_state["df_actual"]
    
    st.markdown("---")
    st.header("Distribución Geográfica de Registros")
    
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
        
        # ajustamos los márgenes del lienzo
        plt.tight_layout()
        
        # Mostramos el gráfico final en la interfaz de Streamlit
        st.pyplot(fig)
        
    else:
        # Si la serie está vacía 
        st.info("No se encontraron datos geográficos suficientes en este dataset para generar el gráfico.")

else:
    # Si entran a la página sin haber elegido un archivo en el sidebar 
    st.warning("Por favor, seleccioná un dataset en la barra lateral para empezar a visualizar los gráficos.")