from pathlib import Path
import csv
from datetime import datetime
from typing import Optional
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas, contar_registros
from common.constants import country_codes_validos


# FUNCIONES BASE DE VALIDACIÓN

def validar_latitud(valor: Optional[str]) -> tuple[bool, str]:
    """
    Valida una latitud individual.
    Recibe: un string o número.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """
    if valor is None or str(valor).strip() == "":
        return False, "Latitud vacía"
    
    texto = str(valor).strip()

    # Verifico si es número (permite punto decimal y signo menos)
    es_numero = texto.replace('.', '', 1).replace('-', '', 1).isdigit()
    
    if not es_numero:
        return False, f"'{texto}' no es un número válido"
    
    latitud = float(texto)

    if -90 <= latitud <= 90:
        return True, ""
    else:
        return False, f"Latitud {latitud} fuera de rango [-90, 90]"


def validar_longitud(valor: Optional[str]) -> tuple[bool, str]:
    """
    Valida una longitud individual.
    Recibe: un string o número.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """
    if valor is None or str(valor).strip() == "":
        return False, "Longitud vacía"
    
    texto = str(valor).strip()

    es_numero = texto.replace('.', '', 1).replace('-', '', 1).isdigit()
    
    if not es_numero:
        return False, f"'{texto}' no es un número válido"
    
    longitud = float(texto)

    if -180 <= longitud <= 180:
        return True, ""
    else:
        return False, f"Longitud {longitud} fuera de rango [-180, 180]"


def validar_par_coordenadas(latitud_valor: Optional[str], longitud_valor: Optional[str]) -> tuple[bool, list[str]]:
    """
    Valida un par de coordenadas juntas.
    Devuelve: (bool, lista_de_errores)
    """

    latitud_vacia = latitud_valor is None or str(latitud_valor).strip() == ""
    longitud_vacia = longitud_valor is None or str(longitud_valor).strip() == ""

    # si ambas estan vacías es válido
    if latitud_vacia and longitud_vacia:
        return True, []

    errores = []

    # Validar solo si hay valor
    if not latitud_vacia:
        latitud_valida, error_latitud = validar_latitud(latitud_valor)

        if not latitud_valida:
            errores.append(error_latitud)

    if not longitud_vacia:
        longitud_valida, error_longitud = validar_longitud(longitud_valor)

        if not longitud_valida:
            errores.append(error_longitud)

    # Caso inconsistente donde hay una vacía y la otra no
    if not latitud_vacia and longitud_vacia:
        errores.append("Tiene latitud pero falta longitud")

    elif latitud_vacia and not longitud_vacia:
        errores.append("Tiene longitud pero falta latitud")

    return len(errores) == 0, errores


def validar_fecha_unica(fecha_str: Optional[str], formatos: Optional[list[str]] = None) -> tuple[bool, str]:
    """
    Valida una fecha en una lista de formatos.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """

    if fecha_str is None or str(fecha_str).strip() == "":
        return True, ""  # Vacío se considera válido

    if formatos is None:
        formatos = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m",
            "%Y",
        ]

    texto = str(fecha_str).strip()

    anio_actual = datetime.now().year

    for formato in formatos:
        try:
            fecha = datetime.strptime(texto, formato)

            if fecha.year > anio_actual:
                return False, f"Fecha {texto} posterior al año actual"

            return True, ""

        except ValueError:
            continue

    return False, f"Formato de fecha inválido: '{texto}'"


def validar_country_code_unico(codigo: Optional[str]) -> tuple[bool, str]:
    """
    Valida un countryCode individual contra el estándar ISO 3166-1 alpha-2.
    Devuelve: (bool, str) -> (es_valido, mensaje_error)
    """

    if codigo is None or str(codigo).strip() == "":
        return True, ""

    codigo_limpio = str(codigo).strip().upper()

    if codigo_limpio in country_codes_validos:
        return True, ""

    return False, f"countryCode inválido: '{codigo_limpio}'"


def validar_incertidumbre_unica(valor: Optional[str]) -> tuple[bool, str]:
    """
    Valida coordinateUncertaintyInMeters individual.
    El valor debe ser numérico, no negativo y no mayor a 100 metros.
    Devuelve: (bool, str) -> (es_valido, mensaje_error)
    """

    if valor is None or str(valor).strip() == "":
        return True, ""  # Vacío se considera válido
    
    texto = str(valor).strip()
    
    try:
        numero = float(texto)

        if numero < 0:
            return False, f"Incertidumbre negativa: {numero}"

        elif numero > 100:
            return False, f"Incertidumbre > 100m: {numero}"

        return True, ""

    except ValueError:
        return False, f"Incertidumbre no es número: '{texto}'"


def validar_coordenadas_rango(dataset: str) -> tuple[int, list[str]]:
    """
    Detecta registros con coordenadas inválidas (fuera de rango o no numéricas).
    Reutiliza validar_par_coordenadas()
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    # Agarro los indices de las latitudes y longitudes gracias a las funciones del punto 2
    indice_latitud = indices_columnas.get('decimalLatitude')
    indice_longitud = indices_columnas.get('decimalLongitude')

    if indice_latitud is None or indice_longitud is None:
        return 0, [f"No se encontraron columnas de coordenadas en {dataset}"]

    cantidad_invalidos = 0

    registros_invalidos = []  # Aca es donde voy a guardar los registros incorrectos

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for numero_fila, fila in enumerate(lector_csv, start=2):

            latitud_valor = fila[indice_latitud] if indice_latitud < len(fila) else ""

            longitud_valor = fila[indice_longitud] if indice_longitud < len(fila) else ""

            es_valido, errores = validar_par_coordenadas(
                latitud_valor,
                longitud_valor
            )

            if not es_valido:
                cantidad_invalidos += 1

                registros_invalidos.append(
                    f"Fila {numero_fila}: {' | '.join(errores)}"
                )

    return cantidad_invalidos, registros_invalidos


#----3b----

def validar_coordenadas_incompletas(dataset: str) -> tuple[int, list[str]]:
    """
    Detecta registros con coordenadas incompletas:
    - Tiene latitud pero no longitud.
    - Tiene longitud pero no latitud.
    - No tiene ninguna de las dos.
    Devuelve: (cantidad, lista_de_errores)
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    indice_latitud = indices_columnas.get('decimalLatitude')

    indice_longitud = indices_columnas.get('decimalLongitude')

    if indice_latitud is None or indice_longitud is None:
        return 0, [f"No se encontraron columnas de coordenadas en {dataset}"]

    registros_incompletos = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        # Hasta aca es lo mismo que el 3a, misma metodología

        # Aca recorremos los registros y vamos chequeando
        # cuales tienen alguno de los 2 campos vacios
        for numero_fila, fila in enumerate(lector_csv, start=2):

            texto_latitud = fila[indice_latitud].strip()

            texto_longitud = fila[indice_longitud].strip()

            # Tiene latitud pero no longitud
            if texto_latitud != "" and texto_longitud == "":

                registros_incompletos.append(
                    f"Fila {numero_fila}: Tiene latitud pero falta la longitud."
                )

            # Tiene longitud pero no latitud
            elif texto_longitud != "" and texto_latitud == "":

                registros_incompletos.append(
                    f"Fila {numero_fila}: Tiene longitud pero falta la latitud."
                )

            # No tiene ninguna
            elif texto_longitud == "" and texto_latitud == "":

                registros_incompletos.append(
                    f"Fila {numero_fila}: Faltan ambos campos."
                )

    return len(registros_incompletos), registros_incompletos


#------ 3c ------

def verificar_fechas(dataset: str) -> tuple[int, list[str]]:
    """
    Revisa que las fechas de los datasets sean válidas.
    Se consideran válidas las fechas que tengan
    el formato adecuado y no sean mayores al año actual.
    reutiliza validar_fecha_unica()
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    # Creo un diccionario para saber qué columnas revisar
    # en cada dataset
    columnas_por_dataset = {
        "IADIZA": [
            'modified',
            'eventDate',
            'verbatimEventDate',
            'dateIdentified',
            'georeferencedDate',
            'lastInterpreted',
            'lastParsed',
            'lastCrawled'
        ],

        "Inaturalist": [
            'eventDate',
            'modified',
            'verbatimEventDate',
            'dateIdentified'
        ],

        "XenoCanto": [
            'eventDate',
            'verbatimEventDate'
        ]
    }

    # Revisa si el nombre del dataset está en el diccionario
    columnas_fecha = columnas_por_dataset.get(dataset, [])

    if not columnas_fecha:
        return 0, [f"No se reconocen columnas de fecha para '{dataset}'"]

    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for numero_fila, fila in enumerate(lector_csv, start=2):

            for columna in columnas_fecha:

                indice_columna = indices_columnas.get(columna)

                if indice_columna is None or indice_columna >= len(fila):
                    continue

                fecha_valor = fila[indice_columna]

                es_valida, mensaje_error = validar_fecha_unica(fecha_valor)

                if not es_valida:

                    errores.append(
                        f"Fila {numero_fila} columna '{columna}': {mensaje_error}"
                    )

    return len(errores), errores


#-------3d ------

def detectar_duplicados(dataset: str) -> tuple[int, list[str]]:
    """
    Detecta registros duplicados usando el campo occurrenceID o id.
    Devuelve: (cantidad_duplicados, lista_de_ids_repetidos)
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    # Agarramos la columna id
    indice_identificador = indices_columnas.get('occurrenceID')

    if indice_identificador is None:
        indice_identificador = indices_columnas.get('id')

    # 2 listas. Una con todos los ids
    # y otra con los que se repiten
    todos_los_identificadores = []

    identificadores_duplicados = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for fila in lector_csv:

            identificador_actual = fila[indice_identificador].strip()

            # Primero revisamos que el id no este vacio
            if identificador_actual != "":

                # Si ya existe, es duplicado
                if identificador_actual in todos_los_identificadores:

                    if identificador_actual not in identificadores_duplicados:

                        identificadores_duplicados.append(
                            identificador_actual
                        )

                else:
                    # Primera vez que aparece
                    todos_los_identificadores.append(
                        identificador_actual
                    )

    return len(identificadores_duplicados), identificadores_duplicados


#----------3e----------

def detectar_invalidos_country_code(dataset: str) -> tuple[int, list[str]]:
    """
    Detecta countryCodes inválidos.
    Utiliza validar_country_code_unico()
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    indice_country_code = indices_columnas.get('countryCode')

    if indice_country_code is None:
        return 0, ['No existe el campo countryCode']

    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for numero_fila, fila in enumerate(lector_csv, start=2):

            if indice_country_code >= len(fila):
                continue

            valor_country_code = fila[indice_country_code]

            es_valido, mensaje_error = validar_country_code_unico(
                valor_country_code
            )

            if not es_valido:

                errores.append(
                    f"Fila {numero_fila}: {mensaje_error}"
                )

    return len(errores), errores


#----------3f----------

def validar_incertidumbre(dataset: str) -> tuple[int, list[str]]:
    """
    Detecta registros donde la incertidumbre
    (coordinateUncertaintyInMeters):
    - No sea numérica.
    - Sea negativa.
    - Sea mayor a 100 metros.
    reutiliza validar_incertidumbre_unica()
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    indice_incertidumbre = indices_columnas.get(
        'coordinateUncertaintyInMeters'
    )

    if indice_incertidumbre is None:

        return 0, [
            f"No existe 'coordinateUncertaintyInMeters' en {dataset}"
        ]

    # agrego una lista con los errores
    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        # el primer dato real está en la fila 2(la 1 eran los encabezados). Usar start=2 hace que los reportes de error coincidan
        for numero_fila, fila in enumerate(lector_csv, start=2):

            if indice_incertidumbre >= len(fila):
                continue

            valor_incertidumbre = fila[indice_incertidumbre]

            es_valido, mensaje_error = validar_incertidumbre_unica(
                valor_incertidumbre
            )

            if not es_valido:

                errores.append(
                    f"Fila {numero_fila}: {mensaje_error}"
                )

    return len(errores), errores

#----------3g----------

def registros_taxonomia_incompleta(dataset: str) -> int:
    """
    Función auxiliar para el 3G. Cuenta cuántos registros tienen
    campos taxonómicos básicos vacíos
    (kingdom, phylum, class, order, family, genus, species).

    Devuelve:
    cantidad de registros con taxonomía incompleta.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return 0

    # Defino qué columnas consideramos información taxonómica
    columnas_taxonomicas = [
        'kingdom',
        'phylum',
        'class',
        'order',
        'family',
        'genus',
        'species'
    ]

    # Busco los índices de esas columnas
    indices_taxonomicos = [
        indices_columnas.get(columna)
        for columna in columnas_taxonomicas
        if indices_columnas.get(columna) is not None
    ]

    cantidad_incompletos = 0

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for fila in lector_csv:

            # Reviso si alguna columna taxonómica está vacía
            registro_incompleto = False

            for indice_columna in indices_taxonomicos:

                if (
                    indice_columna < len(fila)
                    and fila[indice_columna].strip() == ""
                ):

                    registro_incompleto = True
                    break

            if registro_incompleto:
                cantidad_incompletos += 1

    return cantidad_incompletos


def generar_resumen_calidad(
    dataset: str
) -> tuple[Optional[dict], str]:
    """
    Punto 3.G:
    Genera un resumen de calidad agrupando todas las métricas.

    Retorna:
    un diccionario con las métricas
    y un texto formateado del reporte.
    """

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return None, f"Error: {indices_columnas}"

    # Recopilo todas las métricas llamando funciones
    total_registros = contar_registros(dataset)

    cantidad_coordenadas_invalidas, _ = (
        validar_coordenadas_rango(dataset)
    )

    cantidad_fechas_invalidas, _ = verificar_fechas(dataset)

    cantidad_duplicados, _ = detectar_duplicados(dataset)

    cantidad_taxonomia_incompleta = (
        registros_taxonomia_incompleta(dataset)
    )

    # Armo el diccionario que pide el enunciado
    resumen = {
        "dataset": dataset,
        "total_registros": total_registros,
        "coordenadas_invalidas": cantidad_coordenadas_invalidas,
        "fechas_invalidas": cantidad_fechas_invalidas,
        "duplicados": cantidad_duplicados,
        "taxonomia_incompleta": cantidad_taxonomia_incompleta
    }

    # Armamos el reporte en texto
    reporte_texto = (
        f"=== REPORTE DE CALIDAD: {dataset.upper()} ===\n"
    )

    reporte_texto += (
        f"Total de registros: {total_registros}\n"
    )

    reporte_texto += (
        f" - Coordenadas inválidas: "
        f"{cantidad_coordenadas_invalidas}\n"
    )

    reporte_texto += (
        f" - Fechas inválidas: "
        f"{cantidad_fechas_invalidas}\n"
    )

    reporte_texto += (
        f" - Registros duplicados: "
        f"{cantidad_duplicados}\n"
    )

    reporte_texto += (
        f" - Taxonomía incompleta: "
        f"{cantidad_taxonomia_incompleta}\n"
    )

    reporte_texto += (
        "========================================\n"
    )

    return resumen, reporte_texto


#----------3h----------

# Constantes de cotas geográficas para América del Sur

LATITUD_MAXIMA_SUDAMERICA = 15.0
LATITUD_MINIMA_SUDAMERICA = -60.0

LONGITUD_MAXIMA_SUDAMERICA = -30.0
LONGITUD_MINIMA_SUDAMERICA = -90.0


def validar_coordenadas_sudamerica(
    dataset: str
) -> tuple[int, list[str]]:
    """
    Verifica que las coordenadas caigan dentro
    del territorio de América del Sur.

    Utiliza las constantes:
    LATITUD_MINIMA_SUDAMERICA,
    LATITUD_MAXIMA_SUDAMERICA,
    LONGITUD_MINIMA_SUDAMERICA,
    LONGITUD_MAXIMA_SUDAMERICA.

    Retorna la cantidad y el detalle
    de los registros que caen fuera.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return 0, [indices_columnas]

    indice_latitud = indices_columnas.get('decimalLatitude')

    indice_longitud = indices_columnas.get('decimalLongitude')

    if indice_latitud is None or indice_longitud is None:

        return 0, [
            f"Faltan columnas de coordenadas en {dataset}."
        ]

    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for numero_fila, fila in enumerate(lector_csv, start=2):

            if (
                indice_latitud >= len(fila)
                or indice_longitud >= len(fila)
            ):
                continue

            texto_latitud = fila[indice_latitud].strip()

            texto_longitud = fila[indice_longitud].strip()

            if texto_latitud == "" or texto_longitud == "":
                continue

            try:

                latitud = float(texto_latitud)

                longitud = float(texto_longitud)

                # Validamos si están fuera de Sudamérica
                if not (
                    LATITUD_MINIMA_SUDAMERICA
                    <= latitud
                    <= LATITUD_MAXIMA_SUDAMERICA
                ) or not (
                    LONGITUD_MINIMA_SUDAMERICA
                    <= longitud
                    <= LONGITUD_MAXIMA_SUDAMERICA
                ):

                    errores.append(
                        f"Fila {numero_fila}: "
                        f"Fuera de Sudamérica "
                        f"(Lat: {latitud}, Lon: {longitud})"
                    )

            except ValueError:
                # Si no es un número,
                # lo ignoro porque ya se detecta en 3.A
                pass

    return len(errores), errores


#----------3i----------

def auditar_coordenada_generica(
    dataset: str,
    nombre_columna: str,
    minimo_global: float,
    maximo_global: float,
    minimo_sudamerica: float,
    maximo_sudamerica: float
) -> tuple[int, list[str]]:
    """
    Función base reutilizable para auditar
    cualquier columna de coordenadas.

    Valida globalmente (rango mundial)
    y regionalmente (América del Sur).

    Devuelve:
    (cantidad_errores, lista_de_errores)
    """

    ruta, separador = obtener_ruta_y_separador(dataset)

    indices_columnas = obtener_indices_columnas(dataset)

    if isinstance(indices_columnas, str):
        return 0, [indices_columnas]

    indice_columna = indices_columnas.get(nombre_columna)

    if indice_columna is None:

        return 0, [
            f"No existe '{nombre_columna}' en {dataset}"
        ]

    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:

        lector_csv = csv.reader(archivo, delimiter=separador)

        next(lector_csv)

        for numero_fila, fila in enumerate(lector_csv, start=2):

            if indice_columna >= len(fila):
                continue

            valor_texto = fila[indice_columna].strip()

            if valor_texto == "":
                continue

            try:

                valor_numerico = float(valor_texto)

                # Validación global
                if not (
                    minimo_global
                    <= valor_numerico
                    <= maximo_global
                ):

                    errores.append(
                        f"Fila {numero_fila}: "
                        f"Inválida globalmente "
                        f"({valor_numerico})"
                    )

                # Validación Sudamérica
                elif not (
                    minimo_sudamerica
                    <= valor_numerico
                    <= maximo_sudamerica
                ):

                    errores.append(
                        f"Fila {numero_fila}: "
                        f"Fuera de Sudamérica "
                        f"({valor_numerico})"
                    )

            except ValueError:

                # Validación de tipo
                errores.append(
                    f"Fila {numero_fila}: "
                    f"Formato erróneo "
                    f"('{valor_texto}')"
                )

    return len(errores), errores


def auditar_columna_latitud(
    dataset: str
) -> tuple[int, list[str]]:
    """
    Agrupa y ejecuta todas las validaciones
    para el campo decimalLatitude.

    Valida rango global [-90, 90]
    y rango para América del Sur.

    Devuelve:
    (cantidad_errores, lista_de_errores)
    """

    return auditar_coordenada_generica(
        dataset,
        'decimalLatitude',
        -90.0,
        90.0,
        LATITUD_MINIMA_SUDAMERICA,
        LATITUD_MAXIMA_SUDAMERICA
    )


def auditar_columna_longitud(
    dataset: str
) -> tuple[int, list[str]]:
    """
    Agrupa y ejecuta todas las validaciones
    para el campo decimalLongitude.

    Valida rango global [-180, 180]
    y rango para América del Sur.

    Devuelve:
    (cantidad_errores, lista_de_errores)
    """

    return auditar_coordenada_generica(
        dataset,
        'decimalLongitude',
        -180.0,
        180.0,
        LONGITUD_MINIMA_SUDAMERICA,
        LONGITUD_MAXIMA_SUDAMERICA
    )