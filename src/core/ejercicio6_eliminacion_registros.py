import csv
from pathlib import Path
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas
from core.ejercicio5_actualizacion_registros import obtener_ruta_processed
from core.ejercicio3_validaciones import validar_country_code_unico,validar_incertidumbre_unica,validar_par_coordenadas,validar_fecha_unica

#------6a------

def eliminar_por_id(dataset, id_buscado):
	"""
	Elimina el registro del dataset en donde el id buscado coincida id de un registro 
	Si el id no está, devuelve que no lo encontró	
	"""


	ruta, sep = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)

	idx_id = indices.get('occurrenceID') or indices.get('gbifID')
	
	if idx_id is None:
		return 'No existe columna ID válida'


	ruta_carpeta_procesada = obtener_ruta_processed(dataset)

	eliminado = False

	with open(ruta, 'r', encoding='utf-8') as archivo:
		with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:
			lector = csv.reader(archivo, delimiter=sep)
			escritor = csv.writer(archivo_procesado, delimiter=sep)

			header = next(lector)
			escritor.writerow(header)

			for fila in lector:
				if idx_id < len(fila) and str(fila[idx_id]).strip() == str(id_buscado).strip():
					eliminado = True
					continue  # Saltea para no cargar la fila si el id buscado es igual al id de algun registro del dataset
				escritor.writerow(fila)

	return 'Registro eliminado' if eliminado else 'No se encontró el ID'

#------6b------ 
def eliminar_por_lista_suministrada(dataset, lista_suministrada, columna_de_interes):
	"""
	Elimina los registros cuyos valores en la columna indicada coincidan con los elementos
	de la lista suministrada.
	Si nunca coincide, devuelve No se elimino ningun registro.
	"""
	ruta, sep = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)
	
	idx_interes = indices.get(columna_de_interes)

	if idx_interes is None:
		return 'No existe esa columna'

	lista_suministrada = [elemento.strip() for elemento in lista_suministrada]

	ruta_carpeta_procesada = obtener_ruta_processed(dataset)

	eliminado = False

	with open(ruta, 'r', encoding='utf-8') as archivo:
		with open(ruta_carpeta_procesada, 'w', encoding='utf-8', newline='') as archivo_procesado:
			lector = csv.reader(archivo, delimiter=sep)
			escritor = csv.writer(archivo_procesado, delimiter=sep)

			header = next(lector)
			escritor.writerow(header)

			for fila in lector:
				if idx_interes < len(fila) and fila[idx_interes].strip() in lista_suministrada:
					eliminado = True
					continue  # Saltea si esta en la lista
				escritor.writerow(fila)

	return 'Registros eliminados' if eliminado else 'No se elimino ningun registro'

#------6c------

def eliminar_por_condicion(dataset, valor, columna_de_interes, operador):
    """
    Elimina registros que cumplen una condicion entre los elementos de una columna deseada y el valor designado
    Si la condicion nunca se da, devuelve No se elimino ningun registro 
    """
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    idx_interes = indices.get(columna_de_interes)
    if idx_interes is None:
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

            lector = csv.reader(archivo, delimiter=sep)
            escritor = csv.writer(archivo_procesado, delimiter=sep)

            header = next(lector)
            escritor.writerow(header)

            for fila in lector:
                if idx_interes < len(fila):
                    dato_string = fila[idx_interes].strip()

                    try:
                        dato = float(dato_string)
                    except ValueError:
                        dato = dato_string

                    if operador == '>':
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

def sanitizar_dataset(dataset):
	"""Elimina los registros que no puedan ser validados. 
	En caso de haber campos vacios los tomamos como validos """
	ruta, sep = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)

	ruta_dest = obtener_ruta_processed(dataset)

	ids_vistos = set()
	#set() es una estructura de datos que no tiene orden y no admite duplicados,
	#es util porque es mas rapida para buscar elementos, como en este caso los id  

	idx_id = indices.get('occurrenceID')
	if idx_id is None:
		idx_id = indices.get('gbifID')
	if idx_id is None:
		idx_id = indices.get('id')
			
	idx_lat = indices.get('decimalLatitude')
	idx_lon = indices.get('decimalLongitude')
	idx_fecha = indices.get('eventDate')
	idx_cc = indices.get('countryCode')
	idx_inc = indices.get('coordinateUncertaintyInMeters')

	with open(ruta, 'r', encoding='utf-8') as archivo:
		with open(ruta_dest, 'w', encoding='utf-8', newline='') as archivo_procesado:

			lector = csv.reader(archivo, delimiter=sep)
			escritor = csv.writer(archivo_procesado, delimiter=sep)

			header = next(lector)
			escritor.writerow(header)

			for fila in lector:
				es_valida = True

				# -------- Duplicados --------
				if idx_id is not None:
					if idx_id >= len(fila):
						es_valida = False  
					else:
						id_actual = fila[idx_id].strip()
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
				if es_valida and idx_lat is not None and idx_lon is not None:
					lat = fila[idx_lat] if idx_lat < len(fila) else ""
					lon = fila[idx_lon] if idx_lon < len(fila) else ""
					ok, _ = validar_par_coordenadas(lat, lon)
					if not ok:
						es_valida = False

				# -------- Fecha --------
				if es_valida and idx_fecha is not None and idx_fecha < len(fila):
					fecha = fila[idx_fecha]
					if fecha:
						ok, _ = validar_fecha_unica(fecha)
						if not ok:
							es_valida = False

				# -------- Country code --------
				if es_valida and idx_cc is not None and idx_cc < len(fila):
					cc = fila[idx_cc]
					ok, _ = validar_country_code_unico(cc)
					if not ok:
						es_valida = False

				# -------- Incertidumbre --------
				if es_valida and idx_inc is not None and idx_inc < len(fila):
					inc = fila[idx_inc]
					ok, _ = validar_incertidumbre_unica(inc)
					if not ok:
						es_valida = False

				# -------- Escritura --------
				if es_valida:
					escritor.writerow(fila)

	return "Dataset sanitizado"

#Punto 6f
def reporte_sanitizacion(dataset):
    ruta_orig, sep = obtener_ruta_y_separador(dataset)
    ruta_proc = obtener_ruta_processed(dataset)

    with open(ruta_orig, 'r', encoding='utf-8') as f:
        lector_orig = csv.reader(f, delimiter=sep)
        next(lector_orig) #me corro del encabezado
        total_orig = sum(1 for fila in lector_orig)

    sanitizar_dataset(dataset) #Aca hacemos la sanitización del dataset donde crea el archico en la carpeta de procesados
        
    with open(ruta_proc, 'r', encoding='utf-8') as f:
        lector_proc = csv.reader(f, delimiter=sep)
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