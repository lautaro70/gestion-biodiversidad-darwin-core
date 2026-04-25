from pathlib import Path
import csv
from Ejercicio2A import obtener_ruta_y_separador, obtener_indices_columnas, contar_registros



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

    return errores #Aca devuelve la lista con los errores

#Para tener la cantidad de errores hacemos un len y la tenemos


#----3b----

