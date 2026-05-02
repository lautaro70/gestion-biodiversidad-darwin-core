
from datetime import datetime
from pathlib import Path
import csv



#Ejercicio 1-----

def obtener_fecha_hora_actual():
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d %H:%M:%S")
