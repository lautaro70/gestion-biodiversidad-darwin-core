from pathlib import Path

#Ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

#Configuración centralizada de datasets
DATASETS = {
    "IADIZA": {
        "path": BASE_DIR / "raw_datasets" / "IADIZA-CONICET" / "IADIZA-CONICET" / "occurrence.txt",
        "separator": "\t"
    },

    "Inaturalist": {
        "path": BASE_DIR / "raw_datasets" / "Inaturalist" / "Inaturalist" / "observations.csv",
        "separator": ","
    },

    "XenoCanto": {
        "path": BASE_DIR / "raw_datasets" / "XenoCanto" / "XenoCanto" / "occurrence.txt",
        "separator": ","
    }
}