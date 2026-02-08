import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================
ARCHIVO_EXCEL = "registros_ficha2.xlsx"
st.set_page_config(page_title="Ficha de Actividades UT", layout="wide")

# =========================
# LOGIN SIMPLE
# =========================
USUARIOS = {"admin": "1234", "usuario1": "abcd"}

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
    # =========================
    # CSS
    # =========================
    st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .cinta { background: linear-gradient(90deg, #1f77b4, #4fa3d1); padding: 12px 16px; border-radius: 8px; font-size: 20px; font-weight: 600; color: white; margin: 15px 0; }
    .tarjeta { background-color: white; padding: 16px; border-radius: 12px; box-shadow: 0 3px 8px rgba(0,0,0,0.08); margin-bottom: 12px; }
    input, textarea { border-radius: 6px !important; }
    div[data-baseweb="select"] > div { border-radius: 6px; }
    .stButton > button { background-color: #1f77b4; color: white; font-weight: bold; border-radius: 10px; padding: 10px 20px; border: none; }
    .stButton > button:hover { background-color: #155a8a; transform: scale(1.02); }
    thead tr th { background-color: #1f77b4 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    def titulo_cinta(texto):
        st.markdown(f"<div class='cinta'>{texto}</div>", unsafe_allow_html=True)

    # =========================
    # TÍTULO
    # =========================
    st.markdown("<h1 style='text-align:center;color:#1f77b4;font-weight:700;'>Ficha de Ingreso de Actividades UT</h1>", unsafe_allow_html=True)
    st.divider()

    # =========================
    # DATOS GENERALES
    # =========================
    titulo_cinta("Datos Generales")
    with st.container():
        st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            ut = st.selectbox("Seleccionar UT", ["", "UT-LIMA", "UT-LIMA PROV", "UT-CALLAO"])
        with col2:
            fecha = st.date_input("Fecha", max_value=datetime.today())
        with col3:
            codigo_usuario = st.text_input("Código de Usuario")

        nombres = st.text_input("Apellidos y Nombres")
        cargo = st.selectbox("Cargo/Puesto", ["", "Supervisor", "Coordinador", "Asistente", "Otro"])

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # ACTIVIDADES
    # =========================
    titulo_cinta("Seleccionar Actividades Realizadas")
    actividades = [
        "VISITAS 1", "VISITAS 2", "PAGO RBU", "MUNICIPALIDAD", 
        "GABINETE", "BIENESTAR", "CAMPAÑAS", "REUNIONES"
    ]

    actividades_seleccionadas = st.multiselect("Seleccione una o varias actividades:", actividades)
    otras_actividades = st.text_area("Otras actividades realizadas")

    # =========================
    # GUARDAR INFORMACIÓN
    # =========================
    titulo_cinta("Guardar Información")
    if st.button("💾 Guardar registro"):
        if not ut or not nombres or not codigo_usuario or not cargo:
            st.warning("⚠️ Complete todos los datos generales antes de guardar.")
        else:
            registro = {
                "UT": ut,
                "Fecha": fecha.strftime("%d/%m/%Y"),
                "Código de Usuario": codigo_usuario,
                "Apellidos y Nombres": nombres,
                "Cargo/Puesto": cargo
            }

            # Guardar actividades seleccionadas
            for act in actividades:
                registro[act] = "Sí" if act in actividades_seleccionadas else "No"

            registro["Otras Actividades"] = otras_actividades

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
