# Proyecto de Gestión de Biodiversidad - Grupo 47

Este proyecto es una herramienta diseñada para la gestión, validación y exploración de datos biológicos utilizando el estándar **Darwin Core (DwC)**. Permite procesar datasets y visualizar logs de operaciones a través de una interfaz interactiva.

## Integrantes
* **Bellocq Catalina**
* **Bof Máximo Dante**
* **Mascetti Augusto**
* **Pennetta Lautaro**
* **Suarez Franco**

## Configuración del Entorno
Para asegurar que el software funcione correctamente en Windows, Linux o Mac, siga estos pasos para configurar el entorno virtual e instalar las dependencias.

### Requisitos del Sistema
Para asegurar la compatibilidad, este proyecto fue desarrollado y testeado bajo las siguientes versiones:
* **Python**: 3.13.12
* **Streamlit**: 1.57.0
* **Jupyter**: para la ejecución de los notebooks en 'src/notebooks/'.

### Preparación de los Datos
Para que el procesamiento de los Notebooks y la aplicación funcionen correctamente, debe preparar los archivos de datos siguiendo estos pasos:

1. **Ubicación**: Coloque los datasets originales dentro de la carpeta `raw_datasets/`.
2. **Descompresión**: Si los archivos se encuentran en formato `.zip`, descomprímalos en dicha carpeta.
3. **Renombrado y Estructura**: Para que las rutas del sistema localicen los datos, las carpetas dentro de `raw_datasets/` deben mantener la siguiente estructura y nombres exactos (respetando mayúsculas):
    * **IADIZA**: `raw_datasets/IADIZA-CONICET/IADIZA-CONICET/` (Debe contener `occurrence.txt`).
   * **iNaturalist**: `raw_datasets/Inaturalist/Inaturalist/` (Debe contener `observations.csv`).
   * **Xeno-Canto**: `raw_datasets/XenoCanto/XenoCanto/` (Debe contener `Occurrence.txt` -> *la O mayúscula).

*Nota: Se recomienda verificar que los nombres de los archivos internos coincidan exactamente con los mencionados, ya que el sistema es sensible a mayúsculas y minúsculas (Case Sensitive).*

### Creación del entorno virtual (Virtualenv)
Desde la carpeta raíz del proyecto (`code/`), ejecute:

**Windows:**
Bash
python -m venv .venv

**Linux/Mac:**
python3 -m venv .venv

### Activación del entorno
**Windows:**
Bash
.venv\Scripts\activate

**Linux/Mac:**
source .venv/bin/activate

### Instalación de dependencias
Con el entorno activado, instale las bibliotecas necesarias detalladas en el archivo requirements.txt:

Bash
pip install -r requirements.txt

### Instrucciones de Ejecución
Ejercicio de Procesamiento (Notebooks):
Para ejecutar y visualizar los análisis preliminares y validaciones, puede abrir los archivos .ipynb ubicados en src/notebooks/ utilizando VS Code o Jupyter Notebook.

**Ejemplo de uso:**

1-Abrí VS Code.

2-Selecciona el archivo src/notebooks/ejercicio_3.ipynb.

3-Asegúrese de seleccionar el kernel del entorno virtual .venv creado anteriormente.

4-Ejecute todas las celdas para ver el procesamiento de datos (Inicie con la primera).

### Aplicación Interactiva (Streamlit)
La aplicación web centraliza todas las funcionalidades en una interfaz gráfica. Para iniciarla, ejecute el siguiente comando desde la raíz del proyecto:

Bash
streamlit run src/Inicio.py

Una vez ejecutado, se abrirá automáticamente una pestaña en su navegador (generalmente en http://localhost:8501) donde podrá navegar por las páginas de:

**Inicio: Información del proyecto y Darwin Core.**
**Estado del sistema: Visualización de los logs de logs/operations.log.**

### Estructura del Proyecto:
* **documentation/**: Análisis y descripción de los datasets originales (Ejercicio 1).
* **raw_datasets/**: Almacenamiento de los archivos .csv originales.
* **processed_datasets/**: Datos validados y procesados por el sistema.
* **logs/**: Registros de operaciones del sistema.
* **src/**: Código fuente del proyecto.
    * **Inicio.py**: Página principal de la aplicación Streamlit.
    * **pages/**: Páginas secundarias (Estado del sistema, Búsqueda, Visualización).
    * **core/**: Lógica de procesamiento y validaciones.
    * **common/**: Funciones auxiliares y constantes.
    * **notebooks/**: Desarrollo y pruebas de los ejercicios en formato .ipynb.
* **requirements.txt**: Lista de bibliotecas necesarias para el proyecto.

### Configuración Centralizada y Rutas (DRY)

Para evitar la repetición de código y asegurar la consistencia en todo el proyecto (Notebooks y Aplicación), se utiliza un archivo de configuración centralizado ubicado en `src/common/constants.py`.

### Constantes Globales y Estructura Restrictiva
El sistema se rige por las siguientes definiciones constantes que **deben respetarse** para el correcto funcionamiento:

* **BASE_DIR**: Se calcula dinámicamente usando `pathlib`, garantizando que las rutas funcionen de forma relativa a la raíz del proyecto en cualquier sistema operativo.
* **LOG_PATH**: logs/operations.log — Ubicación única para el registro de auditoría del sistema, se crea automático al ejecutar la celda que inicializa el archivo.
* **DATASETS**: Diccionario que centraliza la ubicación y el formato de los datos:
    * **IADIZA**: Ruta: `raw_datasets/IADIZA-CONICET/IADIZA-CONICET/occurrence.txt` | Separador: `\t` (Tabulación).
    * **Inaturalist**: Ruta: `raw_datasets/Inaturalist/Inaturalist/observations.csv` | Separador: `,` (Coma).
    * **XenoCanto**: Ruta: `raw_datasets/XenoCanto/XenoCanto/Occurrence.txt` | Separador: `,` (Coma).

### Uso Transversal
Cualquier módulo que necesite acceder a los datos (como `src/pages/2_Estado_del_sistema.py` o los notebooks) utiliza la función `obtener_ruta_y_separador(dataset)` definida en `src/common/functions.py`, la cual importa directamente estas constantes. Esto asegura que un cambio en la estructura de carpetas solo deba modificarse en un único lugar.