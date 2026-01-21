import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de Tipografías y Logos
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de carpetas
path_fondos = "assets2/" 
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)
if 'descuento' not in st.session_state: st.session_state.descuento = 25 # Mostramos globo por defecto

# --- CSS DE ALTA PRECISIÓN (ESTILO CATÁLOGO) ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con transparencia del 75% (0.25 de opacidad blanca) */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor de la herramienta (Sin cuadros grises) */
    .main-stage {{
        position: relative;
        text-align: center;
        margin: 0 auto;
        max-width: 650px;
        background: transparent !important;
    }}

    /* EL GLOBO GIGANTE: Pegado a la herramienta */
    .floating-badge {{
        position: absolute;
        top: 20px;
        right: -30px;
        background-color: #CC0000;
        color: white;
        width: 175px;
        height: 175px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 5px solid white;
        box-shadow: 0 12px 35px rgba(204,0,0,0.4);
        z-index: 100;
        transform: rotate(12deg);
    }}

    /* Etiqueta de nombre en negro */
    .tool-tag {{
        font-family: 'WuerthBold';
        font-size: 2.2rem;
        color: white;
        background: #121212;
        padding: 10px 35px;
        display: inline-block;
        margin-top: -30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Botoneras minimalistas */
    .stButton>button {{
        background-color: #121212;
        color: white;
        border: none;
        border-radius: 0;
        font-family: 'WuerthBold';
        padding: 15px;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER (LOGOS POSICIONADOS) ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 60px;">
        <img src="data:image/png;base64,{logo_rs}" width="320">
        <img src="data:image/jpg;base64,{logo_w}" width="160">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4.5rem; margin: 0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- ESCENARIO DE PRODUCTO ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="main-stage">', unsafe_allow_html=True)
    
    # Globo de descuento
    st.markdown(f
