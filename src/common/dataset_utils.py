def obtener_ruta_y_separador(dataset: str) -> tuple:
    """
    Retorna la ruta y el separador asociados a un dataset.
    """

    from common.constants import DATASETS

    informacion_dataset = DATASETS.get(dataset)

    if informacion_dataset is None:
        return None, None

    return (
        informacion_dataset["path"],
        informacion_dataset["separator"]
    )