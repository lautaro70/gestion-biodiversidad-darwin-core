
from datetime import datetime
from pathlib import Path

#------7a------
def obtener_fecha_hora_actual() -> str:
    """
    Retorna la fecha y hora actual en formato legible: 'YYYY-MM-DD HH:MM:SS'.
    """
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d %H:%M:%S")

#------7b------
def registrar_operacion_en_log(mensaje: str, tipo: str = "INFO") -> None:
    """
    Escribe una línea en el archivo de log operations.log con el formato:
    'fecha_hora | tipo | mensaje'.
    Crea el archivo si no existe. Agrega sin sobrescribir el contenido previo.
    """
    fecha_hora = obtener_fecha_hora_actual()

    ruta_log = Path(__file__).parent.parent.parent / 'logs' / 'operations.log'

#Aca armo la linea del cambio que se estaria realizando
    linea = f"{fecha_hora} | {tipo} | {mensaje}\n"

    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
        #Y aca simplemente ponemos la linea del cambio en el archivo

def inicializar_log() -> None:
    """
    Crea el archivo operations.log con el encabezado si no existe todavía.
    Útil para inicializar el sistema de logs antes de la primera operación.
    """
    ruta_log = Path(__file__).parent.parent.parent / 'logs' / 'operations.log'
    if not ruta_log.exists():
        with open(ruta_log, "w", encoding="utf-8") as f:
            f.write("Fecha_Hora | Nivel | Detalles\n")
#-------Punto c


#Lo que hicimos acá por ahora fue modificar las funciones de inserción (punto 4)

#Para agregarlas al log.


#7d-----

#Exactamente lo mismo que el c, modificamos las funciones del 5 para agregarlas al log