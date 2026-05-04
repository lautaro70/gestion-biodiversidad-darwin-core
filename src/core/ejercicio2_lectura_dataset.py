import csv
from typing import Optional, Union

from common.dataset_utils import obtener_ruta_y_separador

def mostrar_primeras_filas(dataset: str) -> Optional[str]:
    """
    Abre el archivo principal del dataset y muestra las primeras 10 filas.
    Imprime los primeros 5 encabezados como referencia.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."
        
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        
        # Opcional: Imprimir encabezado primero
        encabezados = next(lector_csv)
        print(f"--- ENCABEZADOS: {encabezados[:5]}... ---") # Muestro los primeros 5 para no saturar
        
        for indice, fila in enumerate(lector_csv):
            print(fila)
            if indice >= 8: # (llega hasta 9 porque ya leímos el header)
                break

# INICIO DEL INCISO 2b 

def columnas_dataset(dataset: str) -> Union[list[str], str]:
    """
    Retorna la lista completa de nombres de columnas del dataset.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """
    ruta, separador = obtener_ruta_y_separador(dataset) 
    if ruta is None:  
        return f"Dataset '{dataset}' no reconocido."
    with open(ruta, 'r', encoding='utf-8') as archivo_abierto: 
        lector_csv = csv.reader(archivo_abierto, delimiter=separador)
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
    indices = {nombre: indice for indice, nombre in enumerate(nombres)}
    return indices	

#INCISO 2d
def contar_registros(dataset: str) -> Union[int, str]:
    """Retorna la cantidad total de registros (filas de datos) del dataset,
    sin contar el encabezado.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None: 
        return f"Dataset '{dataset}' no reconocido."
    #EL encoding utf-8 es para que se lean los caracteres especiales
    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador) #"hasta aca podemos hacer una nueva funcion para que haga esto las veces necesarias"
        next(lector_csv)
        cantidad = 0
        for fila in lector_csv:
            cantidad += 1
    return cantidad 

#INCISO 2e
def columnas_con_nulos(dataset: str) -> Union[list[str], str]:
    """Retorna una lista con los nombres de las columnas que tienen 
    al menos un registro nulo, reutilizando la función del Punto 2.C.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """
    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None: 
        return f"Dataset '{dataset}' no reconocido."
    indices_columnas = obtener_indices_columnas(dataset)
    if isinstance(indices_columnas, str):
        return indices_columnas
    columnas_vacias = set()
    with open(ruta, 'r', encoding='utf-8') as archivo: 
        lector_csv = csv.reader(archivo, delimiter=separador)
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
def porcentaje_nulos(dataset: str) -> Union[dict[str, float], str]:
    """
    Retorna el porcentaje de valores nulos por columna como un diccionario
    {nombre_columna: porcentaje}.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    total_filas = contar_registros(dataset)  # Reutilizo función ya hecha
    
    # Evito división por 0 en caso de dataset vacío
    if total_filas == 0:
        return {}

    conteo_nulos = {columna: 0 for columna in indices}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        next(lector_csv)

        for fila in lector_csv:
            for columna, indice in indices.items():
                # indice < len evita errores si la fila está incompleta
                if indice < len(fila) and fila[indice].strip() == "":
                    conteo_nulos[columna] += 1
     
    # Convierto el conteo de nulos a porcentaje por columna
    return {
        columna: (conteo_nulos[columna] / total_filas) * 100
        for columna in conteo_nulos
    }
 
#Inciso 2g 
def valores_distintos(dataset: str, columna: str) -> Union[int, str]:
    """
    Retorna la cantidad de valores distintos (no vacíos) de una columna.
    Devuelve un mensaje de error si el dataset o la columna no existen.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Verifico que la columna exista
    if columna not in indices:
        return f"La columna '{columna}' no existe."

    indice = indices[columna]
    valores = set()  # El set guarda solo valores únicos

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        next(lector_csv)

        for fila in lector_csv:
            # indice < len para evitar error si la fila está incompleta
            if indice < len(fila):
                valor = fila[indice].strip()
                # Ignoro valores vacíos para no contarlos como distintos
                if valor != "":
                    valores.add(valor)
    return len(valores)
 
#Inciso 2h
def frecuencia_valores(dataset: str, columna: str) -> Union[dict[str, int], str]:
    """
    Retorna la frecuencia de aparición de cada valor (no vacío) en una columna,
    como un diccionario {valor: cantidad}.
    Devuelve un mensaje de error si el dataset o la columna no existen.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Verifico que la columna exista
    if columna not in indices:
        return f"La columna '{columna}' no existe."

    indice = indices[columna]
    frecuencia = {}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        next(lector_csv)

        # Recorro el dataset fila por fila sin cargarlo completo en memoria
        for fila in lector_csv:
            if indice < len(fila):
                valor = fila[indice].strip()

                # Ignoro valores vacíos para no ensuciar el conteo
                if valor != "":
                    # get(valor, 0) evita hacer if valor in diccionario
                    frecuencia[valor] = frecuencia.get(valor, 0) + 1

    return frecuencia

#Inciso 2i
def analisis_columna(dataset: str, columna: str, tipo: str) -> Union[dict, str]:
    """
    Retorna estadísticas de una columna según su tipo:
    - 'numeric': min, max, promedio.
    - 'coordinate': min, max.
    - 'text': longitud mínima y máxima de los valores.
    Devuelve un mensaje de error si el dataset, la columna o el tipo no son válidos.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    if columna not in indices:
        return f"La columna '{columna}' no existe."

    indice = indices[columna]
    valores = []

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        next(lector_csv)

        # Recorro el dataset sin cargarlo completo en memoria
        for fila in lector_csv:
            # Filtro valores válidos (no vacíos)
            if indice < len(fila) and fila[indice].strip() != "":
                valores.append(fila[indice])

    if not valores:
        return "No hay datos válidos"

    #CASOS SEGÚN TIPO

    if tipo == "numeric" or tipo == "coordinate":
        numeros = []

        # Intento convertir a float (evita que falle si hay datos sucios)
        for valor in valores:
            try:
                numeros.append(float(valor))
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
        longitudes = [len(valor) for valor in valores]

        return {
            "min_len": min(longitudes),
            "max_len": max(longitudes)
        }

    else:
        return "Tipo no válido"

#Inciso 2j
def columnas_totalmente_nulas(dataset: str) -> Union[list[str], str]:
    """
    Retorna la lista de columnas cuyos valores son nulos en absolutamente
    todos los registros del dataset.
    Devuelve un mensaje de error si el dataset no es reconocido.
    """

    ruta, separador = obtener_ruta_y_separador(dataset)
    if ruta is None:
        return f"Dataset '{dataset}' no reconocido."

    indices = obtener_indices_columnas(dataset)
    if isinstance(indices, str):
        return indices

    # Supongo inicialmente que todas las columnas son completamente nulas
    columnas_nulas = {columna: True for columna in indices}

    with open(ruta, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.reader(archivo, delimiter=separador)
        next(lector_csv)

        # Recorro el dataset fila por fila (sin cargar todo en memoria)
        for fila in lector_csv:
            for columna, indice in indices.items():
                # Si encuentro un valor no vacío, la columna deja de ser completamente nula
                if indice < len(fila) and fila[indice].strip() != "":
                    columnas_nulas[columna] = False

    # Devuelvo solo las columnas que quedaron siempre vacías
    return [columna for columna, es_nula in columnas_nulas.items() if es_nula]
