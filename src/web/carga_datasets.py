import pandas as pd
from common.constants import PROCESSED_DATASETS

def cargar_dataset_procesado(dataset: str) -> pd.DataFrame:
    """Punto 1.A: Carga un dataset desde la carpeta processed_datasets 
    como un DataFrame de pandas, respetando su separador y codificación."""
    
    informacion_dataset = PROCESSED_DATASETS.get(dataset)
    ruta_procesada = informacion_dataset["path"]
    separador = informacion_dataset["separator"]

    # Validación de seguridad por si aún no se generó el archivo sanitizado
    if not ruta_procesada.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo procesado para '{dataset}' en: {ruta_procesada}. "
            f"Asegúrese de haber ejecutado la sanitización de la Etapa 1."
        )
        
    # Cargo el DataFrame completo (permitido en esta etapa)
    dataframe_resultado = pd.read_csv(
        ruta_procesada, 
        delimiter=separador, 
        encoding='utf-8', 
        low_memory=False
    )
    
    return dataframe_resultado