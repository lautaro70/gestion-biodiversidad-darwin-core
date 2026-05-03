# Proyecto de Gestión de Biodiversidad - Grupo 47

Este proyecto es una herramienta diseñada para la gestión, validación y exploración de datos biológicos utilizando el estándar **Darwin Core (DwC)**. Permite procesar datasets y visualizar logs de operaciones a través de una interfaz interactiva.

## Integrantes
* **Bellocq Catalina**
* **Bof Máximo Dante**
* **Mascetti Augusto**
* **Penetta Lautaro**
* **Suarez Franco**

## Configuración del Entorno

Para asegurar que el software funcione correctamente en Windows, Linux o Mac, siga estos pasos para configurar el entorno virtual e instalar las dependencias.

### Requisitos del Sistema
Para asegurar la compatibilidad, este proyecto fue desarrollado y testeado bajo las siguientes versiones:
* **Python**: 3.13.12
* **Streamlit**: 1.57.0
* **Jupyter**: para la ejecución de los notebooks en 'src/notebooks/'.

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