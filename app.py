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

# Carga de recursos (Tipografías y Logos)
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de Carrusel
path_fondos = "assets2/" 
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)
if 'pausado' not in st.session_state: st.session_state.pausado = False

# --- CSS DEFINITIVO (BLACK LABEL & TRANSPARENCIA) ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo corregido con opacidad 75% */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor de la herramienta sin cuadros */
    .showcase-container {{
        position: relative;
        width: 100%;
        max-width: 700px;
        margin: 0 auto;
        padding: 0;
        background: transparent !important;
    }}

    /* GLOBO GIGANTE FLOTANTE */
    .badge-sticker {{
        position: absolute;
        top: -20px;
        right: -10px;
        background: #CC0000;
        color: white;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 5px solid white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        z-index: 100;
        transform: rotate(10deg);
    }}

    /* Estética de botones negros */
    .stButton>button {{
        background-color: #121212;
        color: white;
        border: 1px solid #444;
        border-radius: 0;
        font-family: 'WuerthBold';
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
        border-color: #CC0000;
    }}
    
    .tool-label {{
        font-family: 'WuerthBold';
        font-size: 2rem;
        background: rgba(255,255,255,0.8);
        padding: 5px 20px;
        display: inline-block;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 50px;">
        <img src="data:image/png;base64,{logo_rs}" width="320">
        <img src="data:image/jpg;base64,{logo_w}" width="160">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4rem; margin-bottom:0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- CARRUSEL CENTRAL ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    # Bloque de imagen y badge
    st.markdown('<div class="showcase-container">', unsafe_allow_html=True)
    
    # Badge (Globo)
    desc = st.session_state.get('descuento_seleccionado', 25)
    st.markdown(f'''
        <div class="badge-sticker">
            <span style="font-size:70px; line-height:0.9;">{desc}%</span>
            <span style="font-size:22px;">OFF</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Herramienta
    st.image(os.path.join(path_prod, img_actual), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación y Nombre (Compacto debajo de la herramienta)
    c1, c_name, c2 = st.columns([1, 4, 1])
    with c1:
        if st.button("◀", use_container_width=True):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with c_name:
        nombre = img_actual.split('.')[0].replace('_', ' ').upper()
        st.markdown(f"<div style='text-align:center;'><span class='tool-label'>{nombre}</span></div>", unsafe_allow_html=True)
    with c2:
        if st.button("▶", use_container_width=True):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

    # Botón Principal de Acción
    st.write("<br>", unsafe_allow_html=True)
    if st.button("🎯 QUIERO ESTA HERRAMIENTA", use_container_width=True):
        st.session_state.pausado = True
        st.success(f"Has seleccionado la {nombre}. Ahora calcula tu descuento abajo.")

# --- FASE DE CÁLCULO (Solo si seleccionó) ---
if st.session_state.pausado:
    st.divider()
    # Aquí iría la calculadora simplificada
