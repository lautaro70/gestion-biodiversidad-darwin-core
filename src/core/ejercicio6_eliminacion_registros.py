import csv
from pathlib import Path
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas


def eliminar_por_id(dataset, id_buscado):
	ruta, sep = obtener_ruta_y_separador(dataset)
	indices = obtener_indices_columnas(dataset)

	idx_id = indices.get('occurrenceID') or indices.get('gbifID')
	
	if idx_id is None:
		return 'No existe columna ID válida'


	carpeta_procesada = Path(__file__).parent.parent / 'processed_datasets' / dataset
	carpeta_procesada.mkdir(parents=True,exist_ok=True)
	ruta_carpeta_procesada = carpeta_procesada / f'{dataset}_processed.csv'

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
