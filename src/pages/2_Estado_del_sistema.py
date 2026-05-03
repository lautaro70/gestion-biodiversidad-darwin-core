import streamlit as st
import csv 
import os

st.set_page_config(page_title="Estado del sistema")
st.title("Estado del sistema")
st.write("los logs se mostraran a continuación")

ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_log = os.path.join(ruta_actual, "..", "..", "logs", "operations.log")

try:
    # Intentamos abrir y leer el archivo directamente
    with open(ruta_log, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        #Lo dejamos en lista asi crea una unica tabla
        datos_log = list(lector)
        
    # Si lo pudimos leer, verificamos que no esté vacío para mostrarlo
    if len(datos_log) > 0:
        st.dataframe(datos_log)
    else:
        st.info("El archivo de logs se encuentra vacío. Aún no hay operaciones registradas.")

except FileNotFoundError:
    st.warning("Aún no se han registrado operaciones en el sistema (archivo 'logs/operations.log' no encontrado).")
except PermissionError:
    st.error("Error de permisos: No se tiene acceso de lectura al archivo de logs.")
except Exception as e:
    #Para cualquier otro error inesperado (ej. archivo corrupto)
    st.error(f"Ocurrió un error crítico e inesperado al intentar leer los logs: {e}")