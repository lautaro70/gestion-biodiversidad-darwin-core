import streamlit as st
from common.dataset_utils import leer_logs
from web.barra_lateral import renderizar_barra_lateral

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Estado del sistema")
st.title("Estado del sistema")
st.write("los logs se mostraran a continuación")

try:
    # Intentamos abrir y leer el archivo directamente
    datos_log = leer_logs()
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