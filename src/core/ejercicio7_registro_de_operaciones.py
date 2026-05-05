from datetime import datetime
from common.constants import LOG_PATH

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

#Aca armo la linea del cambio que se estaria realizando
    linea = f"{fecha_hora} | {tipo} | {mensaje}\n"

    with open(LOG_PATH, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
        #Y aca simplemente ponemos la linea del cambio en el archivo

def inicializar_log() -> None:
    """
    Crea el archivo operations.log con el encabezado si no existe todavía.
    Útil para inicializar el sistema de logs antes de la primera operación.
    """
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    if not LOG_PATH.exists():
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write("Fecha_Hora | Nivel | Detalles\n")

#-------Punto 7c

# En este punto se modificaron las funciones
# del ejercicio 4 (Inserción de registros)
# para integrar el sistema de logs.

# Se registran automáticamente:
#
# - inserciones individuales exitosas
# - inserciones masivas
# - cantidad de registros insertados
# - errores de validación
# - errores por datasets inexistentes
# - operaciones canceladas
#
# Todas las operaciones quedan almacenadas
# dentro de operations.log.


#------7d-----

# En este punto se modificaron las funciones
# del ejercicio 5 (Actualización de registros)
# para agregar registros automáticos en el log.

# Se registran:
#
# - actualizaciones simples
# - actualizaciones múltiples
# - cantidad de registros afectados
# - errores de columnas inexistentes
# - errores de IDs inválidos
# - fallos de validación
#
# Cada operación UPDATE queda registrada
# en operations.log con su tipo correspondiente.


#------7e-----

# En este punto se integró el sistema de logs
# con las funciones del ejercicio 6
# (Eliminación y sanitización de registros).

# Se registran:
#
# - eliminaciones por ID
# - eliminaciones por listas
# - eliminaciones por condición
# - sanitización automática de datasets
# - generación de reportes
# - cantidad de registros eliminados
#
# También se registran operaciones
# sin coincidencias encontradas.


#------7f-----

# En este punto se implementó el registro
# automático de errores del sistema.

# Se utiliza el tipo:
# ERROR

# Algunos errores registrados:
#
# - datasets inexistentes
# - columnas inválidas
# - IDs inexistentes
# - operadores inválidos
# - errores de validación
# - registros inconsistentes
# - operaciones canceladas
#
# Esto permite mantener trazabilidad
# completa de fallos y facilita el debugging.