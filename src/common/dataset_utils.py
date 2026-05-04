import csv
from common.constants import DATASETS, LOG_PATH

def obtener_ruta_y_separador(dataset: str) -> tuple:
    """
    Retorna la ruta y el separador asociados a un dataset.
    """

    informacion_dataset = DATASETS.get(dataset)

    if informacion_dataset is None:
        return None, None

    return (
        informacion_dataset["path"],
        informacion_dataset["separator"]
    )


def leer_logs()-> list:
    """Lee el archivo de operaciones y retorna una lista de listas.
    Lanza FileNotFoundError si el archivo no existe."""
    if not LOG_PATH.exists():
        raise FileNotFoundError
        
    with open(LOG_PATH, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return list(lector)