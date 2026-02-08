import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================
ARCHIVO_EXCEL = "registros_monitoreo.xlsx"
st.set_page_config(page_title="Ficha de Monitoreo", layout="wide")

# =========================
# USUARIOS Y CONTRASEÑAS (Ejemplo) 
# =========================
USUARIOS = {
    "admin": "1234",
    "usuario1": "abcd"
}

# =========================
# FUNCION LOGIN
# =========================
def login():
    st.markdown("<h2 style='text-align:center;'>🔐 Ingreso al Sistema de Monitoreo</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            st.session_state["login"] = True
            st.session_state["usuario"] = usuario
            st.success(f"Bienvenido {usuario} ✅")
        else:
            st.error("Usuario o contraseña incorrectos ❌")

# =========================
# SESIÓN DE LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
else:
    # =========================
    # CSS GLOBAL
    # =========================
    st.markdown("""
    <style>
    .stApp { background-color: #f4f6f9; }
    .cinta {
        background: linear-gradient(90deg, #1f77b4, #4fa3d1);
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: 600;
        color: white;
        margin: 15px 0;
    }
    .tarjeta {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }
    input, textarea { border-radius: 6px !important; }
    div[data-baseweb="select"] > div { border-radius: 6px; }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }
    .stButton > button:hover { background-color: #155a8a; transform: scale(1.02); }
    thead tr th { background-color: #1f77b4 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # FUNCIONES
    # =========================
    def titulo_cinta(texto):
        st.markdown(f"<div class='cinta'>{texto}</div>", unsafe_allow_html=True)

    # =========================
    # TÍTULO PRINCIPAL
    # =========================
    st.markdown("""
    <h1 style="text-align: center; color: #1f77b4; font-weight: 700;">
    📋 Ficha de Monitoreo a la gestión de la entrega de la pensión no contributiva
    </h1>
    """, unsafe_allow_html=True)
    st.divider()

    # =========================
    # DATOS GENERALES
    # =========================
    titulo_cinta("Datos Generales")
    with st.container():
        st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            unidad = st.selectbox(
                "Unidad(es) Orgánica(s)", ["", "UT-LIMA", "UT-LIMA PROV", "UT-CALLAO"]
            )
        with col2:
            fecha_supervision = st.date_input("Fecha(s) de Supervisión", max_value=datetime.today())

        nombre = st.text_input("Apellidos y Nombres del entrevistado")
        dni = st.text_input("DNI")
        cargo = st.text_input("Cargo")

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # ACTIVIDADES
    # =========================
    titulo_cinta("Actividades y Resultados")

    actividades = [
        ("Proceso de Afiliación", [
            "A- Se elaboró el informe con la propuesta del cronograma anual",
            "B- Se solicitó a la ONP la relación de no pensionistas en condición de pobreza",
            "C- Se solicitó a UTI la generación de los archivos de cotejo"
        ]),
        ("Cotejos y Pre Padrón", [
            "D- Se solicitó a las entidades externas la información para el cotejo masivo",
            "E- Se solicitó al OFIS el PGH (RIS) con información actualizada",
            "F- Se recibió la respuesta de las entidades externas",
            "G- Se cargaron los cotejos recibidos",
            "H- Se cargó el preliminar del pre padrón"
        ]),
        ("Apertura de Cuentas y RBU", [
            "I- Se gestionó la apertura de cuentas",
            "J- Se emitió el informe de solicitud de terceros autorizados",
            "K- Se revisaron expedientes de vulnerabilidad adicional",
            "L- Se remitió relación de usuarios sin movimiento",
            "M- Se generó y cargó el PRE PADRON",
            "N- Se informó el término del proceso del PRE PADRON",
            "O- Se remitió correo de validación del PRE PADRON",
            "P- Se cargó la versión final del pre padrón"
        ]),
        ("Cierre y Reportes", [
            "Q- Se cargó lista de fallecidos",
            "R- Se generó lista previa a la RBU",
            "S- Se registró la propuesta de RBU",
            "T- Se confirmó revisión final del padrón",
            "U- Se remitió memorando del proceso",
            "V- Se emitió informe técnico final"
        ])
    ]

    respuestas = []

    for seccion, acts in actividades:
        with st.expander(seccion, expanded=True):
            for i, act in enumerate(acts):
                with st.container():
                    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([6, 2, 4])
                    with col1:
                        st.write(act)
                    with col2:
                        resultado = st.selectbox(
                            "Resultado", ["", "SI", "NO", "No corresponde"], key=f"res_{seccion}_{i}"
                        )
                    with col3:
                        observacion = st.text_input(
                            "Observación", key=f"obs_{seccion}_{i}"
                        )

                    respuestas.append({
                        "Actividad": act,
                        "Resultado": resultado,
                        "Observacion": observacion
                    })

                    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # GUARDAR INFORMACIÓN
    # =========================
    titulo_cinta("Guardar Información")
    if st.button("💾 Guardar información"):
        # Validación básica
        if not unidad or not nombre or not dni or not cargo:
            st.warning("⚠️ Complete todos los datos generales.")
        else:
            filas = []
            for r in respuestas:
                filas.append({
                    "ID Registro": f"{dni}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "Fecha Registro": datetime.now(),
                    "Unidad Organica": unidad,
                    "Fecha Supervision": fecha_supervision.strftime("%d/%m/%Y"),
                    "Entrevistado": nombre,
                    "DNI": dni,
                    "Cargo": cargo,
                    "Actividad": r["Actividad"],
                    "Resultado": r["Resultado"],
                    "Observacion": r["Observacion"]
                })

            df_nuevo = pd.DataFrame(filas)

            if os.path.exists(ARCHIVO_EXCEL):
                df_existente = pd.read_excel(ARCHIVO_EXCEL)
                d
