from pathlib import Path
import csv
from typing import Dict, List, Tuple, Any

from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import (
    columnas_dataset,
    obtener_indices_columnas
)

from core.ejercicio4_insercion_registros import validar_registro


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def obtener_ruta_processed(dataset: str) -> Path:
    """
    Retorna la ruta del dataset procesado.
    Si no existe, se utilizará posteriormente el raw dataset.
    """

    carpeta_destino = (
        Path(__file__).parent.parent /
        "processed_datasets" /
        dataset
    )

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    return carpeta_destino / f"{dataset}_processed.csv"


def obtener_ruta_lectura(dataset: str) -> Tuple[Path, str]:
    """
    Determina desde dónde leer:
    - processed_datasets si existe
    - raw_datasets si todavía no existe versión procesada
    """

    ruta_processed = obtener_ruta_processed(dataset)

    if ruta_processed.exists():
        ruta = ruta_processed
        _, separador = obtener_ruta_y_separador(dataset)
        return ruta, separador

    ruta_raw, separador = obtener_ruta_y_separador(dataset)
    return Path(ruta_raw), separador


def guardar_dataset_actualizado(
    ruta_origen: Path,
    ruta_destino: Path,
    separador: str,
    filas_actualizadas: List[List[str]]
) -> None:
    """
    Guarda un dataset actualizado en processed_datasets.
    """

    with open(
        ruta_destino,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo_destino:

        escritor = csv.writer(
            archivo_destino,
            delimiter=separador
        )

        for fila in filas_actualizadas:
            escritor.writerow(fila)


# =========================================================
# 5A - BUSCAR REGISTROS
# =========================================================

def buscar_registros(dataset, filtros):
    """
    Permite buscar registros utilizando múltiples columnas.

    Retorna:
    - una lista con los registros completos encontrados
    """

    ruta, separador = obtener_ruta_lectura(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return indices_columnas

    resultados = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector = csv.reader(
            archivo,
            delimiter=separador
        )

        encabezados = next(lector)

        # Recorremos fila por fila
        for fila in lector:

            coincide = True

            # Revisamos todos los filtros pedidos
            for columna, valor_esperado in filtros.items():

                if columna not in indices_columnas:
                    coincide = False
                    break

                indice = indices_columnas[columna]

                if indice >= len(fila):
                    coincide = False
                    break

                valor_real = fila[indice].strip()

                if valor_real != str(valor_esperado).strip():
                    coincide = False
                    break

            # Si cumple todos los filtros,
            # armamos el registro completo
            if coincide:

                registro = {}

                for indice, columna in enumerate(encabezados):

                    if indice < len(fila):
                        registro[columna] = fila[indice]
                    else:
                        registro[columna] = ""

                resultados.append(registro)

    return resultados