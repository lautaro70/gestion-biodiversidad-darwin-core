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
   # Creamos un diccionario donde los anios sean la clave y la cantidad de registros su valor
    diccionario_anios = {}
    
    # Inicializamos contadores para registrar cuántos datos se descartan 
    excluidos_nulos = 0
    excluidos_invalidos = 0

    # Nos aseguramos de saber si existe la columna de respaldo 'year'
    tiene_columna_year = 'year' in df.columns

    for i, celda in enumerate(df['eventDate']):
        anio_numero = None
        
        # 1. Intentamos extraer el año de eventDate si es un dato válido
        if not pd.isna(celda) and str(celda).strip() not in ["None", "nan", "<NA>", ""]:
            try:
                anio_texto = str(celda)[:4]
                anio_numero = int(anio_texto)
            except:
                pass # Si falla, dejamos que intente con la columna 'year'

        # 2. Si eventDate falló o era "None", usamos la columna 'year' como respaldo
        if anio_numero is None and tiene_columna_year:
            valor_year = df['year'].iloc[i]
            if not pd.isna(valor_year) and str(valor_year).strip() not in ["None", "nan", "", "0"]:
                try:
                    anio_numero = int(float(valor_year)) # float por si viene como 1998.0
                except:
                    pass

        # 3. Si logramos conseguir un año válido (por cualquiera de las dos vías)
        if anio_numero is not None:
            # Verificamos si el año está dentro de lo que el usuario movió en el slider
            if anio_inicio <= anio_numero <= anio_fin:
                if anio_numero in diccionario_anios:
                    diccionario_anios[anio_numero] += 1
                else:
                    diccionario_anios[anio_numero] = 1
        else:
            # Si no pudimos rescatar el año de ninguna forma, lo contamos como excluido
            if pd.isna(celda) or str(celda).strip() in ["None", "nan", "<NA>", ""]:
                excluidos_nulos += 1
            else:
                excluidos_invalidos += 1
        
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
#-----------------Ejercicio 3c--------------------


def obtener_datos_taxonomia(df, columna_taxonomica):

    #Segun la categoria elegida (familia,clase,orden) contamos cuantos registros hay

    conteo_taxo = df[columna_taxonomica].value_counts()
    
    return conteo_taxo