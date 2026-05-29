import pandas as pd


#--------3a-------------
def obtener_datos_barras(df, top_n): 
    # top_n es la cantidad de barras que desea ver el usuario
    # guardo los paises que no se repiten con el unique y el dropna elimina espacios vacios
    paises_unicos = df['country'].dropna().unique() if 'country' in df else []

    if len(paises_unicos) > 1: 
        # Si hay más de un país lo guardamos en la variable (Lleva un tabulador extra)
        columna_agrupar = 'country'
    else: 
        # Y sino los guardamos en la provincia o localidad si no existe la primera S
        columna_agrupar = 'stateProvince' if 'stateProvince' in df else 'locality'

    
    conteos = df[columna_agrupar].value_counts()
    conteos_top = conteos.head(top_n)
    
    return conteos_top, columna_agrupar