import streamlit as st
import pandas as pd
from common.dataset_utils import leer_logs
from web.barra_lateral import renderizar_barra_lateral

# Llamo a la funcion para que el selector quede guardado (Punto 1.B)
renderizar_barra_lateral()

st.set_page_config(page_title="Estado del sistema")
st.title("Estado del sistema")
st.write("los logs se mostraran a continuación")

try:
    # Intentamos abrir y leer el archivo directamente
    datos_log = leer_logs()
    # Si lo pudimos leer, verificamos que no esté vacío para mostrarlo
    if len(datos_log) > 1: # > 1 porque la primer fila es el encabezado
        # hacemos que las filas tengan el formato ("fecha | tipo | detalle")
        registros = []
        for fila in datos_log[1:]:  # Saltar encabezado
            if fila and len(fila) > 0:
                partes = fila[0].split(" | ") # .split(" | ") separa en 3 partes
                if len(partes) == 3:
                    registros.append({
                        "Fecha_Hora": partes[0],
                        "Tipo": partes[1],
                        "Detalle": partes[2]
                    })
        #convertimos a datframe de pandas
        df_logs = pd.DataFrame(registros)
        df_logs['Fecha_Hora'] = pd.to_datetime(df_logs['Fecha_Hora'])

        # Métricas(Ejercicio 4.E)
        # ============================================
        st.subheader("Métricas")

        col_met1, col_met2, col_met3, col_met4 = st.columns(4)

        with col_met1:
            st.metric("Inserciones", len(df_logs[df_logs['Tipo'] == 'INSERT']))
        with col_met2:
            st.metric("Operaciones", len(df_logs[df_logs['Tipo'] == 'INFO']))
        with col_met3:
            st.metric("Eliminaciones", len(df_logs[df_logs['Tipo'] == 'DELETE']))
        with col_met4:
            st.metric("Errores", len(df_logs[df_logs['Tipo'] == 'ERROR']))

        # Filtros (Ejercicio 4.E)
        # ============================================
        st.subheader("Filtros")

        col1, col2 = st.columns(2)

        with col1:
            tipos_disponibles = df_logs['Tipo'].unique().tolist() # Obtenemos los valores únicos de la columna 'Tipo'
            tipos_seleccionados = st.multiselect( #multiselect para poder seleccionar + de 1
                "Filtrar por tipo de operación:",
                options=tipos_disponibles,
                default=[]
            )

        with col2:
            fecha_min = df_logs['Fecha_Hora'].min().date() #fecha más antigua del log
            fecha_max = df_logs['Fecha_Hora'].max().date() #fecha más reciente del log
            rango_fechas = st.date_input( # con date_input podemos elegir un rango de fechas (desde - hasta)
                "Filtrar por rango de fechas:",
                value=(fecha_min, fecha_max),
                min_value=fecha_min,
                max_value=fecha_max
            )

        # Aplicar filtros
        if tipos_seleccionados:
            df_filtrado = df_logs[df_logs['Tipo'].isin(tipos_seleccionados)] #si se elegió un tipo filtramos por ese tipo
        else:
            df_filtrado = df_logs.copy() #si no se elegiió nada usamos todos los registros y .copy() crea una copia para no modificar el original

        if len(rango_fechas) == 2:
            fecha_inicio, fecha_fin = rango_fechas
            df_filtrado = df_filtrado[ # filtramos las filas que están dentro del rango de fechas
                (df_filtrado['Fecha_Hora'].dt.date >= fecha_inicio) &
                (df_filtrado['Fecha_Hora'].dt.date <= fecha_fin)
            ]

        # Tabla de Logs
        # ============================================
        st.subheader(f"Logs ({len(df_filtrado)} registros)")
        st.dataframe(df_filtrado)

    else:
        st.info("El archivo de logs se encuentra vacío. Aún no hay operaciones registradas.")

except FileNotFoundError:
    st.warning("Aún no se han registrado operaciones en el sistema (archivo 'logs/operations.log' no encontrado).")
except PermissionError:
    st.error("Error de permisos: No se tiene acceso de lectura al archivo de logs.")
except Exception as e:
    #Para cualquier otro error inesperado (ej. archivo corrupto)
    st.error(f"Ocurrió un error crítico e inesperado al intentar leer los logs: {e}")