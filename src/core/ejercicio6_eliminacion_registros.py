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

#------6a------
def eliminar_por_id(dataset: str, id_buscado: str) -> str:
	"""
    Elimina el registro cuyo occurrenceID coincida con el id buscado.
    Genera un nuevo archivo en processed_datasets sin el registro eliminado.
    Si el id no existe, informa el error.
    Devuelve: mensaje indicando el resultado de la operación.
    """

	ruta, separador = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)

	indice_id = indices.get('occurrenceID') 
	
	if indice_id is None:
		return 'No existe columna ID válida'

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
					continue  # Saltea para no cargar la fila si el id buscado es igual al id de algun registro del dataset
				escritor.writerow(fila)

	return 'Registro eliminado' if eliminado else 'No se encontró el ID'


#------6b------ 
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

	eliminado = False

	with open(ruta, 'r', encoding='utf-8') as archivo:
		with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:
			lector = csv.reader(archivo, delimiter=separador)
			escritor = csv.writer(archivo_procesado, delimiter=separador)

			encabezado = next(lector)
			escritor.writerow(encabezado)

			for fila in lector:
				if indice_columna < len(fila) and fila[indice_columna].strip() in lista_suministrada:
					eliminado = True
					continue  # Saltea si esta en la lista
				escritor.writerow(fila)

	return 'Registros eliminados' if eliminado else 'No se elimino ningun registro'


#------6c------
def eliminar_por_condicion(dataset: str, valor: str, columna_de_interes: str, operador: str) -> str:
    """
    Elimina registros que cumplen una condición entre los valores de una columna
    y el valor indicado. Operadores válidos: !=, ==, >, >=, <, <=.
    Genera un nuevo archivo en processed_datasets con los registros restantes.
    Devuelve: mensaje indicando el resultado de la operación.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    indice_columna = indices.get(columna_de_interes)
    if indice_columna is None:
        return 'No existe esa columna'

    ruta_carpeta_procesada = obtener_ruta_processed(dataset)

    eliminado = False
    
    try:
        valor_procesado = float(valor)
    except ValueError:
        valor_procesado = valor

    if operador not in ['>', '>=', '<', '<=', '==', '!=']:
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
                        eliminado = True
                        continue

                escritor.writerow(fila)

    return 'Registros eliminados' if eliminado else 'No se elimino ningun registro'


#------6e------

def sanitizar_dataset(dataset: str) -> str:
	"""
    Elimina automáticamente los registros que no pasen las validaciones del ejercicio 3.
    Valida: duplicados, coordenadas, fechas, countryCode e incertidumbre.
    Los campos vacíos se consideran válidos.
    Genera un nuevo archivo en processed_datasets con los registros válidos.
    Devuelve: mensaje de confirmación.
    """
	ruta, separador = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)

	ruta_dest = obtener_ruta_processed(dataset)

	ids_vistos = set()
	#set() es una estructura de datos que no tiene orden y no admite duplicados,
	#es util porque es mas rapida para buscar elementos, como en este caso los id  

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
					else:
						id_actual = fila[indice_id].strip()
						if id_actual == "":
							es_valida = False  
						elif id_actual in ids_vistos:
							es_valida = False 
						else:
							ids_vistos.add(id_actual)
							
				# No reutilizo la funcion del ejercicio 3d de duplicados porque:
				# - recorre todo el dataset
				# - devuelve lista de duplicados
				# y aca solo queremos eliminar en una sola pasada

				# -------- Coordenadas --------
				if es_valida and indice_latitud is not None and indice_longitud is not None:
					lat = fila[indice_latitud] if indice_latitud < len(fila) else ""
					lon = fila[indice_longitud] if indice_longitud < len(fila) else ""
					es_valido, _ = validar_par_coordenadas(lat, lon)
					if not es_valido:
						es_valida = False

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

				# -------- Country code --------
				if es_valida and indice_country_code is not None and indice_country_code < len(fila):
					country_code = fila[indice_country_code]
					es_valido, _ = validar_country_code_unico(country_code)
					if not es_valido:
						es_valida = False

				# -------- Incertidumbre --------
				if es_valida and indice_incertidumbre is not None and indice_incertidumbre < len(fila):
					incertidumbre = fila[indice_incertidumbre]
					es_valido, _ = validar_incertidumbre_unica(incertidumbre)
					if not es_valido:
						es_valida = False

				# -------- Escritura --------
				if es_valida:
					escritor.writerow(fila)

	return "Dataset sanitizado"


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
        next(lector_orig) #me corro del encabezado
        total_orig = sum(1 for fila in lector_orig)

    sanitizar_dataset(dataset) #Aca hacemos la sanitización del dataset donde crea el archico en la carpeta de procesados
        
    with open(ruta_proc, 'r', encoding='utf-8') as archivo:
        lector_proc = csv.reader(archivo, delimiter=separador)
        next(lector_proc)
        total_proc = sum(1 for fila in lector_proc) #Obtenemos el total de procesados 

    #Aca ya hacemos los calculos para obtener el total de eliminados y el porcentaje

    eliminados = total_orig - total_proc
    if total_orig > 0:
        porcentaje = (eliminados * 100) / total_orig
    else:
        porcentaje = 0

#Y aca informamos 
    print("================================")
    print("      REPORTE DEL PUNTO 6.F     ")
    print("================================")
    print(f"Registros iniciales: {total_orig}")
    print(f"Registros eliminados: {eliminados}")
    print(f"Registros finales:   {total_proc}")
    print(f"Porcentaje eliminado: {porcentaje:.2f}%")
    print("================================")
        
    return total_proc