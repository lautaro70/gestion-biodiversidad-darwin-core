
from datetime import datetime
from pathlib import Path
import csv



#Punto A

def obtener_fecha_hora_actual():
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d %H:%M:%S")




#Punto B

def registrar_operacion_en_log(mensaje, tipo="INFO"):
    fecha_hora = obtener_fecha_hora_actual()

    ruta_log = Path(__file__).parent.parent.parent / 'logs' / 'operations.log'

#Aca armo la linea del cambio que se estaria realizando
    linea = f"{fecha_hora} | {tipo} | {mensaje}\n"

    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
        #Y aca simplemente ponemos la linea del cambio en el archivo

def inicializar_log():
    ruta_log = Path(__file__).parent.parent.parent / 'logs' / 'operations.log'
    if not ruta_log.exists():
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write("Fecha_Hora | Nivel | Detalles\n")
#-------Punto c


#Lo que hicimos acá por ahora fue modificar las funciones de inserción (punto 4)

#Para agregarlas al log.