from pathlib import Path
import csv
from datetime import datetime
from Ejercicio2A import obtener_ruta_y_separador, obtener_indices_columnas, contar_registros
from iso3166 import countries



#Arranco con el 3a



def validar_coordenadas_rango(dataset):

    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
#Agarro los indices de las latitudes y longitudes gracias a las funciones del punto 2
    idx_lat = indices.get('decimalLatitude')
    idx_lon = indices.get('decimalLongitude')

    errores=[] #Aca es donde voy a guardar los registros incorrectos


    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for nro_fila, fila in enumerate(lector, start=2):
            lat_txt = fila[idx_lat].strip() #El strip saca los espacios en blanco
            lon_txt = fila[idx_lon].strip()

            #Aca lo que hago es que me muestre el numero solamente en cada latitud o longitud, sin los signos y puntos
            #El numero 1 significa que solo le saca el primer guion o coma 
            es_lat_num = lat_txt.replace('.','',1).replace('-','',1).isdigit()
            es_lon_num = lon_txt.replace('.','',1).replace('-','',1).isdigit()

            if not es_lat_num or not es_lon_num:
                errores.append(f"Fila {nro_fila}: Error, la coordenada no es un número válido.")
            else:
                lat = float(lat_txt)
                lon = float(lon_txt)
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    errores.append(f"Fila {nro_fila}: Número fuera de rango.")

    return len(errores),errores #Aca devuelve la lista con los errores

#Para tener la cantidad de errores hacemos un len y la tenemos


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

    return incompletos


#------ 3c ------
def verificar_fechas(dataset):
    """
    Revisa que las fechas de los datasets sean válidas. 
    Se consideran válidas a las fechas que tengan el formato adecuado y no sean mayores al año actual
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
        return f"No se reconoce el dataset '{dataset}'"

    # escribimos los formatos de fechas válidos (formatos que define el estándar Darwin Core y GBIF)
    formatos = [
    "%Y-%m-%d",             
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%fZ",   
    "%Y-%m-%dT%H:%M:%S%z",  
    "%Y-%m",                 
    "%Y",                    
    ]

    anio_actual = datetime.now().year
    errores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for nro_fila, fila in enumerate(lector, start=2):
            for columna in columnas_fecha:  #para cada fila revisamos cada columna de fecha
                idx = indices.get(columna)  #obtenemos el indice de la columna
                if idx is None:
                    continue    #si la columna no existe en el dataset la saltea

                fecha_txt = fila[idx].strip()  #nos quedamos con la fecha

                if fecha_txt == "":  #si está vacio lo saltea
                    continue

                fecha_valida = False
                for formato in formatos:  #prueba los formatos para ver cual es el válido
                    try:
                        #strptime convierte un texto a fecha usando el formato que le digamos
                        fecha = datetime.strptime(fecha_txt, formato)
                        fecha_valida = True
                        if fecha.year > anio_actual:
                            errores.append(f"Fila {nro_fila} columna '{columna}': Fecha posterior al año actual: {fecha_txt}")
                        break  #si es el formato correcto frenamos
                    except ValueError:
                        continue 

                if not fecha_valida:
                    errores.append(f"Fila {nro_fila} columna '{columna}': Formato inválido: {fecha_txt}")

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

    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)

    idx_countryCode = indices.get('countryCode')

    if idx_countryCode is None:
        return 'No Existe el campo countryCode'

    errores = []

    with open(ruta, 'r', encoding= 'utf-8')  as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next (lector)

        for i,fila in enumerate (lector, start=2):
            valor = fila[idx_countryCode].strip().upper()

            if valor != '':
                if valor in {'ZZ','XZ'}:
                    continue
                try:
                    countries.get(valor)
                except KeyError:
                     errores.append(f"Fila {i}: countryCode invalido - '{valor}'")
    return len(errores), errores

#----------3f----------
def validar_incertidumbre(dataset):
    """
    Detecta registros donde la incertidumbre (coordinateUncertaintyInMeters):
    - No sea numérica.
    - Sea negativa.
    - Sea mayor a 100 metros.
    """
    ruta, sep = obtener_ruta_y_separador(dataset)
    indices = obtener_indices_columnas(dataset)
    
    idx_inc = indices.get('coordinateUncertaintyInMeters')
    
    if idx_inc is None:
        return f"La columna 'coordinateUncertaintyInMeters' no existe en {dataset}."
    #agrego una lista con los errores
    errores = []
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)
        
        for nro_fila, fila in enumerate(lector, start=2):   #el primer dato real está en la Fila 2(la 1 eran los encabezados). Usar start=2 hace que los reportes de error coincidan
            if idx_inc >= len(fila):
                continue
                
            valor_txt = fila[idx_inc].strip()
            
            if valor_txt == "":
                continue    # Los nulos ya los tratamos en el Punto 2, acá buscamos inválidos
            
            try:
                valor = float(valor_txt)
                if valor < 0:
                    errores.append(f"Fila {nro_fila}: Valor negativo ({valor_txt})")
                elif valor > 100:
                    errores.append(f"Fila {nro_fila}: Valor fuera de rango (>100): {valor_txt}")
            except ValueError:
                errores.append(f"Fila {nro_fila}: No es un número válido: '{valor_txt}'")
                
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
        return f"Faltan columnas de coordenadas en {dataset}."

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