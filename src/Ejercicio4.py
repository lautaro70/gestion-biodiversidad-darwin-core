from pathlib import Path
import csv
from Ejercicio2A import obtener_ruta_y_separador,columnas_dataset

#------4a------

#La estructura que va a representar un registro va a ser un diccionario, donde cada columna va a ser una clave
#y el dato de esa columna será el valor que le corresponde a la clave

#------4b------

def generar_registro_vacio(columnas):
    registro = {}
    for campo in columnas:
        if campo != "id" and campo != "gbifID" and campo != "occurrenceID":
            registro[campo]= None
    return registro
    
