from pathlib import Path
import csv
from typing import Optional, Union

from common.dataset_utils import obtener_ruta_y_separador

from core.ejercicio2_lectura_dataset import (
    columnas_dataset,
    contar_registros
)

from core.ejercicio7_registro_de_operaciones import (
    registrar_operacion_en_log
)

#------4a------

# La estructura que representa un registro es un diccionario,
# donde cada columna es una clave y su dato es el valor correspondiente.


#------4b------

def generar_registro_vacio(
    columnas: list[str]
) -> dict[str, None]:
    """
    Genera un registro vacío con todos los valores
    inicializados en None.

    Recibe la lista de columnas del dataset.
    No incluye el campo 'id'.

    Devuelve:
    diccionario {nombre_columna: None}
    """

    registro = {}

    for nombre_columna in columnas:

        if nombre_columna != "id":

            registro[nombre_columna] = None

    return registro


#------4c------
def validar_registro(
    dataset: str,
    registro: dict
) -> tuple[bool, list[str]]:
    """
    Valida un registro antes de insertarlo.
    Reutiliza las funciones base de validación del ejercicio 3.
    Implementa el punto 7.F: registra errores en el log.

    Devuelve:
    (es_valido, lista_de_errores)
    """

    # Importamos las funciones base y la de registro
    from core.ejercicio3_validaciones import (
        validar_par_coordenadas,
        validar_fecha_unica,
        validar_country_code_unico,
        validar_incertidumbre_unica
    )
   

    errores = []

    # --- 1. Validar coordenadas (3a y 3b) ---
    valor_latitud = registro.get("decimalLatitude")
    valor_longitud = registro.get("decimalLongitude")

    coordenadas_validas, errores_coordenadas = validar_par_coordenadas(
        valor_latitud, 
        valor_longitud
    )
    if not coordenadas_validas:
        errores.extend(errores_coordenadas)

    # --- 2. Validar fechas (3c) ---
    columnas_fecha = {
        "IADIZA": [
            'modified', 'eventDate', 'verbatimEventDate', 'dateIdentified',
            'georeferencedDate', 'lastInterpreted', 'lastParsed', 'lastCrawled'
        ],
        "Inaturalist": [
            'eventDate', 'modified', 'verbatimEventDate', 'dateIdentified'
        ],
        "XenoCanto": [
            'eventDate', 'verbatimEventDate'
        ]
    }

    for columna_fecha in columnas_fecha.get(dataset, []):
        valor_fecha = registro.get(columna_fecha)
        if valor_fecha is None or str(valor_fecha).strip() == "":
            continue

        fecha_valida, mensaje_error = validar_fecha_unica(valor_fecha)
        if not fecha_valida:
            errores.append(f"Columna '{columna_fecha}': {mensaje_error}")

    # --- 3. Validar countryCode (3e) ---
    valor_country_code = registro.get("countryCode")
    country_code_valido, mensaje_error = validar_country_code_unico(valor_country_code)
    if not country_code_valido and mensaje_error:
        errores.append(mensaje_error)

    # --- 4. Validar incertidumbre (3f) ---
    valor_incertidumbre = registro.get("coordinateUncertaintyInMeters")
    incertidumbre_valida, mensaje_error = validar_incertidumbre_unica(valor_incertidumbre)
    if not incertidumbre_valida and mensaje_error:
        errores.append(mensaje_error)

    # --- Punto 7f
    registro_valido = len(errores) == 0

    if not registro_valido:
        # Por cada error encontrado, generamos una entrada en el log con nivel ERROR
        for error in errores:
            # Formato: fecha | dataset | tipo | cantidad | 
            # Usamos "VALIDATION" como tipo de operación para ser específicos
            mensaje_error_log = f"Punto 7.F: Falló validación en {dataset}. Motivo: {error}"
            registrar_operacion_en_log(mensaje_error_log, "ERROR")[cite: 1]

    return registro_valido, errores


#------4d------

def registro_a_fila(
    dataset: str,
    registro: dict
) -> Union[list[str], str]:
    """
    Convierte un registro (diccionario del 4A)
    en una lista lista para agregar al CSV,
    deduciendo y agregando el ID correspondiente
    a cada dataset:

    - IADIZA:
      occurrenceID = IADIZA:COI:{catalogNumber}

    - Inaturalist:
      id autoincremental

    - XenoCanto:
      id = {numero}@XC

    Devuelve:
    lista de valores en el orden de columnas del CSV.
    """

    columnas = columnas_dataset(dataset)

    # si devolvió un string = hubo error
    if isinstance(columnas, str):

        return f"Dataset '{dataset}' no reconocido."

    # Generamos el ID según cada dataset

    if dataset == "IADIZA":

        # Su occurrenceID se forma como
        # IADIZA:COI:catalogNumber

        catalogo = registro.get('catalogNumber', '')

        registro['occurrenceID'] = (
            f"IADIZA:COI:{catalogo}"
        )

        # gbifID lo asigna GBIF,
        # entonces lo dejamos vacío

        registro['gbifID'] = ''

    elif dataset == "Inaturalist":

        # El id es autoincremental,
        # necesitamos saber cuántos registros hay

        total_registros = contar_registros(dataset)

        registro['id'] = str(total_registros + 1)

    elif dataset == "XenoCanto":

        # El id (XXXXXX@XC)
        # se forma a partir del catalogNumber

        catalogo = registro.get('catalogNumber', '')

        # catalogNumber es XC999540,
        # nos quedamos solo con el número

        numero_catalogo = catalogo.replace('XC', '')

        registro['id'] = f"{numero_catalogo}@XC"

    # Convertimos el diccionario a lista
    # en el orden de columnas del CSV

    fila = []

    for columna in columnas:

        valor = registro.get(columna)

        if valor is None:

            fila.append('')

        else:

            fila.append(str(valor))

    return fila


# --- FUNCIÓN AUXILIAR para pedir los datos (nuevas filas) ---

def crear_registro_interactivo(
    dataset: str
) -> tuple[Optional[list], Optional[list[str]]]:
    """
    Pide por teclado los datos esenciales de un registro,
    los valida y retorna la fila lista para insertar.

    Campos solicitados:
    catalogNumber,
    decimalLatitude,
    decimalLongitude,
    eventDate,
    countryCode,
    coordinateUncertaintyInMeters,
    scientificName.

    Devuelve:
    (fila_lista, None) si es válido,
    o (None, lista_errores) si falla.
    """

    columnas = columnas_dataset(dataset)

    nuevo_registro = generar_registro_vacio(columnas)

    campos_clave = [
        'catalogNumber',
        'decimalLatitude',
        'decimalLongitude',
        'eventDate',
        'countryCode',
        'coordinateUncertaintyInMeters',
        'scientificName'
    ]

    for campo in campos_clave:

        if campo in columnas:

            valor_ingresado = input(
                f"Ingrese {campo} "
                f"(Enter para dejar vacío): "
            )

            if valor_ingresado.strip() != "":

                nuevo_registro[campo] = (
                    valor_ingresado.strip()
                )

    registro_valido, errores = validar_registro(
        dataset,
        nuevo_registro
    )

    if registro_valido:

        return (
            registro_a_fila(dataset, nuevo_registro),
            None
        )

    else:

        return None, errores


#------4f (Versión Refactorizada) ------
def insertar_registro_teclado(dataset: str) -> str:
    """
    Pide datos por teclado, los valida y los inserta en processed_datasets.
    Implementa el punto 7.C (éxito) y el punto 7.F (error).
    """

    ruta_origen, separador = obtener_ruta_y_separador(dataset)

    if not ruta_origen:
        # ----7f: Registro de error si el dataset no existe
        mensaje_error = f"Punto 7.F: Intento de INSERT fallido. Dataset '{dataset}' no reconocido."
        registrar_operacion_en_log(mensaje_error, "ERROR")
        return "Dataset no reconocido."

    # Definimos rutas
    carpeta_destino = (
        Path(__file__).parent.parent.parent 
        / 'processed_datasets' 
        / dataset
    )

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    ruta_destino = (
        carpeta_destino 
        / f"{dataset}_processed.csv"
    )

    print(f"\n--- Ingresando UN registro para {dataset} ---")

    # Usamos el motor reutilizable
    nueva_fila, errores = crear_registro_interactivo(dataset)

    # --- 7f---
    if not nueva_fila:
        # Si no hay fila es porque falló la validación o el ingreso
        mensaje_fallo = f"Punto 7.F: Error en INSERT para {dataset}. Detalle: {errores}"
        registrar_operacion_en_log(mensaje_fallo, "ERROR")
        return f"Error: {errores}"
    #--------seguimos con el 4
    # Guardamos (Escribimos una sola vez)
    if ruta_destino.exists():
        with open(ruta_destino, 'a', encoding='utf-8', newline='') as archivo_destino:
            escritor_csv = csv.writer(archivo_destino, delimiter=separador)
            escritor_csv.writerow(nueva_fila)
    else:
        with open(ruta_origen, 'r', encoding='utf-8') as archivo_origen, \
             open(ruta_destino, 'w', encoding='utf-8', newline='') as archivo_destino:
            
            escritor_csv = csv.writer(archivo_destino, delimiter=separador)
            
            for fila in csv.reader(archivo_origen, delimiter=separador):
                escritor_csv.writerow(fila)
            
            escritor_csv.writerow(nueva_fila)

    # --- 7c---
    
    mensaje_exito = f"Punto 7.C: Inserción manual de 1 registro en {dataset}"
    registrar_operacion_en_log(mensaje_exito, "INSERT")

    return "Registro único guardado."

#------4g (Extendiendo la lógica del 4f) ------
def insertar_multiples_registros(dataset: str) -> str:
    """
    Extiende el 4.F para insertar múltiples registros en lote.
    Implementa el punto 7.C (éxito masivo) y el punto 7.F (errores individuales).
    """

    ruta_origen, separador = obtener_ruta_y_separador(dataset)

    if not ruta_origen:
        # ------7f Registro en el log
        registrar_operacion_en_log(f"Punto 7.F: INSERT masivo fallido. Dataset '{dataset}' inválido.", "ERROR")
        return "Dataset no reconocido."

    carpeta_destino = (
        Path(__file__).parent.parent.parent 
        / 'processed_datasets' 
        / dataset
    )

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    ruta_destino = (
        carpeta_destino 
        / f"{dataset}_processed.csv"
    )

    nuevas_filas = []

    # Bucle donde registramos las fallas en el log (7f)
    while True:
        fila, errores = crear_registro_interactivo(dataset)

        if fila:
            nuevas_filas.append(fila)
            print("Registro encolado.")
        else:
            # ---7f
            # Cada vez que un registro del lote falla, se loguea el error
            mensaje_error = f"Punto 7.F: Error en registro de lote para {dataset}. Detalle: {errores}"
            registrar_operacion_en_log(mensaje_error, "ERROR")
            print(f"Error: {errores}")

        continuar = input("\n¿Ingresar otro? (s/n): ").lower()
        if continuar != 's':
            break

    if not nuevas_filas:
        # PUNTO 7.F: Si se sale del bucle sin ningún registro válido[cite: 1]
        registrar_operacion_en_log(f"Punto 7.F: Operación masiva en {dataset} cancelada por falta de datos válidos.", "ERROR")
        return "Operación cancelada."

    # Guardamos todas las filas de una sola vez
    if ruta_destino.exists():
        with open(ruta_destino, 'a', encoding='utf-8', newline='') as archivo_destino:
            escritor_csv = csv.writer(archivo_destino, delimiter=separador)
            # Note el plural: writerows
            escritor_csv.writerows(nuevas_filas)
    else:
        with open(ruta_origen, 'r', encoding='utf-8') as archivo_origen, \
             open(ruta_destino, 'w', encoding='utf-8', newline='') as archivo_destino:
            
            escritor_csv = csv.writer(archivo_destino, delimiter=separador)
            
            for fila in csv.reader(archivo_origen, delimiter=separador):
                escritor_csv.writerow(fila)
            
            escritor_csv.writerows(nuevas_filas)

    # --- 7c---
    cantidad_registros = len(nuevas_filas)
    mensaje = f"Punto 7.C: Inserción masiva de {cantidad_registros} registros en {dataset}"
    
    # Se cambia "INFO" por "INSERT" para cque quede el mismo tipo de operación
    registrar_operacion_en_log(mensaje, "INSERT")

    return f"{len(nuevas_filas)} registros guardados."