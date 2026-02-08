import streamlit as st
import pandas as pd
import os
from datetime import datetime

ARCHIVO_EXCEL = "registros_ficha_con_combos.xlsx"

st.set_page_config(page_title="Ficha con combos por actividad", layout="wide")

# Login simple
USUARIOS = {"admin":"1234", "usuario1":"abcd"}

def login():
    st.markdown("<h2 style='text-align:center;'>🔐 Ingreso al Sistema</h2>", unsafe_allow_html=True)
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            st.session_state["login"] = True
            st.session_state["usuario"] = usuario
            st.success(f"Bienvenido {usuario} ✅")
        else:
            st.error("Usuario o contraseña incorrectos ❌")

if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
else:
    st.title("Ficha de Ingreso con combos por actividad")

    # Datos generales
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        ut = st.selectbox("UT", ["", "UT-LIMA", "UT-LIMA PROV", "UT-CALLAO"])
    with col2:
        fecha = st.date_input("Fecha", max_value=datetime.today())
    with col3:
        codigo_usuario = st.text_input("Código de Usuario")
    with col4:
        nombres = st.text_input("Apellidos y Nombres")
    with col5:
        cargo = st.selectbox("Cargo/Puesto", ["", "Supervisor", "Coordinador", "Asistente", "Otro"])

    st.markdown("---")

    # Actividades y combos
    actividades = [
        "ACTIVIDAD VISITAS 1",
        "ACTIVIDAD VISITAS 2",
        "ACTIVIDAD PAGO RBU",
        "ACTIVIDAD MUNICIPALIDAD",
        "ACTIVIDAD GABINETE",
        "ACTIVIDAD BIENESTAR",
        "ACTIVIDAD CAMPAÑAS",
        "ACTIVIDAD REUNIONES"
    ]
    opciones = ["", "SI", "NO", "No corresponde"]

    # Crear columnas para actividades + 1 para otras actividades
    cols = st.columns(len(actividades) + 1)

    # Diccionario para almacenar respuestas
    respuestas = {}

    # Mostrar selectboxes para cada actividad en columnas
    for i, act in enumerate(actividades):
        with cols[i]:
            respuestas[act] = st.selectbox(act, opciones, key=f"res_{i}")

    # Última columna para "Otras actividades"
    with cols[-1]:
        otras = st.text_area("OTRAS ACTIVIDADES", height=100)

    # Guardar botón
    if st.button("💾 Guardar registro"):
        # Validar campos obligatorios
        if not ut or not codigo_usuario or not nombres or not cargo:
            st.warning("⚠️ Complete todos los datos generales antes de guardar.")
        else:
            registro = {
                "UT": ut,
                "Fecha": fecha.strftime("%d/%m/%Y"),
                "Código de Usuario": codigo_usuario,
                "Apellidos y Nombres": nombres,
                "Cargo/Puesto": cargo,
                "Otras Actividades": otras
            }
            # Agregar actividades y sus respuestas
            for act in actividades:
                registro[act] = respuestas.get(act, "")

            # Guardar en Excel
            df_nuevo = pd.DataFrame([registro])
            if os.path.exists(ARCHIVO_EXCEL):
                df_existente = pd.read_excel(ARCHIVO_EXCEL)
                df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
            else:
                df_final = df_nuevo
            df_final.to_excel(ARCHIVO_EXCEL, index=False)
            st.success("✅ Registro guardado correctamente")
            st.dataframe(df_nuevo)
