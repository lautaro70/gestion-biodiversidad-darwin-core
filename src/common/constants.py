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
        "path": BASE_DIR / "raw_datasets" / "XenoCanto" / "XenoCanto" / "Occurrence.txt",
        "separator": ","
    }
}

#Lista de codigos ISO 3166
country_codes_validos = {
    "AR", "BR", "CL", "UY", "PY", "PE", "CO", "VE",
    "MX", "US", "CA", "ES", "FR", "DE", "IT", "GB",
    "PT", "NL", "BE", "CH", "SE", "NO", "DK", "FI",
    "JP", "CN", "KR", "IN", "AU", "NZ", "ZA", "XZ", "ZZ"
    }

#Ruta de Log
LOG_PATH = BASE_DIR / "logs" / "operations.log"

PROCESSED_DATASETS = {
    "IADIZA": {
        "path": BASE_DIR / "processed_datasets" / "IADIZA" / "IADIZA_processed.csv",
        "separator": "\t"
    },

    "Inaturalist": {
        "path": BASE_DIR / "processed_datasets" / "Inaturalist" / "Inaturalist_processed.csv",
        "separator": ","
    },

    "XenoCanto": {
        "path": BASE_DIR / "processed_datasets" / "XenoCanto" / "XenoCanto_processed.csv",
        "separator": ","
    }
}