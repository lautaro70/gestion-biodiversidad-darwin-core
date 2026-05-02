import streamlit as st

#LOGS_PATH=Path(__file__).parent.parent #falta hacer el camino correcto a logs, adicionalmente esto tenerlo en las constantes, aca solo se hacen cuestiones esteticas
st.set_page_config(page_title="Estado del sistema")
st.title("Estado del sistema")
st.write("los logs se mostraran a continuación")

#with open(LOGS_PATH, "r") as file:#para iterar utilizamos en un archivo externo y que nos devuelvan los logs
    #st.write(file.read)