import sys
from pathlib import Path

# Agrega la carpeta 'src' a su mapa de búsqueda de módulos
ruta_src = str(Path(__file__).resolve().parent.parent)

if ruta_src not in sys.path:
    sys.path.append(ruta_src)

import streamlit as st
from components.barra_lateral import renderizar_barra_lateral

st.set_page_config(page_title="Aplicacion Biodiversidad grupo 47")
st.title("Aplicacion Biodiversidad - Grupo 47")
st.subheader("Bienvenido a la aplicacion de Biodiversidad")

st.divider()
st.header("Propósito de la Aplicación")
st.write("""
El objetivo principal de esta herramienta es centralizar, validar y explorar de forma interactiva grandes conjuntos de datos sobre especies.

**¿Por qué es importante?**
El análisis de datos de biodiversidad es vital para comprender cómo se distribuyen las especies en el planeta, evaluar el impacto ambiental a lo largo del tiempo y tomar decisiones fundamentadas para la conservación y protección de los ecosistemas.
""")
st.divider()

st.header("Estándar Darwin Core (DwC)")
st.write("""
**¿Qué es?**  
Es un estándar de datos, básicamente un glosario de términos comunes mantenido por la organización internacional de estándares de biodiversidad.

**¿Para qué se utiliza?**  
Sirve como un "idioma universal" para compartir información biológica. Al establecer nombres de columnas y formatos estrictos, permite que científicos, museos e instituciones de todo el mundo puedan cruzar e integrar sus investigaciones sin problemas de compatibilidad.
""")

st.divider()
st.header("Instrucciones de Uso")
st.info("""
**Navegación:**  
Utilice el menú lateral ubicado a la izquierda de la pantalla para desplazarse por las distintas secciones.

**¿Qué información podrá consultar?**      
* **Estado del sistema:** Muestra un registro histórico (logs) de las operaciones realizadas sobre los datasets.
* **Búsqueda:** *Permite localizar registros específicos a partir de criterios combinables. Incluye vista de tablas paginadas, exportación a CSV y acceso a la 
                **Ficha de Datos** interactiva con mapas y contenido multimedia.*  
* **Visualización:** *Presenta de forma gráfica la distribución y características de los datos mediante dashboards y reportes estadísticos*
* **Gestión de Registros:** Interfaz transaccional que permite realizar operaciones de inserción, actualización y eliminación de registros directamente desde la aplicación.
* **Exploración de Datasets:** Ofrece una vista general de todos los datasets disponibles en el sistema, permitiendo comparar su completitud, peso en disco y leer la documentación generada.
        """)

# Llamo a la funcion para dibujar el selector (Punto 1.B)
renderizar_barra_lateral()