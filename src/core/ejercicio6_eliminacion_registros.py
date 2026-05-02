import csv
from pathlib import Path
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas
from core.ejercicio5_actualizacion_registros import obtener_ruta_processed

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

