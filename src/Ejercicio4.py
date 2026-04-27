from pathlib import Path
import csv
from datetime import datetime
from iso3166 import countries
from Ejercicio2A import obtener_ruta_y_separador,columnas_dataset,contar_registros

#------4a------

#La estructura que va a representar un registro va a ser un diccionario, donde cada columna va a ser una clave
#y el dato de esa columna será el valor que le corresponde a la clave

#------4b------

def generar_registro_vacio(columnas):
    registro = {}
    for campo in columnas:
        if campo != "id" and campo != "gbifID" and campo != "occurrenceID":
            registro[campo]= None
    return registro
    
#------4c------

def validar_registro (dataset, registro):
    """ Valida un registro antes de insertarlo,
        reutilizando las validaciones del ejercicio 3."""
    errores = []
    
    # Obtenemos los valores de latitud y longitud del registro
    lat_txt = registro.get("decimalLatitude")
    lon_txt = registro.get("decimalLongitude")

    # Validación 3b: chequear que no falte ninguna coordenada
    if lat_txt and not lon_txt:
        errores.append("Tiene latitud pero falta longitud")
    elif lon_txt and not lat_txt:
        errores.append("Tiene longitud pero falta latitud")

    # Validación 3a: chequear que las coordenadas sean números válidos y estén en rango
    if lat_txt and lon_txt:
        es_lat_num = lat_txt.replace('.','',1).replace('-','',1).isdigit()
        es_lon_num = lon_txt.replace('.','',1).replace('-','',1).isdigit()
        
        if not es_lat_num or not es_lon_num:
            errores.append("Las coordenadas no son números válidos")
        else:
            lat = float(lat_txt)
            lon = float(lon_txt)
            if not (-90 <= lat <= 90):
                errores.append("La latitud está fuera de rango [-90, 90]")
            if not (-180 <= lon <= 180):
                errores.append("La longitud está fuera de rango [-180, 180]")
    
    # Columnas de fecha a validar
    columnas_fecha = {
        "IADIZA": ['modified', 'eventDate', 'verbatimEventDate', 'dateIdentified', 'georeferencedDate', 'lastInterpreted', 'lastParsed', 'lastCrawled'],
        "Inaturalist": ['eventDate', 'modified', 'verbatimEventDate', 'dateIdentified'],
        "XenoCanto": ['eventDate', 'verbatimEventDate']
    }

    formatos = [
    "%Y-%m-%d",             
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%fZ",   
    "%Y-%m-%dT%H:%M:%S%z",  
    "%Y-%m",                 
    "%Y",                    
    ]
    anio_actual = datetime.now().year

    # Validación 3c: fechas
    for columna in columnas_fecha.get(dataset, []):
        fecha_txt = registro.get(columna)
        if not fecha_txt:  # si está vacío lo saltea
            continue
    
        fecha_valida = False
        for formato in formatos:
            try:
                fecha = datetime.strptime(fecha_txt, formato)
                fecha_valida = True
                if fecha.year > anio_actual:
                    errores.append(f"Columna '{columna}': fecha posterior al año actual: {fecha_txt}")
                break
            except ValueError:
                continue
    
        if not fecha_valida:
            errores.append(f"Columna '{columna}': formato de fecha inválido: {fecha_txt}")
    
    # Validación 3e: countryCode
    country_code = registro.get("countryCode")
    if country_code:
        country_code = country_code.strip().upper()
        if country_code not in {'ZZ', 'XZ'}:
            try:
                countries.get(country_code)
            except KeyError:
                errores.append(f"countryCode inválido: '{country_code}'")
    
    # Validación 3f: coordinateUncertaintyInMeters
    incertidumbre = registro.get("coordinateUncertaintyInMeters")
    if incertidumbre:
        try:
            valor = float(incertidumbre)
            if valor < 0:
                errores.append("coordinateUncertaintyInMeters es negativo")
            elif valor > 100:
                errores.append(f"coordinateUncertaintyInMeters es demasiado grande (>100): {valor}")
        except ValueError:
            errores.append(f"coordinateUncertaintyInMeters no es un número válido: '{incertidumbre}'")
    es_valido = len(errores) == 0
    return es_valido, errores

#------4d------

def registro_a_fila(dataset, registro):
    """
    Convierte un registro (diccionario del 4A) en una lista lista para 
    agregar al CSV, deduciendo y agregando el ID correspondiente a cada dataset.
    """

    columnas = columnas_dataset(dataset)
    if isinstance (columnas,str): # si devolvió un string = hubo error
        return f"Dataset '{dataset}' no reconocido."
    
    # Generamos el ID según cada dataset
    if dataset== "IADIZA": 
        # Su occurrenceID se forma como IADIZA:COI:catalogNumber
        catalog = registro.get('catalogNumber', '')
        registro['occurrenceID']= f"IADIZA:COI:{catalog}"
        # gbifID lo asigna GBIF, entonces lo dejamos vacío
        registro ['gbifID']=''
    
    elif dataset == "Inaturalist":
        # El id es autoincremental, necesitamos saber cuantos registros hay para calcular el ID que sigue
        total = contar_registros(dataset)
        registro['id'] = str(total + 1)
    
    elif dataset == "XenoCanto":
        # El id ( XXXXXX@XC )se forma a partir del catalogNumber
        catalog = registro.get('catalogNumber', '')
         # catalogNumber es XC999540, entonces nos quedamos solo con el número (es decir, sin XC)
        numero = catalog.replace('XC', '')
        registro['id'] = f"{numero}@XC"
    
    # Convertimos el diccionario a lista en el orden de las columnas del CSV
    fila = []
    for columna in columnas:
        valor = registro.get(columna)
        if valor is None:
            fila.append('')
        else:
            fila.append(str(valor))

    return fila