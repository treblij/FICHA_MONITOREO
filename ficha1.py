import streamlit as st
import pandas as pd
import os
from datetime import datetime

ARCHIVO_EXCEL = "registros_monitoreo.xlsx"

st.set_page_config(page_title="Ficha de Monitoreo", layout="wide")

# =========================
# FUNCIONES AUXILIARES
# =========================
def titulo_cinta(texto):
    """Muestra un título con fondo celeste tipo 'cinta'."""
    st.markdown(f"""
    <div style="
        background-color: #a0d8f1;
        padding: 10px;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
    ">
    {texto}
    </div>
    """, unsafe_allow_html=True)

# =========================
# TÍTULO PRINCIPAL
# =========================
st.markdown(
    "<h1 style='text-align: center;'>📋 Ficha de Monitoreo a la gestión de la entrega de la pensión no contributiva</h1>",
    unsafe_allow_html=True
)
st.divider()

# =========================
# DATOS GENERALES
# =========================
titulo_cinta("Datos Generales")

col1, col2 = st.columns(2)
with col1:
    unidad = st.selectbox(
        "Unidad(es) Orgánica(s)",
        ["", "UT-LIMA", "UT-LIMA PROV", "UT-CALLAO"],
        index=0
    )
with col2:
    fecha_supervision = st.date_input("Fecha(s) de Supervisión", max_value=datetime.today())

nombre = st.text_input("Apellidos y Nombres del entrevistado")
dni = st.text_input("DNI")
cargo = st.text_input("Cargo")

st.divider()

# =========================
# ACTIVIDADES
# =========================
titulo_cinta("Actividad")

# Espacio entre títulos
st.markdown("<br>", unsafe_allow_html=True)

titulo_cinta("Proceso de Afiliación de Usuarios y generación de RBU")

actividades = [
    "A- Se elaboró el informe con la propuesta del cronograma anual para la entrega de la subvención monetaria (RBU)",
    "B- Se solicitó a la ONP la relación de no pensionistas en condición de pobreza afiliados al Sistema Nacional de Pensiones, para solicitar los cotejos a las entidades externas",
    "C- Se solicitó a UTI la generación de los archivos de cotejo, para solicitar el cotejo a las entidades externas",
    "D- Se solicitó a las entidades externas (RENIEC, ONP, SIS, ESSALUD, SBS, otros), la información para el cotejo masivo", 
    "E- Se solicitó al OFIS el PGH (RIS) con la información actualizada de la CSE",
    "F- Se recibió la respuesta con los archivos de cotejo masivo de todas las entidades externas", 
    "G- Se realizó la carga de los cotejos recibidos por las entidades externas, a la carpeta compartida con la UTI", 
    "H- Se realizó la carga del preliminar del pre padrón en la carpeta compartida, para la apertura de cuentas",
    "I- Se gestionó la apertura de cuentas de los potenciales usuarios",
    "J- Se emitió el informe de solicitud de terceros autorizados para la emisión de la RDE", 
    "K- Se revisaron las Solicitudes de los expedientes de vulnerabilidad adicional (VA)",
    "L- Se remitió a la UTI la relación de usuarios sin movimiento de cuentas en 12 meses", 
    "M- Se realizó la generación y carga del PRE PADRON en la carpeta compartida, luego del cierre del SISOPE", 
    "N- Se remitió a la UO el término del proceso del PRE-PADRON (cotejo masivo del PGH con la información de las entidades públicas)", 
    "O- Se remitió a la UTI el correo de validación del PRE PADRON",
    """P- Se realizó la carga de la versión final del pre padrón en la carpeta compartida, de acuerdo al detalle siguiente:
• Usuarios que continúan respecto a la RBU del período anterior
• Potenciales usuarios libres producto del cotejo realizado
• Usuarios que serán suspendidos o desafiliados
• Adultos mayores no potenciales""",
    "Q- Se cargó en el SISOPE la lista de fallecidos remitidas por la RENIEC e identificadas por la UT en las visitas domiciliarias",
    "R- Se generó la lista previa a la RBU con información nominal del Ubigeo y DNI, de acuerdo con los siguientes listados nominales: Registros de PROPUESTA DE NUEVOS INGRESOS, Registro de SUSPENDIDOS y DESAFILIADOS",
    "S- Se registró en el SISOPE la propuesta de RBU y se generó el archivo PADRON FINAL que comprende: Registro de PROPUESTA DE NUEVOS INGRESOS, Registro de SUSPENDIDOS y DESAFILIADOS",
    "T- Se confirmó a la UTI la revisión final del padrón generado y registrado en la base de datos del sistema",
    "U- Se remitió a la UO el memorando informando el desarrollo y participación en el procesamiento de elaboración de la RBU", 
    "V- Se emitieron el Informe técnico que sustenta la propuesta de RBU e informe que sustenta las modalidades de cobro, aperturas de cuenta y monto a transferir, incluyendo la Certificación de Crédito Presupuestal para el trámite correspondiente",
]

respuestas = []

for i, act in enumerate(actividades):
    col1, col2, col3 = st.columns([6, 2, 4])
    with col1:
        st.write(act)
    with col2:
        respuesta = st.selectbox(
            "Resultado",
            ["", "SI", "NO", "NA"],
            key=f"resultado_{i}"
        )
    with col3:
        observacion = st.text_input(
            "Observación",
            key=f"obs_{i}"
        )
    respuestas.append({
        "Actividad": act,
        "Resultado": respuesta,
        "Observacion": observacion
    })

st.divider()

# =========================
# GUARDAR INFORMACIÓN
# =========================
titulo_cinta("Guardar Información")

if st.button("💾 Guardar información"):
    # Validación básica de datos
    if not unidad or not nombre or not dni or not cargo:
        st.warning("⚠️ Por favor, complete todos los datos generales antes de guardar.")
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
            df_existente = pd.read_excel(ARCHIVO_EXCEL, engine="openpyxl")
            df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        else:
            df_final = df_nuevo

        df_final.to_excel(ARCHIVO_EXCEL, index=False, engine="openpyxl")

        st.success(f"✅ Información guardada correctamente. Se registraron {len(df_nuevo)} filas.")
        st.dataframe(df_nuevo)
