from pathlib import Path
import csv
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

 def Detectar_invalidos_countryCode (dataset):

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
