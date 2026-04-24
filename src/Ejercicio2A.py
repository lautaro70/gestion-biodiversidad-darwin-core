from pathlib import Path
import csv

def mostrar_primeras_filas_Conicet():
    base = Path(__file__).parent 
    ruta = base.parent / 'raw_datasets' / 'IADIZA-CONICET' / 'IADIZA-CONICET' / 'occurrence.txt'
    with open(ruta, 'r') as Conicet_dataset:
        csv_reader_Conicet = csv.reader(Conicet_dataset, delimiter='\t')
        header = next(csv_reader_Conicet)
        
        for i,row in enumerate(csv_reader_Conicet):
            print (row)
            if i >= 9:
                break
            
def mostrar_primeras_filas_Inaturalist ():
    base = Path(__file__).parent 
    ruta = base.parent / 'raw_datasets' / 'Inaturalist' / 'Inaturalist' / 'observations.csv'
    with open(ruta, 'r') as Inaturalist_dataset:
        csv_reader_Inaturalist = csv.reader(Inaturalist_dataset, delimiter=',')
        header = next(csv_reader_Inaturalist)
        
        for i,row in enumerate(csv_reader_Inaturalist):
            print (row)
            if i >= 9:
                break

def mostrar_primeras_filas_XenoCanto ():
    base = Path(__file__).parent 
    ruta = base.parent / 'raw_datasets' / 'XenoCanto' / 'XenoCanto' / 'Occurrence.txt'
    with open(ruta, 'r',encoding='utf-8') as XenoCanto_dataset:
        csv_reader_XenoCanto = csv.reader(XenoCanto_dataset, delimiter=',')
        header = next(csv_reader_XenoCanto)
        
        for i,row in enumerate(csv_reader_XenoCanto):
            print (row)
            if i >= 9:
                break

def obtener_ruta_y_separador(dataset):
    base = Path(__file__).parent 
    ruta_raiz = base.parent 
    
    if dataset == "IADIZA":
        ruta = ruta_raiz / 'raw_datasets' / 'IADIZA-CONICET' / 'IADIZA-CONICET' / 'occurrence.txt'
        sep = '\t'
    elif dataset == "Inaturalist":
        ruta = ruta_raiz / 'raw_datasets' / 'Inaturalist' / 'Inaturalist' / 'observations.csv'
        sep = ','
    elif dataset == "XenoCanto":
        ruta = ruta_raiz / 'raw_datasets' / 'XenoCanto' / 'XenoCanto' / 'occurrence.txt'
        sep = ','
    else:
        return None, None
    return ruta, sep			

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