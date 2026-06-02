import pandas as pd


#--------3a-------------
def obtener_datos_barras(df, top_n): 
    # top_n es la cantidad de barras que desea ver el usuario
    # guardo los paises que no se repiten con el unique y el dropna elimina espacios vacios
    paises_unicos = df['country'].dropna().unique() if 'country' in df else []

    if len(paises_unicos) > 1: 
        # Si hay más de un país lo guardamos en la variable 
        columna_agrupar = 'country'
    else: 
        # Y sino los guardamos en la provincia o localidad si no existe la primera 
        columna_agrupar = 'stateProvince' if 'stateProvince' in df else 'locality'

    
    conteos = df[columna_agrupar].value_counts()
    conteos_top = conteos.head(top_n)
    
    return conteos_top, columna_agrupar

#------3b

def obtener_datos_lineas(df, anio_inicio, anio_fin):
    # Creamos un diccionario donde los anios sean la clave y la cantidad de registros que hay en ellos el valor
    diccionario_anios = {}
    
    # Inicializamos contadores para registrar cuántos datos se descartan 
    excluidos_nulos = 0
    excluidos_invalidos = 0

    for celda in df['eventDate']:
        if pd.isna(celda): # Si el valor de la celda es nulo
            excluidos_nulos += 1
            continue # Saltamos a la siguiente fila
        
        try:
            texto_fecha = str(celda) # Como la mayoria de las fechas vienen: 2024-06-07 agarramos los primeros 4 caracteres
            anio_texto = texto_fecha[:4]

            anio_numero = int(anio_texto) # Convertimos los 4 caracteres en numero entero
            
            # Verificamos si el año está dentro de lo que el usuario movió en el slider
            if anio_numero >= anio_inicio and anio_numero <= anio_fin:
                if anio_numero in diccionario_anios:
                    # Si el año ya estaba en nuestro diccionario, le sumamos 1 al contador
                    diccionario_anios[anio_numero] += 1
                else:
                    # Si es la primera vez que aparece este año, lo inauguramos en 1
                    diccionario_anios[anio_numero] = 1

        except:
            # Si la celda tenía un texto roto o inválido (ejem: "Fecha desconocida") que no se puede pasar a int,
            # el 'try' va a fallar, y el 'except' va a haacer que siga sin romper el programa.
            excluidos_invalidos += 1
            continue
        
    # Ordenamos las tuplas por su clave (el anio) 
    lista_ordenada = sorted(diccionario_anios.items())
        
    # Separamos los anios finales por un lado y los conteos por otro
    anios_finales = [elemento[0] for elemento in lista_ordenada]
    conteos_finales = [elemento[1] for elemento in lista_ordenada]

    # Lo metemos en una Serie de Pandas para que se conecte con nuestro archivo
    resultado_serie = pd.Series(conteos_finales, index=anios_finales)
    
    # Calculamos el total de registros que no entraron en el gráfico
    total_excluidos = excluidos_nulos + excluidos_invalidos
    
    return resultado_serie, total_excluidos