import streamlit as st
import pandas as pd
from datetime import date, datetime
from web.barra_lateral import renderizar_barra_lateral
from web.carga_datasets import cargar_dataset_procesado
from core.ejercicio4_insercion_registros import insertar_registro_desde_diccionario
from core.ejercicio5_actualizacion_registros import buscar_registros
from core.ejercicio5_actualizacion_registros import actualizar_multiples_campos_validado
from core.ejercicio6_eliminacion_registros import eliminar_por_id
from core.ejercicio6_eliminacion_registros import eliminar_por_lista_suministrada
from core.ejercicio6_eliminacion_registros import eliminar_por_condicion

st.set_page_config(page_title="Gestión de registros")
st.title("Gestión de registros")

renderizar_barra_lateral()

dataset_seleccionado = st.session_state["dataset_actual"]

try:
    datos = cargar_dataset_procesado(dataset_seleccionado)
    st.info(f" Dataset: **{dataset_seleccionado}** - {len(datos)} registros")

    # EJERCICIO 4.A - Formulario de inserción
    # ============================================
    st.header("Insertar nuevo registro")

    # Mostrar nombres de columnas según el dataset 
    with st.expander("Ver columnas"):
        st.write(list(datos.columns))

    if dataset_seleccionado == "XenoCanto":
        nombre_columna_latitud = "latitudeDecimal"
        nombre_columna_longitud = "longitudeDecimal"
        nombre_columna_pais = "country"
        pais_es_codigo = False
    else:
        nombre_columna_latitud = "decimalLatitude"
        nombre_columna_longitud = "decimalLongitude"
        nombre_columna_pais = "countryCode"
        pais_es_codigo = True

    # Formulario
    with st.form("formulario_insercion"):
        nombre_cientifico = st.text_input("Nombre científico")
        latitud = st.number_input("Latitud", value=0.0, step=0.0001, format="%.6f")
        longitud = st.number_input("Longitud", value=0.0, step=0.0001, format="%.6f")
        fecha_evento = st.date_input("Fecha del evento")
        
        if pais_es_codigo:
            pais = st.text_input("Código de país (ej: AR)")
        else:
            pais = st.text_input("País")
        
        boton_guardar = st.form_submit_button("Guardar registro")
        
        if boton_guardar:
            # Armar el diccionario con los datos del formulario
            nuevo_registro = {
                "scientificName": nombre_cientifico if nombre_cientifico else None,
                nombre_columna_latitud: latitud,
                nombre_columna_longitud: longitud,
                "eventDate": str(fecha_evento),
                nombre_columna_pais: pais.upper() if pais_es_codigo and pais else pais,
            }
            
            exito, mensaje = insertar_registro_desde_diccionario(dataset_seleccionado, nuevo_registro)
            
            if exito:
                st.success(f" {mensaje}")
            else:
                st.error(f"{mensaje}")

    # EJERCICIO 4.B - Búsqueda por identificador
    # ============================================
    
    st.header("Buscar registro para editar")
    
    # Seleccionar ID según el dataset
    if dataset_seleccionado == "IADIZA":
        columna_id = "occurrenceID"
        ejemplo_id = "IADIZA:COI:006861"
    elif dataset_seleccionado == "Inaturalist":
        columna_id = "id"
        ejemplo_id = "17063"
    else:  # XenoCanto
        columna_id = "id"
        ejemplo_id = "999540@XC"
    
    st.caption(f"Búsqueda en la columna **{columna_id}** (ejemplo: `{ejemplo_id}`)")
    
    id_buscar = st.text_input(f"Ingresá el {columna_id} del registro que querés editar:")
    
    if st.button("Buscar registro", key="boton_buscar"):
        if id_buscar:
            # Buscar el registro usando la función de la Parte 1
            filtros = {columna_id: id_buscar}
            resultados = buscar_registros(dataset_seleccionado, filtros)
            
            if resultados and len(resultados) > 0:
                st.success(f"Registro encontrado")
                # Guardamos el registro encontrado en session_state
                st.session_state["registro_a_editar"] = resultados[0]
                
                with st.expander("Ver registro completo"):
                    st.json(resultados[0])
            else:
                st.error(f"No se encontró ningún registro con {columna_id} = '{id_buscar}'")
                if "registro_a_editar" in st.session_state:
                    del st.session_state["registro_a_editar"]
        else:
            st.warning("Por favor, ingresá un ID")
    
    # EJERCICIO 4.C - Formulario de edición
    # ============================================
    if "mensaje_exito" in st.session_state:
        st.success(st.session_state["mensaje_exito"])
        if "campos_modificados" in st.session_state:
            st.info("Campos modificados")
            for campo, (viejo, nuevo) in st.session_state["campos_modificados"].items():
                st.write(f"- **{campo}**: '{viejo}' -> '{nuevo}'")
            del st.session_state["campos_modificados"]
        del st.session_state["mensaje_exito"]
        
    st.header("Editar Registro")
    
    #chequeamos si hay algún registro guardado del punto anterior
    if "registro_a_editar" in st.session_state: 
        registro = st.session_state["registro_a_editar"]
    
        st.success(f"Editar Registro con {columna_id}={registro.get(columna_id, '')}")

        with st.form("formulario_edicion"):
            st.subheader("Modificá los datos del Registro")

            #Obtenemos los valores actuales del registro
            nombre_actual= registro.get("scientificName", "")
        
            # Latitud y Longitud
            try:
                latitud_actual = float(registro.get(nombre_columna_latitud, 0.0))
            except (ValueError, TypeError):
                latitud_actual=0.0
        
            try:
                longitud_actual= float(registro.get(nombre_columna_longitud, "0.0"))
            except(ValueError,TypeError):
                longitud_actual= 0.0
            
            #Fecha
            fecha_actual= registro.get("eventDate", "")

            if fecha_actual and isinstance(fecha_actual, str):
                try:
                    fecha_actual= datetime.strptime(fecha_actual, "%Y-%m-%d").date()
                except(ValueError):
                    fecha_actual=date.today()
            elif not fecha_actual: 
                fecha_actual = date.today()
            
            #Pais
            pais_actual = registro.get(nombre_columna_pais,"")
            
            #Para poder Editarlos
            nombre_nuevo = st.text_input("Nombre Cientifico", value= nombre_actual)

            latitud_nueva = st.number_input("Latitud", value=latitud_actual, step =0.0001,format="%.6f")
            longitud_nueva = st.number_input ("Longitud", value=longitud_actual, step=0.001, format ="%.6f")

            fecha_nueva= st.date_input("Fecha del Evento", value=fecha_actual)
            
            if pais_es_codigo:
                pais_nuevo= st.text_input("Codigo de País", value=pais_actual)
            else:
                pais_nuevo= st.text_input("País", value=pais_actual)
            
            boton_actualizar= st.form_submit_button("Actualizar Registro")

            if boton_actualizar:
                #Armamos diccionario para usar en la función
                cambios={}

                if nombre_nuevo != nombre_actual:
                    cambios["scientificName"]=nombre_nuevo

                if latitud_nueva != latitud_actual:
                    cambios[nombre_columna_latitud]=latitud_nueva
                if longitud_nueva != longitud_actual:
                    cambios[nombre_columna_longitud]=longitud_nueva 
                
                if fecha_nueva!= fecha_actual:
                    cambios["eventDate"]=str(fecha_nueva)

                if pais_nuevo!= pais_actual:
                    if pais_es_codigo:
                        cambios[nombre_columna_pais]=pais_nuevo.upper()
                    else:
                        cambios[nombre_columna_pais]=pais_nuevo
                
                if not cambios:
                    st.warning("No hiciste ningún cambio")
                else:
                    # FUNCIÓN DE ACTUALIZACIÓN
                    exito, mensaje = actualizar_multiples_campos_validado(
                        dataset_seleccionado,
                        columna_id,
                        str(registro.get(columna_id, "")),
                        cambios
                    )
                    
                    if exito:
                        st.session_state["mensaje_exito"] = mensaje
                        st.session_state["campos_modificados"] = {campo: (registro.get(campo, ""), valor_nuevo) for campo, valor_nuevo in cambios.items()}
                        # Limpiar el registro guardado y recargar
                        del st.session_state["registro_a_editar"]
                        st.rerun()
                    else:
                        st.error(f"{mensaje}")

    # EJERCICIO 4.D - Eliminación de registros
    # ============================================
    st.header("Eliminación de Registros")

    # Mostrar mensaje de éxito si existe (después de recargar)
    if "mensaje_eliminacion" in st.session_state:
        st.success(st.session_state["mensaje_eliminacion"])
        del st.session_state["mensaje_eliminacion"]

    #separamos por modalidad
    tab1,tab2,tab3 = st.tabs(["Por ID Único", "Por Valor de Columna", "Por Condición"])

    # ---------- TAB 1: Por ID único ----------
    with tab1:
        st.subheader("Eliminar un Registro por su Identificador Único")

        if dataset_seleccionado == "IADIZA":
            columna_id_eliminar = "occurrenceID"
        else:
            columna_id_eliminar = "id"
        
        st.caption(f"Elimar de la columna: **{columna_id_eliminar}**")

        id_a_eliminar = st.text_input(f"Ingresá el {columna_id_eliminar} a Eliminar:", key = "id_eliminar")

        if st.button("Ver Registro a Eliminar", key= "ver_id"):
            if id_a_eliminar:
                filtros = {columna_id_eliminar:id_a_eliminar}
                resultados = buscar_registros (dataset_seleccionado,filtros)

                if resultados:
                    st.session_state["registro_a_eliminar_id"] = resultados[0]
                    st.session_state["id_a_eliminar_confirmar"] = id_a_eliminar
                    st.rerun()
                else:
                    st.error(f"No se encontró ningún registro con {columna_id_eliminar} = '{id_a_eliminar}'")
            else:
                st.warning("Ingresá un ID")

        if "registro_a_eliminar_id" in st.session_state:
            st.warning("Se va a eliminar este registro:")
            with st.expander("Ver registro a eliminar"):
                st.json(st.session_state["registro_a_eliminar_id"])
    
            if st.button("Confirmar eliminación", key="confirmar_id"):
                resultado = eliminar_por_id(dataset_seleccionado, st.session_state["id_a_eliminar_confirmar"], columna_id_eliminar)
                st.session_state["mensaje_eliminacion"] = resultado
                del st.session_state["registro_a_eliminar_id"]
                del st.session_state["id_a_eliminar_confirmar"]
                st.rerun()
    
    # ---------- TAB 2: Por valor de columna ----------
    with tab2:
        st.subheader("Eliminar por Valor de una Columna")

        columna_eliminar= st.selectbox(
            "Seleccioná la Columna:", 
            options= list(datos.columns),
            key= "col_eliminar")
        
        if columna_eliminar:
            valores_unicos= datos[columna_eliminar].dropna().unique().tolist()
            valores_a_eliminar= st.multiselect(
                f"Seleccioná los Valores a Eliminar de {columna_eliminar}",
                options= valores_unicos,
                key= "valores_eliminar"  )
            
            if valores_a_eliminar:
                #los mostramos
                registros_afectados= datos[datos[columna_eliminar].isin(valores_a_eliminar)]
                st.warning(f"Se eliminarán **{len(registros_afectados)}** registros")

                with st.expander(f"ver {len(registros_afectados)} registros a eliminar"):
                    st.dataframe(registros_afectados)
                
                if st.button("Confirmar Eliminación Por Valores", key= "confirmar_valores"):
                    resultado= eliminar_por_lista_suministrada(
                        dataset_seleccionado,
                        valores_a_eliminar,
                        columna_eliminar
                    )
                    st.session_state["mensaje_eliminacion"] = resultado
                    st.rerun()
            else:
                st.info("Seleccioná uno o más valores para eliminar")

    # ---------- TAB 3: Por condición ----------
    with tab3:
        st.subheader("Eliminar Registros que cumplan una Condición")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            columna_condicion = st.selectbox(
                "Columna:",
                options=list(datos.columns),
                key="col_cond"
            )
        
        with col2:
            operador = st.selectbox(
                "Operador:",
                options=["==", "!=", ">", ">=", "<", "<="],
                key="operador"
            )
        
        with col3:
            valor_condicion = st.text_input("Valor a comparar:", key="valor_cond")

        if columna_condicion and valor_condicion and operador:
            try:
                try:
                    valor_comparacion = float(valor_condicion)
                except ValueError:
                    valor_comparacion = valor_condicion
                
                # Aplicar operador
                if operador == "==":
                    cumple = datos[columna_condicion].astype(str) == str(valor_comparacion)
                elif operador == "!=":
                    cumple = datos[columna_condicion].astype(str) != str(valor_comparacion)
                elif operador == ">":
                    cumple = pd.to_numeric(datos[columna_condicion], errors='coerce') > valor_comparacion
                elif operador == ">=":
                    cumple = pd.to_numeric(datos[columna_condicion], errors='coerce') >= valor_comparacion
                elif operador == "<":
                    cumple = pd.to_numeric(datos[columna_condicion], errors='coerce') < valor_comparacion
                elif operador == "<=":
                    cumple = pd.to_numeric(datos[columna_condicion], errors='coerce') <= valor_comparacion
                else:
                    cumple = pd.Series([False] * len(datos))
                
                registros_afectados = datos[cumple]
                
                if len(registros_afectados) > 0:
                    st.warning(f"Se van a eliminar **{len(registros_afectados)}** Registros")
                    
                    with st.expander(f"Ver {len(registros_afectados)} Registros a Eliminar"):
                        st.dataframe(registros_afectados)
                    
                    if st.button("Confirmar Eliminación Por Condición", key="confirmar_cond"):
                        resultado = eliminar_por_condicion(
                            dataset_seleccionado,
                            valor_condicion,
                            columna_condicion,
                            operador
                        )
                        st.session_state["mensaje_eliminacion"] = resultado
                        st.rerun()
                else:
                    st.warning("No hay registros que cumplan esa condición")
                    
            except Exception as e:
                st.error(f"Error al evaluar la condición: {e}")
        else:
            st.info("Completá la columna, operador y valor para la vista previa")
            
except Exception as error:
    st.error(f"Error al cargar el dataset '{dataset_seleccionado}': {error}")