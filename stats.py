# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 12:18:02 2026

@author: usuario

Stats sobre las jornadas Nosotras investigamos - 11F 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración estética
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ====== 1. Cargar archivo ======
archivo = "C:/Users/usuario/Downloads/Stats_jornadas.tsv"  # Cambia por el nombre de tu archivo
df = pd.read_csv(archivo, sep="\t")


# Crear identificadores únicos para emails vacíos

# Crear identificadores únicos SOLO donde falte email
mask_sin_email = df["Email address"].isna()
df.loc[mask_sin_email, "Email address"] = (
    "sin_email_" + df.loc[mask_sin_email].index.to_series().astype(str)
)

# Eliminar duplicados (mantiene la primera inscripción)
df = df.drop_duplicates(subset="Email address", keep="first")

print("Número total de inscripciones:", len(df))

#%%
# ====== 2. Asistencia confirmada ======

asistencia = df["Asistencia a las jornadas"].value_counts()

print("\nAsistencia:")
print(asistencia)

# Función para mostrar porcentaje + número absoluto
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({count})"
    return my_format

# Paleta morada
colores = ["#4B0082", "#C8A2C8"]  # morado oscuro / morado claro

# Crear gráfico
fig, ax = plt.subplots(figsize=(6,6))

wedges, texts, autotexts = ax.pie(
    asistencia,
    labels=asistencia.index,
    autopct=autopct_format(asistencia),
    startangle=90,
    colors=colores
)

# Cambiar color del texto según el fondo
for i, autotext in enumerate(autotexts):
    if colores[i] == "#4B0082":   # morado oscuro
        autotext.set_color("white")
    else:
        autotext.set_color("black")

plt.title(f"Asistencia a las Jornadas\nTotal inscritos: {len(df)}")
plt.axis('equal')
plt.tight_layout()

# %%
# ====== 2. Sexo ======
# Note : We hadn't recorded the information; it's incomplete based on the first name, so there may be biases.


asistencia = df["Sexo"].replace({"M": "Mujer", "H": "Hombre"}).value_counts()

print("\nAsistencia:")
print(asistencia)

# Función para mostrar porcentaje + número absoluto
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({count})"
    return my_format

# Paleta morada
colores = ["#4B0082", "#C8A2C8"]  # morado oscuro / morado claro

# Crear gráfico
fig, ax = plt.subplots(figsize=(6,6))

wedges, texts, autotexts = ax.pie(
    asistencia,
    labels=asistencia.index,
    autopct=autopct_format(asistencia),
    startangle=90,
    colors=colores
)

# Cambiar color del texto según el fondo
for i, autotext in enumerate(autotexts):
    if colores[i] == "#4B0082":   # morado oscuro
        autotext.set_color("white")
    else:
        autotext.set_color("black")

plt.title(f"Reparticion por sexo\nTotal inscritos: {len(df)}")
plt.axis('equal')
plt.tight_layout()
#%%
# =============================================================================
# # Para el resto vamos a illustrar solo los que asistieron
# =============================================================================
filtro_asistentes = df["Asistencia a las jornadas"].str.contains("Si", na=False)
df_asistentes = df[filtro_asistentes].copy()
df = df_asistentes
print(f"Número de personas que asistieron: {len(df_asistentes)}")


# ====== 3. Puesto / Etapa profesional ======
# limpio (lo siento abuela de la ponente)

# ==========================================
# 1️DEFINIR CATEGORÍAS FINALES
# ==========================================

MAPEO_CATEGORIAS = {
    # -------------------------
    # ESTUDIANTADO UNIVERSITARIO
    # -------------------------
    "Estudiante universitaria/o": "Estudiante universitario/a",
    "Estudiante de Máster ": "Estudiante universitario/a",
    "Màster": "Estudiante universitario/a",
    "Posgrado y estudiante de maestría": "Estudiante universitario/a",
    "Máster universitario en danza y arte terapia": "Estudiante universitario/a",

    # -------------------------
    # DOCTORADO / PREDOCTORAL
    # -------------------------
    "Estudiante de doctorado": "Doctorado / Predoctoral",
    "Investigador predoctoral contratado. ": "Doctorado / Predoctoral",
    "FPU": "Doctorado / Predoctoral",

    # -------------------------
    # POSTDOC
    # -------------------------
    "Postdoc / Investigador/a en etapa temprana": "Postdoc",

    # -------------------------
    # PROFESORADO
    # -------------------------
    "Profesor/a universitario/a / PDI": "Profesorado",
    "Profesora de matemáticas en el IES LLANES": "Profesorado",

    # -------------------------
    # PERSONAL TECNICO / ADMIN
    # -------------------------
    "Tecnica de apoyo en investigación": "Personal técnico",
    "PTGAS": "Personal técnico",

    # -------------------------
    # PUBLICO GENERAL
    # -------------------------
    "No me dedico a la ciencia, pero estoy muy interesadx": "Público general",
    "Médica jubilada": "Público general",
    "Abuela de la ponente ": "Público general",
    "Jardinero": "Público general",
    "Formada en distintas disciplinas universitarias": "Público general",
}

# ==========================================
# 2️APLICAR MAPEO
# ==========================================

def agrupar_categoria(valor):
    if pd.isna(valor):
        return "Sin especificar"
    return MAPEO_CATEGORIAS.get(valor, "OTRO / REVISAR")

df["Etapa profesional (agrupada)"] = df["Puesto / Etapa profesional"].apply(agrupar_categoria)

# ==========================================
# 3️VER RESULTADO
# ==========================================

print("\nDistribución agrupada:")
print(df["Etapa profesional (agrupada)"].value_counts())

# Filas marcadas como OTRO / REVISAR
otros = df[df["Etapa profesional (agrupada)"] == "OTRO / REVISAR"]

# Mostrar columna original y cuántas veces aparece cada valor
categorias_otros = otros["Puesto / Etapa profesional"].value_counts()

print("Categorías originales que quedaron como OTRO / REVISAR:")
print(categorias_otros)

# =============================================================================
# # Figure
# =============================================================================
# # Contar etapas profesionales
etapas = df["Etapa profesional (agrupada)"].value_counts()

# Crear degradado morado
num_barras = len(etapas)
colores = plt.cm.Purples(np.linspace(0.35, 0.95, num_barras))

fig, ax = plt.subplots(figsize=(10,6))

bars = ax.barh(etapas.index, etapas.values, color=colores)

# Añadir número en cada barra
for i, bar in enumerate(bars):
    width = bar.get_width()
    
    # Si el color es oscuro → texto blanco
    if i > num_barras / 2:
        color_texto = "white"
    else:
        color_texto = "black"
    
    ax.text(
        width - 0.5 if color_texto == "white" else width + 0.5,
        bar.get_y() + bar.get_height()/2,
        f"{int(width)}",
        va='center',
        ha='right' if color_texto == "white" else 'left',
        color=color_texto,
        fontweight="bold"
    )

ax.set_title("Distribución por Etapa Profesional")
ax.set_xlabel("Número de personas")
ax.invert_yaxis()  # La categoría más frecuente arriba
plt.tight_layout()


#%%
# ====== 4. ¿Cómo conocieron las jornadas? ======
origen = df["¿Cómo conociste estas jornadas?"].value_counts()

print("\nCómo conocieron las jornadas:")
print(origen)


MAPEO_CATEGORIAS = {
    "Recomendación de una amiga / profesores": "Recomendación",
    "Soy compi de las organizadoras. " : "Recomendación",
    
    "Universidad / Facultades" : "Universidad / Facultades",
    "Redes sociales" : "Redes sociales",
    "Internet " : "Internet",
    "Página web" : "Internet",
    "Ingrese a la pagina de CICUS" : "Internet",
    "Carteles" : "Carteles",
    "Una amiga " : "Recomendación"
}

df["Canal de diffusion (agrupada)"] = df["¿Cómo conociste estas jornadas?"].apply(agrupar_categoria)

print("\nDistribución agrupada:")
print(df["Canal de diffusion (agrupada)"].value_counts())

# Filas marcadas como OTRO / REVISAR
otros = df[df["Canal de diffusion (agrupada)"] == "OTRO / REVISAR"]

# Mostrar columna original y cuántas veces aparece cada valor
categorias_otros = otros["¿Cómo conociste estas jornadas?"].value_counts()

print("Categorías originales que quedaron como OTRO / REVISAR:")
print(categorias_otros)

origen = df["Canal de diffusion (agrupada)"].value_counts()
# =============================================================================
# Figure
# =============================================================================

# Crear degradado morado
num_barras = len(origen)
colores = plt.cm.Purples(np.linspace(0.35, 0.95, num_barras))

fig, ax = plt.subplots(figsize=(10,6))

bars = ax.barh(origen.index, origen.values, color=colores)

# Añadir número en cada barra
for i, bar in enumerate(bars):
    width = bar.get_width()
    
    # Si el color es oscuro → texto blanco
    if i > num_barras / 2:
        color_texto = "white"
    else:
        color_texto = "black"
    
    ax.text(
        width - 0.5 if color_texto == "white" else width + 0.5,
        bar.get_y() + bar.get_height()/2,
        f"{int(width)}",
        va='center',
        ha='right' if color_texto == "white" else 'left',
        color=color_texto,
        fontweight="bold"
    )

ax.set_title("¿Cómo conocieron las Jornadas?")
ax.set_xlabel("Número de personas")
ax.set_ylabel("Canal de difusión")
ax.invert_yaxis()  # La categoría más frecuente arriba
plt.tight_layout()

#%%
# ===============================
# Actividades planeadas
# ===============================

col_actividades = "¿A qué actividades planeas asistir? (puedes seleccionar varias)"
# Diccionario de reemplazo (normalización)
NORMALIZACION_ACTIVIDADES = {
    'AFORO COMPLETO (lista de espera) - Ponencia online "Mujeres en la ciencia: datos':
        'Ponencia "Mujeres en la ciencia: datos, desafíos y brechas estructurales con perspectiva de género"',
    'Ponencia "Mujeres en la ciencia: datos': 'Ponencia "Mujeres en la ciencia: datos, desafíos y brechas estructurales con perspectiva de género"',
    'desafíos y brechas estructurales con perspectiva de género"': np.nan
    # Aquí puedes añadir más reemplazos si hay variantes
    # 'Otra variante': 'Nombre estándar',
}

actividades = df[col_actividades].dropna().str.split(",")
actividades = actividades.explode().str.strip()
# Aplicar normalización
actividades = actividades.replace(NORMALIZACION_ACTIVIDADES)
conteo_actividades = actividades.value_counts()

plt.figure(figsize=(10,6))
sns.barplot(x=conteo_actividades.values, y=conteo_actividades.index, hue=conteo_actividades.index,
            palette="Purples_r")
plt.title("Actividades a las que asistieron")
plt.xlabel("Número de personas")
plt.ylabel("Actividad")


# Contar cuántas actividades eligió cada persona
num_actividades = df[col_actividades].dropna().str.split(",").apply(len)

# Contar cuántas personas eligieron 1, 2, 3… actividades
conteo = num_actividades.value_counts().sort_index()

# Función para mostrar porcentaje + número absoluto
def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({count})"
    return my_format

# Crear camembert
plt.figure(figsize=(7,7))
plt.pie(
    conteo,
    labels=[f"{i} actividades" for i in conteo.index],
    autopct=autopct_format(conteo),
    startangle=90,
    colors=plt.cm.Purples_r(np.linspace(0.20, 0.95, len(conteo)))
)
plt.title("¿A cuántas actividades se inscribió cada persona?")
plt.axis('equal')
plt.tight_layout()


# %%
# ===============================
# Preferencia horaria del simposio
# ===============================
col_simposio = "Si has elegido, asistencia al simposio. Por favor, indicanos tu preferencia horaria:"

NORMALIZACION_SIMPOSIO = {
    "Sin preferencia": ["Turno mañana I: 10:00 – 11:30", 
                        "Turno mañana II: 12:30 – 13:30", 
                        "Turno tarde: 15:00 – 16:30"],
    "Turno mañana I: 10:00 – 11:30": ["Turno mañana I: 10:00 – 11:30"],
    "Turno mañana II: 12:30 – 13:30": ["Turno mañana II: 12:30 – 13:30"],
    "Turno tarde: 15:00 – 16:30": ["Turno tarde: 15:00 – 16:30"], 
    'No puedo/no me apetece asistir a los simposios': np.nan
}

df["Turnos simposio"] = df[col_simposio].map(NORMALIZACION_SIMPOSIO)
df_turnos = df.explode("Turnos simposio").dropna(subset=["Turnos simposio"])

conteo_turnos = df_turnos["Turnos simposio"].value_counts().sort_index()

plt.figure(figsize=(10,6))
sns.barplot(x=conteo_turnos.values, y=conteo_turnos.index, hue=conteo_turnos.index,
            palette="Purples_r")
plt.title("Distribución de preferencias horarias de los simposios")
plt.xlabel("Número de personas")
plt.ylabel("Horario")
plt.tight_layout()

# %%
# ===============================
# Taller de Bienestar emocional
# ===============================
col_taller = 'AFORO COMPLETO - ¿Te gustaría asistir al taller sobre “Bienestar emocional y prevención de estrés en contexto de investigación” a cargo de la Unidad de Psicología Aplicada de la Universidad de Sevilla? (opcional, máximo 30 plazas)'

NORMALIZACION_TALLER = {
    "Me encantaría inscribirme": "Si",
    "Inscribirme en lista de espera": "Si",
    "No quiero inscribirme": "No"
}

df["taller"] = df[col_taller].map(NORMALIZACION_TALLER)

conteo_taller = df["taller"].value_counts()

plt.figure(figsize=(10,6))
# sns.barplot(x=conteo_taller.values, y=conteo_taller.index, palette="Purples_r")
# Crear camembert
plt.figure(figsize=(7,7))
plt.pie(
    conteo_taller,
    labels=[f"{i}" for i in conteo_taller.index],
    autopct=autopct_format(conteo_taller),
    startangle=90,
    colors=plt.cm.Purples_r(np.linspace(0.20, 0.95, len(conteo_taller)))
)
plt.title("Taller sobre “Bienestar emocional y prevención de estrés en contexto de investigación” \n a cargo de la Unidad de Psicología Aplicada de la Universidad de Sevilla")
plt.xlabel("Número de personas")
plt.ylabel("Respuesta")
plt.axis('equal') 
plt.tight_layout()


# %%

import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Image, Table
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.lib import utils

# Save matplotlib figures
image_paths = []

for i, fig_num in enumerate(plt.get_fignums()):
    fig = plt.figure(fig_num)
    img_path = f"figure_{i+1}.png"
    fig.savefig(img_path, bbox_inches="tight", dpi=300)
    image_paths.append(img_path)

# Create landscape document with small margins
pdf_path = "report.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=landscape(A4),
    rightMargin=0.5*inch,
    leftMargin=0.5*inch,
    topMargin=0.1*inch,
    bottomMargin=0.1*inch
)

elements = []

# Grid configuration
cols = 3
rows = 3

page_width, page_height = landscape(A4)

usable_width = page_width - doc.leftMargin - doc.rightMargin
usable_height = page_height - doc.topMargin - doc.bottomMargin

cell_width = usable_width / cols
cell_height = usable_height / rows


def get_image_keep_ratio(path, max_width, max_height):
    img = utils.ImageReader(path)
    img_width, img_height = img.getSize()

    ratio = min(max_width / img_width, max_height / img_height)

    return Image(
        path,
        width=img_width * ratio,
        height=img_height * ratio
    )


# Prepare exactly 9 cells (fill empty if needed)
images = image_paths[:9]
while len(images) < 9:
    images.append("")

table_data = []
index = 0

for r in range(rows):
    row = []
    for c in range(cols):
        if images[index] != "":
            row.append(get_image_keep_ratio(images[index], cell_width, cell_height))
        else:
            row.append("")
        index += 1
    table_data.append(row)

table = Table(
    table_data,
    colWidths=[cell_width] * cols,
    rowHeights=[cell_height] * rows
)

elements.append(table)

doc.build(elements)

print("PDF created:", pdf_path)




#%%
# ====== certificado ======
columna_dni = "Necesita certificado"

# Filtrar solo las filas donde hay valor en DNI (no vacío)
df_certificado = df[df[columna_dni].notna() & (df[columna_dni].astype(str).str.strip() != "")].copy()

# Crear tabla final con Nombre, Email y DNI
columnas_finales = ["Nombre y apellidos", "Email address", columna_dni]
df_certificado_final = df_certificado[columnas_finales]

# Exportar a Excel
df_certificado_final.to_excel("necessidad_certificados.xlsx", index=False)

print(f"Archivo 'certificados.xlsx' creado con {len(df_certificado_final)} personas.")

