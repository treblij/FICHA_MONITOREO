import streamlit as st
import pandas as pd
import os
from datetime import datetime

import pip
pip.main(["install","openpyxl"])

ARCHIVO_EXCEL = "registros_monitoreo.xlsx"

st.set_page_config(page_title="Ficha de Monitoreo", layout="wide")

st.title("📋 Ficha de Monitoreo a la gestion de la entrega de la pension no contributiva")

# =====================
# DATOS GENERALES
# =====================
st.subheader("Datos Generales")

col1, col2 = st.columns(2)
with col1:
    unidad = st.text_input("Unidad(es) Orgánica(s)")
with col2:
    fecha_supervision = st.date_input("Fecha(s) de Supervisión")

nombre = st.text_input("Apellidos y Nombres del entrevistado")
dni = st.text_input("DNI")
cargo = st.text_input("Cargo")

st.divider()

# =====================
# ACTIVIDADES (ejemplo)
# =====================
st.subheader("Actividad")
st.subheader("Proceso de Afiliación de Usuarios y generación de RBU")

actividades = [
    "A- Se elaboró el informe con la propuesta del cronograma anual (RBU)",
    "B- Se solicitó a la ONP la relación de no pensionistas",
    "C- Se solicitó a la UTI la generación de archivos de cotejo",
    "D- Se solicitó información a entidades externas",
]

respuestas = []

for act in actividades:
    col1, col2, col3 = st.columns([6, 2, 4])
    with col1:
        st.write(act)
    with col2:
        respuesta = st.selectbox(
            "Resultado",
            ["SI", "NO", "NA"],
            key=act
        )
    with col3:
        observacion = st.text_input(
            "Observación",
            key=f"obs_{act}"
        )

    respuestas.append({
        "Actividad": act,
        "Resultado": respuesta,
        "Observacion": observacion
    })

st.divider()

# =====================
# GUARDAR
# =====================
if st.button("💾 Guardar información"):
    filas = []

    for r in respuestas:
        filas.append({
            "Fecha Registro": datetime.now(),
            "Unidad Organica": unidad,
            "Fecha Supervision": fecha_supervision,
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
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(ARCHIVO_EXCEL, index=False)

    st.success("✅ Información guardada correctamente en el archivo Excel")

