import csv
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas
from core.ejercicio5_actualizacion_registros import obtener_ruta_processed
from core.ejercicio3_validaciones import (
    validar_country_code_unico,
    validar_incertidumbre_unica,
    validar_par_coordenadas,
    validar_fecha_unica
)
from core.ejercicio7_registro_de_operaciones import registrar_operacion_en_log

#------6a------
def eliminar_por_id(dataset: str, id_buscado: str) -> str:
    """
    Elimina el registro cuyo occurrenceID coincida con el id buscado.
    Implementa 7.E (éxito) y 7.F (errores).
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    indice_id = indices.get('occurrenceID') 
    
    if indice_id is None:
        # ----7f: Error por falta de columna identificadora
        error_msj = 'No existe columna ID válida'
        registrar_operacion_en_log(f"Punto 7.F: DELETE fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    ruta_carpeta_procesada = obtener_ruta_processed(dataset)

    eliminado = False

    with open(ruta, 'r', encoding='utf-8') as archivo:
        with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:
            lector = csv.reader(archivo, delimiter=separador)
            escritor = csv.writer(archivo_procesado, delimiter=separador)

            encabezado = next(lector)
            escritor.writerow(encabezado)

            for fila in lector:
                if indice_id < len(fila) and str(fila[indice_id]).strip() == str(id_buscado).strip():
                    eliminado = True
                    continue  # Saltea para no cargar la fila
                escritor.writerow(fila)

    cantidad_eliminados = 1 if eliminado else 0
    
    if eliminado:
        # -----7e: Registro de éxito con tipo delete para que se vea mas claro, lo cambie
        mensaje_log = f"Punto 7.E: Eliminación en {dataset}. Registros eliminados: {cantidad_eliminados}"
        registrar_operacion_en_log(mensaje_log, "DELETE")
        return f"Registro eliminado. Total de afectados: {cantidad_eliminados}"
    else:
        # -------7f: Error porque el ID no existía en el dataset
        error_msj = f"No se encontró el ID '{id_buscado}'. Total de afectados: 0"
        registrar_operacion_en_log(f"Punto 7.F: DELETE fallido en {dataset}. ID inexistente.", "ERROR")
        return error_msj


#---------6b
def eliminar_por_lista_suministrada(dataset: str, lista_suministrada: list[str], columna_de_interes: str) -> str:
    """
    Elimina los registros cuyos valores en la columna indicada coincidan
    con alguno de los elementos de la lista suministrada.
    Genera un nuevo archivo en processed_datasets con los registros restantes.
    Devuelve: mensaje indicando el resultado de la operación.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    indice_columna = indices.get(columna_de_interes)

    if indice_columna is None:
        return 'No existe esa columna'

    lista_suministrada = [elemento.strip() for elemento in lista_suministrada]
    ruta_carpeta_procesada = obtener_ruta_processed(dataset)

    # Cambiamos el booleano por un contador para cumplir mejor el Punto 7.E
    cantidad_eliminados = 0

    with open(ruta, 'r', encoding='utf-8') as archivo:
        with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:
            lector = csv.reader(archivo, delimiter=separador)
            escritor = csv.writer(archivo_procesado, delimiter=separador)

            encabezado = next(lector)
            escritor.writerow(encabezado)

            for fila in lector:
                if indice_columna < len(fila) and fila[indice_columna].strip() in lista_suministrada:
                    cantidad_eliminados += 1 # Contamos cada eliminación
                    continue  # Saltea si esta en la lista
                escritor.writerow(fila)
    
    # --- PUNTO 7e
    
    # Mensaje para el log
    mensaje_log = f"Punto 7.E: Eliminación por lista en {dataset}. Registros eliminados: {cantidad_eliminados}"
    registrar_operacion_en_log(mensaje_log, "WARNING")

    # Retornamos el mensaje indicando la cantidad (Punto 7.E)
    if cantidad_eliminados > 0:
        return f"Proceso completado. Total de eliminados: {cantidad_eliminados}"
    else:
        return f"No se encontraron coincidencias. Total de afectados: {cantidad_eliminados}"

#------6c------
def eliminar_por_condicion(dataset: str, valor: str, columna_de_interes: str, operador: str) -> str:
    """
    Elimina registros que cumplen una condición.
    Implementa 7.E (conteo) y 7.F (errores de validación).
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    indice_columna = indices.get(columna_de_interes)
    if indice_columna is None:
        # PUNTO 7.F: Error si la columna no existe
        error_msj = f"Columna '{columna_de_interes}' no encontrada."
        registrar_operacion_en_log(f"Punto 7.F: DELETE por condición fallido en {dataset}. {error_msj}", "ERROR")
        return 'No existe esa columna'

    ruta_carpeta_procesada = obtener_ruta_processed(dataset)
    cantidad_eliminados = 0
    
    try:
        valor_procesado = float(valor)
    except ValueError:
        valor_procesado = valor

    if operador not in ['>', '>=', '<', '<=', '==', '!=']:
        # --------7f: Error si el operador es inválido
        registrar_operacion_en_log(f"Punto 7.F: DELETE por condición fallido en {dataset}. Operador '{operador}' inválido.", "ERROR")
        return 'Operador no válido'

    with open(ruta, 'r', encoding='utf-8') as archivo:
        with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:

            lector = csv.reader(archivo, delimiter=separador)
            escritor = csv.writer(archivo_procesado, delimiter=separador)

            encabezado = next(lector)
            escritor.writerow(encabezado)

            for fila in lector:
                if indice_columna < len(fila):
                    dato_string = fila[indice_columna].strip()

                    try:
                        dato = float(dato_string)
                    except ValueError:
                        dato = dato_string

                    if type(dato) != type(valor_procesado):
                        condicion = False
                    elif operador == '>':
                        condicion = dato > valor_procesado
                    elif operador == '>=':
                        condicion = dato >= valor_procesado
                    elif operador == '<':
                        condicion = dato < valor_procesado
                    elif operador == '<=':
                        condicion = dato <= valor_procesado
                    elif operador == '==':
                        condicion = dato == valor_procesado
                    else:  # '!='
                        condicion = dato != valor_procesado

                    if condicion:
                        cantidad_eliminados += 1 
                        continue

                escritor.writerow(fila)

    # --- 7e y c ---
    if cantidad_eliminados > 0:
        # Registro de éxito con tipo DELETE
        mensaje_log = f"Punto 7.E: Eliminación por condición en {dataset}. Registros eliminados: {cantidad_eliminados}"
        registrar_operacion_en_log(mensaje_log, "DELETE")
        return f"Registros eliminados correctamente. Total de afectados: {cantidad_eliminados}"
    else:
        # ------7f: Si no se eliminó nada, se registra como error de búsqueda/condición
        registrar_operacion_en_log(f"Punto 7.F: DELETE en {dataset} sin coincidencias para la condición.", "ERROR")
        return f"No se eliminó ningún registro. Total de afectados: 0"
    
    
#------6e------
def sanitizar_dataset(dataset: str) -> str:
    """
    Elimina automáticamente los registros que no pasen las validaciones del ejercicio 3.
    Valida: duplicados, coordenadas, fechas, countryCode e incertidumbre.
    Los campos vacíos se consideran válidos exceptuando el ID, ya que consideramos que si 
    si no se puede identificar, no es un registro valido.
    Genera un nuevo archivo en processed_datasets con los registros válidos.
    Devuelve: mensaje de confirmación.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    ruta_dest = obtener_ruta_processed(dataset)

    #------7f
    if ruta is None or indices is None:
        registrar_operacion_en_log(
            f"Punto 7.F: DELETE fallido. Dataset '{dataset}' inválido.",
            "ERROR"
        )
        return "Dataset no reconocido o inválido."
    
    cantidad_eliminados = 0 #-----7e
    ids_vistos = set()

    indice_id = indices.get('occurrenceID')
    if indice_id is None:
        indice_id = indices.get('gbifID')
    if indice_id is None:
        indice_id = indices.get('id')
            
    indice_latitud = indices.get('decimalLatitude')
    indice_longitud = indices.get('decimalLongitude')
    indice_fecha = indices.get('eventDate')
    indice_country_code = indices.get('countryCode')
    indice_incertidumbre = indices.get('coordinateUncertaintyInMeters')

    with open(ruta, 'r', encoding='utf-8') as archivo:
        with open(ruta_dest, 'w', encoding='utf-8', newline='') as archivo_procesado:

            lector = csv.reader(archivo, delimiter=separador)
            escritor = csv.writer(archivo_procesado, delimiter=separador)

            encabezado = next(lector)
            escritor.writerow(encabezado)

            for fila in lector:
                es_valida = True

                # -------- Duplicados --------
                if indice_id is not None:
                    if indice_id >= len(fila):
                        es_valida = False  
                        mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: INDICE ID FUERA DE RANGO"
                        registrar_operacion_en_log(mensaje_fallo, "ERROR")
                    else:
                        id_actual = fila[indice_id].strip()
                        if id_actual == "":
                            es_valida = False  
                            mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: ID VACIO"
                            registrar_operacion_en_log(mensaje_fallo, "ERROR")
                           
                        elif id_actual in ids_vistos:
                            es_valida = False 
                            mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: ID DUPLICADO"
                            registrar_operacion_en_log(mensaje_fallo, "ERROR")
                           
                        else:
                            ids_vistos.add(id_actual)
                else:                            
                    es_valida = False 
                    mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: COLUMNA ID NO EXISTE"
                    registrar_operacion_en_log(mensaje_fallo, "ERROR")

                # -------- Coordenadas --------
                if es_valida and indice_latitud is not None and indice_longitud is not None:
                    lat = fila[indice_latitud] if indice_latitud < len(fila) else ""
                    lon = fila[indice_longitud] if indice_longitud < len(fila) else ""
                    es_valido, _ = validar_par_coordenadas(lat, lon)
                    if not es_valido:
                        es_valida = False
                        mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: COORDENADA INVALIDA"
                        registrar_operacion_en_log(mensaje_fallo, "ERROR")
                

                # -------- Fecha --------
                columnas_fecha = ['eventDate', 'modified', 'verbatimEventDate', 'dateIdentified']

                for columna in columnas_fecha:
                    indice_fecha = indices.get(columna)
                    if es_valida and indice_fecha is not None and indice_fecha < len(fila):
                        fecha = fila[indice_fecha]

                        if fecha and str(fecha).strip():
                            es_valido, _ = validar_fecha_unica(fecha)
                            if not es_valido:
                                es_valida = False
                                mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: FECHA INVALIDA"
                                registrar_operacion_en_log(mensaje_fallo, "ERROR")
                

                # -------- Country code --------
                if es_valida and indice_country_code is not None and indice_country_code < len(fila):
                    country_code = fila[indice_country_code]
                    es_valido, _ = validar_country_code_unico(country_code)
                    if not es_valido:
                        es_valida = False
                        mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: COUNTRYCODE INVALIDO"
                        registrar_operacion_en_log(mensaje_fallo, "ERROR")

                # -------- Incertidumbre --------
                if es_valida and indice_incertidumbre is not None and indice_incertidumbre < len(fila):
                    incertidumbre = fila[indice_incertidumbre]
                    es_valido, _ = validar_incertidumbre_unica(incertidumbre)
                    if not es_valido:
                        es_valida = False
                        mensaje_fallo = f"Punto 7.F: Error en DELETE para {dataset}. Detalle: INCERTIDUMBRE INVALIDA"
                        registrar_operacion_en_log(mensaje_fallo, "ERROR")

                # -------- Escritura --------
                if es_valida:
                    escritor.writerow(fila)
                else:
                    cantidad_eliminados += 1 #----------7e

    # ---Punto 7e
    mensaje_log = f"Punto 7.E: Sanitización automática en {dataset}. Registros eliminados por no cumplir requisitos: {cantidad_eliminados}"
    registrar_operacion_en_log(mensaje_log, "WARNING")

    return f"Dataset sanitizado. Registros eliminados: {cantidad_eliminados}"


#Punto 6f
def reporte_sanitizacion(dataset: str) -> int:
    """
    Ejecuta la sanitización del dataset e imprime un reporte con:
    - cantidad de registros iniciales
    - cantidad de registros eliminados
    - cantidad de registros finales
    - porcentaje eliminado sobre el total
    Devuelve: cantidad de registros en el archivo procesado.
    """
    ruta_orig, separador = obtener_ruta_y_separador(dataset)
    ruta_proc = obtener_ruta_processed(dataset)

    with open(ruta_orig, 'r', encoding='utf-8') as archivo:
        lector_orig = csv.reader(archivo, delimiter=separador)
        next(lector_orig) # me corro del encabezado
        total_orig = sum(1 for fila in lector_orig)

    # Aca hacemos la sanitización del dataset donde crea el archivo en la carpeta de procesados
    sanitizar_dataset(dataset) 
        
    with open(ruta_proc, 'r', encoding='utf-8') as archivo:
        lector_proc = csv.reader(archivo, delimiter=separador)
        next(lector_proc)
        total_proc = sum(1 for fila in lector_proc) # Obtenemos el total de procesados 

    # Cálculos para obtener el total de eliminados
    eliminados = total_orig - total_proc

    # -------- 7e Registro en Log
    mensaje_reporte = f"Punto 7.E: Reporte final generado para {dataset}. Finales: {total_proc}, Eliminados: {eliminados}"
    registrar_operacion_en_log(mensaje_reporte, "INFO")
    
#-----sigue el 6f 

    if total_orig > 0:
        porcentaje = (eliminados * 100) / total_orig
    else:
        porcentaje = 0

    # Informamos por pantalla
    print("================================")
    print("      REPORTE DEL PUNTO 6.F     ")
    print("================================")
    print(f"Registros iniciales: {total_orig}")
    print(f"Registros eliminados: {eliminados}")
    print(f"Registros finales:    {total_proc}")
    print(f"Porcentaje eliminado: {porcentaje:.2f}%")
    print("================================")
        
    return total_proc