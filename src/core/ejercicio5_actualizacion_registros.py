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

# =========================================================
# 5B - ACTUALIZAR UN CAMPO
# =========================================================

def actualizar_campo_registro(
    dataset,
    columna_identificadora,
    valor_identificador,
    columna_actualizar,
    nuevo_valor
):
    """
    Permite actualizar UN campo de un registro específico.

    Parámetros:
    - dataset: nombre del dataset
    - columna_identificadora: columna utilizada para buscar el registro
    - valor_identificador: valor que identifica al registro
    - columna_actualizar: columna que se quiere modificar
    - nuevo_valor: nuevo valor para esa columna

    Retorna:
    - mensaje indicando el resultado de la operación
    """

    ruta_lectura, separador = obtener_ruta_lectura(dataset)

    ruta_destino = obtener_ruta_processed(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return indices_columnas

    # Verificamos que existan las columnas
    if columna_identificadora not in indices_columnas:
        return (
            f"No existe la columna "
            f"'{columna_identificadora}'"
        )

    if columna_actualizar not in indices_columnas:
        return (
            f"No existe la columna "
            f"'{columna_actualizar}'"
        )

    indice_identificador = indices_columnas[
        columna_identificadora
    ]

    indice_actualizar = indices_columnas[
        columna_actualizar
    ]

    filas_actualizadas = []

    registro_encontrado = False

    with open(
        ruta_lectura,
        'r',
        encoding='utf-8'
    ) as archivo:

        lector = csv.reader(
            archivo,
            delimiter=separador
        )

        encabezados = next(lector)

        # Guardamos encabezados
        filas_actualizadas.append(encabezados)

        # Recorremos registros
        for fila in lector:

            nueva_fila = fila.copy()

            # Verificamos si es el registro buscado
            if (
                indice_identificador < len(fila)
                and fila[indice_identificador].strip()
                == str(valor_identificador).strip()
            ):

                registro_encontrado = True

                # Si la fila es más corta,
                # agregamos espacios vacíos
                while len(nueva_fila) <= indice_actualizar:
                    nueva_fila.append("")

                # Actualizamos el valor
                nueva_fila[indice_actualizar] = str(
                    nuevo_valor
                )

            filas_actualizadas.append(nueva_fila)

    if not registro_encontrado:
        return (
            f"No se encontró ningún registro con "
            f"{columna_identificadora} = "
            f"'{valor_identificador}'"
        )

    # Guardamos nueva versión del dataset
    guardar_dataset_actualizado(
        ruta_origen=ruta_lectura,
        ruta_destino=ruta_destino,
        separador=separador,
        filas_actualizadas=filas_actualizadas
    )

    return "Registro actualizado correctamente."