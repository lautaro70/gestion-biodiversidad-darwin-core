from pathlib import Path
import csv
from datetime import datetime
from common.dataset_utils import obtener_ruta_y_separador
from core.ejercicio2_lectura_dataset import obtener_indices_columnas, contar_registros
from iso3166 import countries

# FUNCIONES BASE DE VALIDACIÓN

def validar_latitud(valor):
    """
    Valida una latitud individual.
    Recibe: un string o número.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """
    if valor is None or str(valor).strip() == "":
        return False, "Latitud vacía"
    
    txt = str(valor).strip()
    # Verifico si es número (permite punto decimal y signo menos)
    es_numero = txt.replace('.', '', 1).replace('-', '', 1).isdigit()
    
    if not es_numero:
        return False, f"'{txt}' no es un número válido"
    
    lat = float(txt)
    if -90 <= lat <= 90:
        return True, ""
    else:
        return False, f"Latitud {lat} fuera de rango [-90, 90]"


def validar_longitud(valor):
    """
    Valida una longitud individual.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """
    if valor is None or str(valor).strip() == "":
        return False, "Longitud vacía"
    
    txt = str(valor).strip()
    es_numero = txt.replace('.', '', 1).replace('-', '', 1).isdigit()
    
    if not es_numero:
        return False, f"'{txt}' no es un número válido"
    
    lon = float(txt)
    if -180 <= lon <= 180:
        return True, ""
    else:
        return False, f"Longitud {lon} fuera de rango [-180, 180]"


def validar_par_coordenadas(lat_valor, lon_valor):
    """
    Valida un par de coordenadas juntas.
    Devuelve: (bool, lista_de_errores)
    """
    errores = []
    
    valida_lat, error_lat = validar_latitud(lat_valor)
    if not valida_lat:
        errores.append(error_lat)
    
    valida_lon, error_lon = validar_longitud(lon_valor)
    if not valida_lon:
        errores.append(error_lon)
    
    # Caso especial: una completa y la otra vacía (punto 3B)
    lat_vacia = lat_valor is None or str(lat_valor).strip() == ""
    lon_vacia = lon_valor is None or str(lon_valor).strip() == ""
    
    if (not lat_vacia and lon_vacia):
        errores.append("Tiene latitud pero falta longitud")
    elif (lat_vacia and not lon_vacia):
        errores.append("Tiene longitud pero falta latitud")
    
    return len(errores) == 0, errores


def validar_fecha_unica(fecha_str, formatos=None):
    """
    Valida una fecha en una lista de formatos.
    Devuelve: (bool, str) -> (es_valida, mensaje_error)
    """
    if fecha_str is None or str(fecha_str).strip() == "":
        return True, ""  # Vacío se considera válido (solo nos interesan los inválidos)
    
    if formatos is None:
        from datetime import datetime
        formatos = [
            "%Y-%m-%d",             
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",   
            "%Y-%m-%dT%H:%M:%S%z",  
            "%Y-%m",                 
            "%Y",                    
        ]
    
    txt = str(fecha_str).strip()
    anio_actual = datetime.now().year
    
    for formato in formatos:
        try:
            fecha = datetime.strptime(txt, formato)
            if fecha.year > anio_actual:
                return False, f"Fecha {txt} posterior al año actual"
            return True, ""
        except ValueError:
            continue
    
    return False, f"Formato de fecha inválido: '{txt}'"


def validar_country_code_unico(codigo):
    """
    Valida un countryCode individual.
    Devuelve: (bool, str)
    """
    if codigo is None or str(codigo).strip() == "":
        return True, ""  # Vacío se considera válido (ya lo cubre punto 2)
    
    codigo = str(codigo).strip().upper()
    
    if codigo in {'ZZ', 'XZ'}:
        return True, ""
    
    try:
        from iso3166 import countries
        countries.get(codigo)
        return True, ""
    except KeyError:
        return False, f"countryCode inválido: '{codigo}'"


def validar_incertidumbre_unica(valor):
    """
    Valida coordinateUncertaintyInMeters individual.
    Devuelve: (bool, str)
    """
    if valor is None or str(valor).strip() == "":
        return True, ""  # Vacío se considera válido
    
    txt = str(valor).strip()
    
    try:
        num = float(txt)
        if num < 0:
            return False, f"Incertidumbre negativa: {num}"
        elif num > 100:
            return False, f"Incertidumbre > 100m: {num}"
        return True, ""
    except ValueError:
        return False, f"Incertidumbre no es número: '{txt}'"

#Arranco con el 3a

def validar_coordenadas_rango(dataset):
    """
    Detecta registros con coordenadas inválidas (fuera de rango o no numéricas).
    Reutiliza validar_par_coordenadas()
    """

    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
#Agarro los indices de las latitudes y longitudes gracias a las funciones del punto 2
    idx_lat = indices.get('decimalLatitude')
    idx_lon = indices.get('decimalLongitude')

    if idx_lat is None or idx_lon is None:
        return 0, [f"No se encontraron columnas de coordenadas en {dataset}"]
    
    cantidad_invalidos = 0
    registros_invalidos = [] #Aca es donde voy a guardar los registros incorrectos


    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for nro_fila, fila in enumerate(lector, start=2):
            lat_valor = fila[idx_lat] if idx_lat < len(fila) else ""
            lon_valor = fila[idx_lon] if idx_lon < len(fila) else ""
            
            es_valido, errores = validar_par_coordenadas(lat_valor, lon_valor)
            
            if not es_valido:
                cantidad_invalidos += 1
                registros_invalidos.append(f"Fila {nro_fila}: {' | '.join(errores)}")
    
    return cantidad_invalidos, registros_invalidos


#----3b----

def validar_coordenadas_incompletas(dataset):

    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    idx_lat = indices.get('decimalLatitude')
    idx_lon = indices.get('decimalLongitude')
    
    incompletos = []

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        #Hasta aca es lo mismo que el 3a, misma metodología


        #Aca recorremos los registros  y vamos chequeando cuales tienen alguno de los 2 campos vacios para agregarlos a la lista incompletos
        for nro_fila, fila in enumerate(lector, start=2):
            lat_txt = fila[idx_lat].strip()
            lon_txt = fila[idx_lon].strip()

            if lat_txt != "" and lon_txt == "": #Logicamente aca agregamos los que tienen latitud pero no longitud
                incompletos.append(f"Fila {nro_fila}: Tiene latitud pero falta la longitud.")


            elif lon_txt != "" and lat_txt == "": #Y aca al reves, si longitud pero no latitud
                incompletos.append(f"Fila {nro_fila}: Tiene longitud pero falta la latitud.")

            #No tuvimos en cuenta los casos donde no tiene ninguno de los 2 campos.Deberiamos agregarlo ?

    return len(incompletos), incompletos 


#------ 3c ------
def verificar_fechas(dataset):
    """
    Revisa que las fechas de los datasets sean válidas. 
    Se consideran válidas a las fechas que tengan el formato adecuado y no sean mayores al año actual
    reutiliza validar_fecha_unica()
    """
   
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    #creo un diccionario para saber que columnas revisar en cada dataset
    columnas_por_dataset = {
        "IADIZA": ['modified', 'eventDate', 'verbatimEventDate', 'dateIdentified', 'georeferencedDate', 'lastInterpreted', 'lastParsed', 'lastCrawled'],
        "Inaturalist": ['eventDate', 'modified','verbatimEventDate', 'dateIdentified'],
        "XenoCanto": ['eventDate', 'verbatimEventDate']
    }

    #revisa si el nombre del dataset está en el diccionario, sino devuelve una lista vacia (false)
    columnas_fecha = columnas_por_dataset.get(dataset, [])
    if not columnas_fecha:
        return 0, [f"No se reconocen columnas de fecha para '{dataset}'"]

    errores = []
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)
        
        for nro_fila, fila in enumerate(lector, start=2):
            for columna in columnas_fecha:
                idx = indices.get(columna)
                if idx is None or idx >= len(fila):
                    continue
                
                fecha_valor = fila[idx]
                es_valida, error_msg = validar_fecha_unica(fecha_valor)
                
                if not es_valida:
                    errores.append(f"Fila {nro_fila} columna '{columna}': {error_msg}")
    
    return len(errores), errores
#-------3d ------

def detectar_duplicados(dataset):
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
#Agarramos la columna id
    idx_id = indices.get('occurrenceID')
    if idx_id is None:
        idx_id = indices.get('id')

# 2 listas. Una con todos los id y otra con los que se repiten
    todos_los_ids = []
    duplicados = []


    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for fila in lector:
            id_actual = fila[idx_id].strip()
            
            if id_actual != "": #Primero revisamos que el id no este vacio
                if id_actual in todos_los_ids: #Si esta en todos los ids y no en duplicados, lo agregamos a duplicados porque se estaria repitiendo
                    if id_actual not in duplicados:
                        duplicados.append(id_actual)
                
                else: 
                    todos_los_ids.append(id_actual) #Pero si no esta en todos los ids, lo agregamos a todos porque es la pirmera vez que aparece

    return len(duplicados), duplicados #devolvemos la lista con la cantidad de duplicados

#----------3e----------
def Detectar_invalidos_countryCode(dataset):
    """
    Detecta countryCodes inválidos.
    reutiliza validar_country_code_unico()
    """

    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    idx_countryCode = indices.get('countryCode')

    if idx_countryCode is None:
        return 0, ['No existe el campo countryCode']

    errores = []

    with open(ruta, 'r', encoding= 'utf-8')  as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next (lector)

        for i,fila in enumerate (lector, start=2):
            if idx_countryCode >= len(fila):
                continue
            valor = fila[idx_countryCode]
            es_valido, error_msg = validar_country_code_unico(valor)
            if not es_valido:
                errores.append(f"Fila {i}: {error_msg}")
    
    return len(errores), errores

#----------3f----------
def validar_incertidumbre(dataset):
    """
    Detecta registros donde la incertidumbre (coordinateUncertaintyInMeters):
    - No sea numérica.
    - Sea negativa.
    - Sea mayor a 100 metros.
    reutiliza validar_incertidumbre_unica()
    """
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    idx_inc = indices.get('coordinateUncertaintyInMeters')
    
    if idx_inc is None:
         return 0, [f"No existe 'coordinateUncertaintyInMeters' en {dataset}"]
    #agrego una lista con los errores
    errores = []
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)
        
        for nro_fila, fila in enumerate(lector, start=2):   #el primer dato real está en la Fila 2(la 1 eran los encabezados). Usar start=2 hace que los reportes de error coincidan
            if idx_inc >= len(fila):
                continue
                
            valor = fila[idx_inc]
            es_valido, error_msg = validar_incertidumbre_unica(valor)
            
            if not es_valido:
                errores.append(f"Fila {nro_fila}: {error_msg}")
    
    return len(errores), errores

#----------3g----------
def registros_taxonomia_incompleta(dataset):
    """Función auxiliar para el 3G. Cuenta cuántos registros tienen
    campos taxonómicos básicos vacíos."""
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    if isinstance(indices, str):
        return 0

    # Defino qué columnas consideramos "Información Taxonómica"
    cols_taxonomicas = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    
    # Busco los índices de esas columnas (ignoro las que no existan en el dataset)
    indices_tax = [indices.get(col) for col in cols_taxonomicas if indices.get(col) is not None]
    
    incompletos = 0
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)
        
        for fila in lector:
            # Reviso si alguna de las columnas taxonómicas está en blanco
            es_incompleto = False
            for idx in indices_tax:
                if idx < len(fila) and fila[idx].strip() == "":
                    es_incompleto = True
                    break # Con que falte un solo dato (ej: la familia), ya es incompleto
            
            if es_incompleto:
                incompletos += 1
                
    return incompletos

def generar_resumen_calidad(dataset):
    """
    Punto 3.G: Genera un resumen de calidad agrupando todas las métricas.
    Retorna un diccionario y un texto formateado.
    """
    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return None, f"Error: {indices}"

    # Recopilo todas las métricas llamando a las funciones
    total = contar_registros(dataset)
    cant_coord, _ = validar_coordenadas_rango(dataset)
    cant_fechas, _ = verificar_fechas(dataset)
    cant_duplicados, _ = detectar_duplicados(dataset)
    cant_tax_incompleta = registros_taxonomia_incompleta(dataset)

    #Armo el diccionario que pide el enunciado
    resumen_dict = {
        "dataset": dataset,
        "total_registros": total,
        "coordenadas_invalidas": cant_coord,
        "fechas_invalidas": cant_fechas,
        "duplicados": cant_duplicados,
        "taxonomia_incompleta": cant_tax_incompleta}
    #Armamos el reporte en texto (string)
    reporte_texto = f"=== REPORTE DE CALIDAD: {dataset.upper()} ===\n"
    reporte_texto += f"Total de registros: {total}\n"
    reporte_texto += f" - Coordenadas inválidas: {cant_coord}\n"
    reporte_texto += f" - Fechas inválidas: {cant_fechas}\n"
    reporte_texto += f" - Registros duplicados: {cant_duplicados}\n"
    reporte_texto += f" - Taxonomía incompleta: {cant_tax_incompleta}\n"
    reporte_texto += "========================================\n"

    return resumen_dict, reporte_texto

#----------3h----------
# Constantes de cotas geográficas para América del Sur
LAT_MAX_SA = 15.0
LAT_MIN_SA = -60.0
LON_MAX_SA = -30.0
LON_MIN_SA = -90.0

def validar_coordenadas_sudamerica(dataset):
    """Verifica que las coordenadas caigan dentro del territorio de América del Sur.
    Retorna la cantidad y el detalle de los registros que caen fuera."""
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    if isinstance(indices, str):
        return 0, [indices]

    idx_lat = indices.get('decimalLatitude')
    idx_lon = indices.get('decimalLongitude')
    
    if idx_lat is None or idx_lon is None:
        return 0, [f"Faltan columnas de coordenadas en {dataset}."]

    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for nro_fila, fila in enumerate(lector, start=2):
            if idx_lat >= len(fila) or idx_lon >= len(fila):
                continue
                
            lat_txt = fila[idx_lat].strip()
            lon_txt = fila[idx_lon].strip()

            if lat_txt == "" or lon_txt == "":
                continue

            try:
                lat = float(lat_txt)
                lon = float(lon_txt)

                # Validamos si están FUERA de nuestra "caja" sudamericana
                if not (LAT_MIN_SA <= lat <= LAT_MAX_SA) or not (LON_MIN_SA <= lon <= LON_MAX_SA):
                    errores.append(f"Fila {nro_fila}: Fuera de Sudamérica (Lat: {lat}, Lon: {lon})")
                    
            except ValueError:
                # Si no es un número, lo ignoramos acá porque ya lo detecta el Punto 3.A
                pass
                
    return len(errores), errores

#----------3i----------
def auditar_coordenada_generica(dataset, nombre_columna, min_glob, max_glob, min_sa, max_sa):
    """Función base REUTILIZABLE para auditar cualquier columna de coordenadas"""
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    if isinstance(indices, str): return 0, [indices]
    
    idx = indices.get(nombre_columna)
    if idx is None: return 0, [f"No existe '{nombre_columna}' en {dataset}"]

    errores = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for i, fila in enumerate(lector, start=2):
            if idx >= len(fila): continue
            
            val_txt = fila[idx].strip()
            if val_txt == "": continue

            try:
                val = float(val_txt)
                # 1. Validación Global
                if not (min_glob <= val <= max_glob):
                    errores.append(f"Fila {i}: Inválida globalmente ({val})")
                # 2. Validación Sudamérica
                elif not (min_sa <= val <= max_sa):
                    errores.append(f"Fila {i}: Fuera de Sudamérica ({val})")
            except ValueError:
                # 3. Validación de Tipo
                errores.append(f"Fila {i}: Formato erróneo ('{val_txt}')")

    return len(errores), errores

def auditar_columna_latitud(dataset):
    # Rango global lat: [-90, 90] | Rango SA: [LAT_MIN_SA, LAT_MAX_SA]
    return auditar_coordenada_generica(dataset, 'decimalLatitude', -90.0, 90.0, LAT_MIN_SA, LAT_MAX_SA)

def auditar_columna_longitud(dataset):
    # Rango global lon: [-180, 180] | Rango SA: [LON_MIN_SA, LON_MAX_SA]
    return auditar_coordenada_generica(dataset, 'decimalLongitude', -180.0, 180.0, LON_MIN_SA, LON_MAX_SA)