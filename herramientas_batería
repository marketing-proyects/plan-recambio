import streamlit as st
import base64
from pathlib import Path

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

# --- FUNCIÓN PARA CARGAR FUENTES (Uso de tus archivos .ttf) ---
def get_base64_font(font_path):
    with open(font_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Intentamos cargar tus fuentes (asegúrate de que los archivos estén en la misma carpeta)
try:
    font_bold = get_base64_font("WuerthBold.ttf")
    font_book = get_base64_font("WuerthBook.ttf")
    font_extra = get_base64_font("WuerthExtraBoldCond.ttf")
except FileNotFoundError:
    # Fallback por si los nombres de archivo varían
    font_bold = font_book = font_extra = ""

# --- INYECCIÓN DE ESTILO WÜRTH ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{font_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{font_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{font_extra}); }}

    html, body, [class*="css"] {{
        font-family: 'WuerthBook', sans-serif;
    }}

    h1, h2, h3, .stMetric label {{
        font-family: 'WuerthExtra', sans-serif !important;
        color: #CC0000;
        text-transform: uppercase;
    }}

    /* Estilo del Header Principal */
    .main-header {{
        background-color: #CC0000;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }}
    
    .main-header h1 {{
        color: white !important;
        margin: 0;
        font-size: 3rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header"><h1>PLAN RECAMBIO</h1></div>', unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tabs = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Consolidación"])

# --- PERSISTENCIA DE DATOS (Session State) ---
if 'descuento_global' not in st.session_state:
    st.session_state.descuento_global = 0

# --- FASE 1: CALCULADORA ---
with tabs[0]:
    st.subheader("Cálculo de Beneficio")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Complete lo que el cliente entrega:")
        item = st.selectbox("Equipo entregado", 
                            ["Máquina Completa (Herramienta + 2 Bat + Cargador)", 
                             "Máquina Parcial (Solo Herramienta)", 
                             "Baterías / Cargadores sueltos"])
        cant = st.number_input("Cantidad", min_value=1, step=1)
        
    with col2:
        # Aquí irá la lógica visual una vez definida
        st.metric("Descuento Aplicable", f"{st.session_state.descuento_global}%")
        if st.button("Calcular y Aplicar"):
            # Lógica temporal para probar
            st.session_state.descuento_global = 20 if "Completa" in item else 10
            st.rerun()

# --- FASE 2: CATÁLOGO ---
with tabs[1]:
    st.subheader("Equipos Disponibles")
    if st.session_state.descuento_global > 0:
        st.success(f"Aplicando {st.session_state.descuento_global}% de descuento por plan recambio.")
    else:
        st.warning("Primero debe calcular el descuento en la Fase 1.")

# --- FASE 3: CONSOLIDACIÓN ---
with tabs[2]:
    st.subheader("Resumen de Operación")
    st.caption("Nota: Los precios finales no incluyen fletes ni impuestos.")
