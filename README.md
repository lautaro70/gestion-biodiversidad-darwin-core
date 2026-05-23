# Proyecto de Gestión de Biodiversidad - Grupo 47

## Integrantes
* **Bellocq Catalina**
* **Bof Máximo Dante**
* **Mascetti Augusto**
* **Pennetta Lautaro**
* **Suarez Franco**

Este proyecto es una herramienta diseñada para la gestión, validación y exploración de datos biológicos utilizando el estándar **Darwin Core (DwC)**. Permite procesar datasets y visualizar logs de operaciones a través de una interfaz interactiva.

El objetivo principal es resolver los problemas típicos de los datos provenientes del mundo real (registros corruptos, coordenadas fuera de rango, fechas inconsistentes y datos taxonómicos incompletos) mediante un procesamiento por lotes eficiente que cuida el consumo de memoria RAM. La herramienta implementa:
*   **Lectura y Análisis Estructural**: Exploración agnóstica de archivos del dataset (`.txt` y `.csv`) calculando métricas de completitud sin sobrecargar el sistema.
*   **Validación Crítica de Calidad**: Control estricto de coordenadas geográficas globales y cotas regionales específicas para América del Sur, detección de duplicados e inconsistencias temporales.
*   **Persistencia Inmutable**: Los archivos originales en formato crudo nunca se modifican; todas las operaciones de saneamiento generan nuevas versiones limpias orientadas a la producción.
*   **Auditoría (Logging)**: Registro detallado y cronológico de cada transacción para asegurar la trazabilidad del sistema.
*   **Interfaz Interactiva**: Un panel de control web dinámico que expone los reportes estadísticos y el estado transaccional.

## Descarga de Datasets
Para replicar los análisis y ejecutar la plataforma, es necesario descargar los conjuntos de datos oficiales provistos por la cátedra, los cuales corresponden a muestras adaptadas de las siguientes fuentes:

1. **IADIZA**: Registros de ocurrencias biológicas.
2. **Xeno-canto**: Grabaciones y registros de aves.
3. **iNaturalist**: Observaciones de biodiversidad ciudadana[cite: 7].

**Enlace Oficial de Descarga:** 
Todos los datasets comprimidos deben ser descargados de forma obligatoria desde el servidor de la facultad en el siguiente enlace:
https://archivos.linti.unlp.edu.ar/index.php/s/rPG30E5wUwy6Xbo

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

#### Contenido de los Notebooks:
**ejercicio2.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio2_lectura_dataset.py
**ejercicio3.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio3_validaciones.py
**ejercicio4.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio4_insercion_registros.py
**ejercicio5.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio5_actualizacion_registros.py
**ejercicio6.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio6_eliminacion_registros.py
**ejercicio7.ipynb**: Incluye las pruebas de las funciones del archivo ejercicio7_registro_de_operaciones.py

#### Instrucciones detalladas de ejecución:
**Opción A: Desde Visual Studio Code (Recomendado)**
1. Abra VS Code en la carpeta raíz del proyecto (`code/`).
2. Instale la extensión oficial de **Jupyter** en VS Code si aún no la tiene.
3. Navegue en el explorador de archivos y abra `src/notebooks/ejercicio_3.ipynb`.
4. En la esquina superior derecha del editor, haga clic en **Select Kernel** y asegúrese de elegir la ruta del entorno virtual del proyecto (`.venv`).
5. Ejecute las celdas secuencialmente haciendo clic en el botón de "Play" al lado de cada una.

**Opción B: Desde la Terminal clásica**
1. Asegúrese de tener el entorno virtual activado en su terminal.
2. Instale la interfaz ejecutando: `pip install notebook` (solo si no dispone de ella).
3. Inicie el servidor local corriendo: `jupyter notebook`
4. Se abrirá una interfaz en su navegador web. Ingrese a la carpeta `src/notebooks/` y abra el archivo deseado.

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