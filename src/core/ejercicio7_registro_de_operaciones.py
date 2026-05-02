
from datetime import datetime
from pathlib import Path
import csv



#Punto B

def obtener_fecha_hora_actual():
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d %H:%M:%S")




#Punto A

def registrar_operacion_en_log(mensaje, tipo="INFO"):
    fecha_hora = obtener_fecha_hora_actual()

    ruta_log = Path("logs") / "operations.log"
#Aca armo la linea del cambio que se estaria realizando
    linea = f"{fecha_hora} - {tipo} - {mensaje}\n"

    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
        #Y aca simplemente ponemos la linea del cambio en el archivo