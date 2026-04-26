from pathlib import Path
import csv

def mostrar_primeras_filas(dataset):
    """Abre el archivo principal y muestra las primeras 10 filas."""
    ruta, sep = obtener_ruta_y_separador(dataset)
    
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."
        
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=sep)
        
        # Opcional: Imprimir encabezado primero
        header = next(lector_csv)
        print(f"--- ENCABEZADOS: {header[:5]}... ---") # Muestro los primeros 5 para no saturar
        
        for i, row in enumerate(lector_csv):
            print(row)
            if i >= 8: # (llega hasta 9 porque ya leímos el header)
                break

def obtener_ruta_y_separador(dataset):
    base = Path(__file__).parent.parent 
    # El diccionario guarda { "Nombre": (ruta, separador) }
    config_datasets = {
        "IADIZA": (base / 'raw_datasets' / 'IADIZA-CONICET' / 'IADIZA-CONICET' / 'occurrence.txt', '\t'),
        "Inaturalist": (base / 'raw_datasets' / 'Inaturalist' / 'Inaturalist' / 'observations.csv', ','),
        "XenoCanto": (base / 'raw_datasets' / 'XenoCanto' / 'XenoCanto' / 'Occurrence.txt', ',')}
    # El método .get() busca la clave. Si no la encuentra, devuelve (None, None)
    return config_datasets.get(dataset, (None, None))	

# INICIO DEL INCISO 2b 
#Hacer una funcion con las columnas de los datasets

def columnas_dataset(dataset): 
    ruta, sep = obtener_ruta_y_separador(dataset) 
    if ruta is None:  
        return f"Dataset '{dataset}' no reconocido."
    with open(ruta, 'r', encoding='utf-8') as archivo_abierto: 
        lector_csv = csv.reader(archivo_abierto, delimiter=sep)
        #El lector agarra el archivo para que python lo entienda y lo separe con el separador
        columnas = next(lector_csv) 
        #El next devuelve la primera fila del dataset que mandamos para tener los nombres de las columnas
        return columnas
    #print(columnas_dataset("IADIZA"))

#INCISO 2c
def obtener_indices_columnas(dataset):
    """Retorna un diccionario con {nombre_columna: indice}"""  
    nombres = columnas_dataset(dataset)
    if isinstance(nombres, str):
        return nombres
    #Uso una comprensión de diccionario para mapear nombre -> posición
    indices = {nombre: i for i, nombre in enumerate(nombres)}
    return indices	

#INCISO 2d
def contar_registros(dataset):
    """Retorna la cantidad total de registros (filas de datos) del dataset,
    sin contar el encabezado."""
    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None: 
        return f"Dataset '{dataset}' no reconocido."
    #EL encoding utf-8 es para que se lean los caracteres especiales
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=sep) #"hasta aca podemos hacer una nueva funcion para que haga esto las veces necesarias"
        next(lector_csv)
        cantidad = 0
        for fila in lector_csv:
            cantidad += 1
    return cantidad 

#INCISO 2e
def columnas_con_nulos(dataset):
    """Retorna una lista con los nombres de las columnas que tienen 
    al menos un registro nulo, reutilizando la función del Punto 2.C."""
    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None: 
        return f"Dataset '{dataset}' no reconocido."
    indices_columnas=obtener_indices_columnas(dataset)
    if isinstance(indices_columnas, str):
        return indices_columnas
    columnas_vacias = set()
    with open(ruta, 'r', encoding='utf-8') as archivo: 
        lector_csv = csv.reader(archivo, delimiter=sep)
        # Saltamos el encabezado porque los nombres ya los trajo la función 2.C
        next(lector_csv) 
        #Recorro el archivo
        for fila in lector_csv:
                #Uso el diccionario para revisar solo los índices válidos
            for nombre_columna, indice in indices_columnas.items():
                if indice < len(fila) and fila[indice].strip() == "":
                    columnas_vacias.add(nombre_columna) 
        return list(columnas_vacias)

#INCISO 2f
def porcentaje_nulos(dataset):
    """Retorna el porcentaje de valores nulos por columna"""

    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    total_filas = contar_registros(dataset)  # Reutilizo función ya hecha
    
    # Evito división por 0 en caso de dataset vacío
    if total_filas == 0:
        return {}

    conteo_nulos = {col: 0 for col in indices}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for fila in lector:
            for col, idx in indices.items():
                # idx < len evita errores si la fila está incompleta
                if idx < len(fila) and fila[idx].strip() == "":
                    conteo_nulos[col] += 1
     
    # Convierto el conteo de nulos a porcentaje por columna
    return {
        col: (conteo_nulos[col] / total_filas) * 100
        for col in conteo_nulos
    }
 
#Inciso 2g 
def valores_distintos(dataset, columna):
    """Retorna la cantidad de valores distintos de una columna"""

    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Verifico que la columna exista
    if columna not in indices:
        return f"La columna '{columna}' no existe."

    idx = indices[columna]
    valores = set()  # El set guarda solo valores únicos

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        for fila in lector:
            # idx < len para evitar error si la fila está incompleta
            if idx < len(fila):
                valor = fila[idx].strip()
                # Ignoro valores vacíos para no contarlos como distintos
                if valor != "":
                    valores.add(valor)
    return len(valores)
 
#Inciso 2h
def frecuencia_valores(dataset, columna):
    """Retorna la frecuencia de aparición de cada valor en una columna"""

    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Verifico que la columna exista
    if columna not in indices:
        return f"La columna '{columna}' no existe."

    idx = indices[columna]
    frecuencia = {}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        # Recorro el dataset fila por fila sin cargarlo completo en memoria
        for fila in lector:
            if idx < len(fila):
                valor = fila[idx].strip()

                # Ignoro valores vacíos para no ensuciar el conteo
                if valor != "":
                    # get(valor, 0) evita hacer if valor in diccionario
                    frecuencia[valor] = frecuencia.get(valor, 0) + 1

    return frecuencia

#Inciso 2i
def analisis_columna(dataset, columna, tipo):
    """numeric: min, max, promedio
       coordinate: min, max
       text: longitud mínima y máxima"""

    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    if columna not in indices:
        return f"La columna '{columna}' no existe."

    idx = indices[columna]
    valores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        # Recorro el dataset sin cargarlo completo en memoria
        for fila in lector:
            # Filtro valores válidos (no vacíos)
            if idx < len(fila) and fila[idx].strip() != "":
                valores.append(fila[idx])

    if not valores:
        return "No hay datos válidos"

    #CASOS SEGÚN TIPO

    if tipo == "numeric" or tipo == "coordinate":
        numeros = []

        # Intento convertir a float (evita que falle si hay datos sucios)
        for v in valores:
            try:
                numeros.append(float(v))
            except ValueError:
                continue  # ignoro valores no numéricos

        if not numeros:
            return "No hay datos numéricos válidos"

        resultado = {
            "min": min(numeros),
            "max": max(numeros)
        }

        if tipo == "numeric":
            resultado["promedio"] = sum(numeros) / len(numeros)

        return resultado

    elif tipo == "text":
        # Mido la longitud de cada string
        longitudes = [len(v) for v in valores]

        return {
            "min_len": min(longitudes),
            "max_len": max(longitudes)
        }

    else:
        return "Tipo no válido"

#Inciso 2j
def columnas_totalmente_nulas(dataset):
    """Retorna las columnas cuyos valores son nulos en todos los registros"""

    ruta, sep = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Supongo inicialmente que todas las columnas son completamente nulas
    columnas_nulas = {col: True for col in indices}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo, delimiter=sep)
        next(lector)

        # Recorro el dataset fila por fila (sin cargar todo en memoria)
        for fila in lector:
            for col, idx in indices.items():
                # Si encuentro un valor no vacío, la columna deja de ser completamente nula
                if idx < len(fila) and fila[idx].strip() != "":
                    columnas_nulas[col] = False

    # Devuelvo solo las columnas que quedaron siempre vacías
    return [col for col, es_nula in columnas_nulas.items() if es_nula]
