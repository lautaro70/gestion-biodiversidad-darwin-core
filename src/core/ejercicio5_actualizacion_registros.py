from pathlib import Path
import csv
from typing import List, Tuple

from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import (
    columnas_dataset,
    obtener_indices_columnas
)

from core.ejercicio4_insercion_registros import validar_registro
from core.ejercicio7_registro_de_operaciones import registrar_operacion_en_log


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def obtener_ruta_processed(dataset: str) -> Path:
    """
    Retorna la ruta del dataset procesado.
    Si no existe, se utilizará posteriormente el raw dataset.
    """

    carpeta_destino = (
    Path(__file__).parent.parent.parent /
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

def buscar_registros(dataset: str, filtros: dict) -> list[dict]:
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
    dataset: str,
    columna_identificadora: str,
    valor_identificador: str,
    columna_actualizar: str,
    nuevo_valor: str
) -> str:
    """
    Permite actualizar UN campo de un registro específico.
    Implementa 7.D (éxito) y 7.F (errores).
    """

    ruta_lectura, separador = obtener_ruta_lectura(dataset)
    ruta_destino = obtener_ruta_processed(dataset)
    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        # -----------------7f: Error si no se pueden obtener los índices (como un archivo inexistente)
        registrar_operacion_en_log(f"Punto 7.F: UPDATE fallido en {dataset}. Motivo: {indices_columnas}", "ERROR")
        return indices_columnas

    # Verificamos que existan las columnas
    if columna_identificadora not in indices_columnas:
        # ----------7f: Error de columna identificadora inexistente
        error_msj = f"No existe la columna '{columna_identificadora}'"
        registrar_operacion_en_log(f"Punto 7.F: UPDATE fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    if columna_actualizar not in indices_columnas:
        # -------7f Error de columna a actualizar inexistente
        error_msj = f"No existe la columna '{columna_actualizar}'"
        registrar_operacion_en_log(f"Punto 7.F: UPDATE fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    indice_identificador = indices_columnas[columna_identificadora]
    indice_actualizar = indices_columnas[columna_actualizar]

    filas_actualizadas = []
    registro_encontrado = False

    with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        encabezados = next(lector)

        # Guardamos encabezados
        filas_actualizadas.append(encabezados)

        # Recorremos registros
        for fila in lector:
            nueva_fila = fila.copy()

            # Verificamos si es el registro buscado
            if (
                indice_identificador < len(fila)
                and fila[indice_identificador].strip() == str(valor_identificador).strip()
            ):
                registro_encontrado = True

                # Si la fila es más corta, agregamos espacios vacíos
                while len(nueva_fila) <= indice_actualizar:
                    nueva_fila.append("")

                # Actualizamos el valor
                nueva_fila[indice_actualizar] = str(nuevo_valor)

            filas_actualizadas.append(nueva_fila)

    if not registro_encontrado:
        # ---------7f: Error si el ID solicitado no existe en el dataset
        error_msj = f"No se encontró ningún registro con {columna_identificadora} = '{valor_identificador}'"
        registrar_operacion_en_log(f"Punto 7.F: UPDATE fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    # Guardamos nueva versión del dataset
    guardar_dataset_actualizado(
        ruta_origen=ruta_lectura,
        ruta_destino=ruta_destino,
        separador=separador,
        filas_actualizadas=filas_actualizadas
    )

    # --------punto 7d
    cantidad_afectados = 1
    mensaje = f"Punto 7.D: Actualización de campo '{columna_actualizar}' en {dataset}. Afectados: {cantidad_afectados}"
    registrar_operacion_en_log(mensaje, "UPDATE")

    return f"Registro actualizado correctamente. Total de afectados: {cantidad_afectados}"
# =========================================================
# 5C - ACTUALIZAR MÚLTIPLES CAMPOS
# =========================================================

def actualizar_multiples_campos(
    dataset: str,
    columna_identificadora: str,
    valor_identificador: str,
    nuevos_valores: dict
) -> str:
    """
    Permite actualizar múltiples campos de un mismo registro.
    Implementa 7.D (éxito) y 7.F (errores).
    """

    ruta_lectura, separador = obtener_ruta_lectura(dataset)
    ruta_destino = obtener_ruta_processed(dataset)
    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        # ------7f: Error si el dataset no puede ser leído o no existe
        registrar_operacion_en_log(f"Punto 7.F: UPDATE múltiple fallido en {dataset}. Motivo: {indices_columnas}", "ERROR")
        return indices_columnas

    # Verificamos que exista la columna identificadora
    if columna_identificadora not in indices_columnas:
        # ----------7f: Registro de error por columna de búsqueda inexistente
        error_msj = f"No existe la columna '{columna_identificadora}'"
        registrar_operacion_en_log(f"Punto 7.F: UPDATE múltiple fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    # Verificamos que existan todas las columnas a modificar
    for columna in nuevos_valores:
        if columna not in indices_columnas:
            # -----------7f: Registro de error por columna de actualización inexistente
            error_msj = f"No existe la columna '{columna}'"
            registrar_operacion_en_log(f"Punto 7.F: UPDATE múltiple fallido en {dataset}. {error_msj}", "ERROR")
            return error_msj

    indice_identificador = indices_columnas[columna_identificadora]
    filas_actualizadas = []
    registro_encontrado = False

    with open(ruta_lectura, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=separador)
        encabezados = next(lector)

        # Guardamos encabezados
        filas_actualizadas.append(encabezados)

        # Recorremos fila por fila
        for fila in lector:
            nueva_fila = fila.copy()

            # Verificamos si es el registro buscado
            if (
                indice_identificador < len(fila)
                and fila[indice_identificador].strip() == str(valor_identificador).strip()
            ):
                registro_encontrado = True

                # Aplicamos todas las modificaciones
                for columna, nuevo_valor in nuevos_valores.items():
                    indice_columna = indices_columnas[columna]

                    # Si la fila es corta, agregamos posiciones vacías
                    while len(nueva_fila) <= indice_columna:
                        nueva_fila.append("")

                    nueva_fila[indice_columna] = str(nuevo_valor)

            filas_actualizadas.append(nueva_fila)

    if not registro_encontrado:
        # ---------7f: Error si el ID no existe en el archivo
        error_msj = f"No se encontró ningún registro con {columna_identificadora} = '{valor_identificador}'"
        registrar_operacion_en_log(f"Punto 7.F: UPDATE múltiple fallido en {dataset}. {error_msj}", "ERROR")
        return error_msj

    # Guardamos nueva versión del dataset
    guardar_dataset_actualizado(
        ruta_origen=ruta_lectura,
        ruta_destino=ruta_destino,
        separador=separador,
        filas_actualizadas=filas_actualizadas
    )

    # ----7d: Registro de éxito con tipo update
    cantidad_afectados = 1
    mensaje = f"Punto 7.D: Actualización múltiple en {dataset}. Afectados: {cantidad_afectados}"
    registrar_operacion_en_log(mensaje, "UPDATE")

    return f"Registro actualizado correctamente. Total de afectados: {cantidad_afectados}"
# =========================================================
# 5D - VALIDAR ACTUALIZACIONES
# =========================================================

def actualizar_registro_validado(
    dataset: str,
    identificador_columna: str,
    identificador_valor: str,
    columna_actualizar: str,
    nuevo_valor: str
):
    """
    Actualiza UN campo de un registro validando previamente
    que el cambio no genere inconsistencias.

    Si la validación falla:
    - NO modifica el registro
    - retorna los errores encontrados
    """

    ruta_origen, separador = obtener_ruta_y_separador(dataset)

    if ruta_origen is None:
        return False, "Dataset no reconocido."

    columnas = columnas_dataset(dataset)

    if isinstance(columnas, str):
        return False, columnas

    if columna_actualizar not in columnas:
        return False, f"La columna '{columna_actualizar}' no existe."

    carpeta_destino = (
        Path(__file__).parent.parent.parent
        / "processed_datasets"
        / dataset
    )

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    ruta_destino = (
        carpeta_destino / f"{dataset}_processed.csv"
    )

    registros_actualizados = []
    registro_encontrado = False

    with open(ruta_origen, "r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(
            archivo,
            delimiter=separador
        )

        for registro in lector_csv:

            coincide = (
                registro.get(identificador_columna, "").strip()
                == str(identificador_valor).strip()
            )

            if coincide:

                copia_registro = registro.copy()

                copia_registro[columna_actualizar] = str(nuevo_valor)

                es_valido, errores = validar_registro(
                    dataset,
                    copia_registro
                )

                if not es_valido:
                    return False, errores

                registros_actualizados.append(copia_registro)

                registro_encontrado = True

            else:
                registros_actualizados.append(registro)

    if not registro_encontrado:
        return False, (
            f"No existe un registro con "
            f"{identificador_columna} = "
            f"'{identificador_valor}'."
        )

    with open(
        ruta_destino,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo_salida:

        escritor = csv.DictWriter(
            archivo_salida,
            fieldnames=columnas,
            delimiter=separador
        )

        escritor.writeheader()
        escritor.writerows(registros_actualizados)

    return (
        True,
        f"Registro actualizado correctamente en "
        f"'{ruta_destino.name}'."
    )


def actualizar_multiples_campos_validado(
    dataset: str,
    identificador_columna: str,
    identificador_valor: str,
    cambios: dict
):
    """
    Actualiza múltiples campos de un registro validando
    previamente que los nuevos valores sean correctos.

    Si la validación falla:
    - NO se aplica ningún cambio
    - retorna la lista de errores
    """

    ruta_origen, separador = obtener_ruta_y_separador(dataset)

    if ruta_origen is None:
        return False, "Dataset no reconocido."

    columnas = columnas_dataset(dataset)

    if isinstance(columnas, str):
        return False, columnas

    for columna in cambios:
        if columna not in columnas:
            return (
                False,
                f"La columna '{columna}' no existe."
            )

    carpeta_destino = (
        Path(__file__).parent.parent.parent
        / "processed_datasets"
        / dataset
    )

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    ruta_destino = (
        carpeta_destino / f"{dataset}_processed.csv"
    )

    registros_actualizados = []
    registro_encontrado = False

    with open(ruta_origen, "r", encoding="utf-8") as archivo:

        lector_csv = csv.DictReader(
            archivo,
            delimiter=separador
        )

        for registro in lector_csv:

            coincide = (
                registro.get(identificador_columna, "").strip()
                == str(identificador_valor).strip()
            )

            if coincide:

                copia_registro = registro.copy()

                for columna, nuevo_valor in cambios.items():
                    copia_registro[columna] = str(nuevo_valor)

                es_valido, errores = validar_registro(
                    dataset,
                    copia_registro
                )

                if not es_valido:
                    return False, errores

                registros_actualizados.append(copia_registro)

                registro_encontrado = True

            else:
                registros_actualizados.append(registro)

    if not registro_encontrado:
        return (
            False,
            f"No existe un registro con "
            f"{identificador_columna} = "
            f"'{identificador_valor}'."
        )

    with open(
        ruta_destino,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo_salida:

        escritor = csv.DictWriter(
            archivo_salida,
            fieldnames=columnas,
            delimiter=separador
        )

        escritor.writeheader()
        escritor.writerows(registros_actualizados)

    
    mensaje = f"Punto 7.D: Actualización múltiple de campos en {dataset}"
    registrar_operacion_en_log(mensaje, "INFO")

    return (
        True,
        f"Registro actualizado correctamente en "
        f"'{ruta_destino.name}'."
    )