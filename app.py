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

# Carga de recursos
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de archivos
path_fondos = "assets2/" 
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)
if 'descuento' not in st.session_state: st.session_state.descuento = 0

# --- CSS DE PRECISIÓN ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.3)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor Principal Ajustado */
    .viewport-container {{
        position: relative;
        width: 100%;
        max-width: 600px; /* Herramientas más pequeñas, no ocupan toda la pantalla */
        margin: 0 auto;
        text-align: center;
    }}

    /* GLOBO PEGADO A LA HERRAMIENTA */
    .sticker-badge {{
        position: absolute;
        top: 10px;
        right: 0px;
        background: #CC0000;
        color: white;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 4px solid white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        z-index: 99;
        transform: rotate(5deg);
    }}

    .tool-title {{
        font-family: 'WuerthBold';
        font-size: 1.8rem;
        color: white;
        background: #121212;
        padding: 8px 20px;
        display: inline-block;
        margin-top: -15px;
    }}

    /* Estilo Calculadora */
    .calc-box {{
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        border-top: 5px solid #CC0000;
        margin-top: 20px;
        color: #121212;
    }}

    .stButton>button {{
        background-color: #121212;
        color: white;
        border-radius: 0;
        font-family: 'WuerthBold';
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 30px;">
        <img src="data:image/png;base64,{logo_rs}" width="250">
        <img src="data:image/jpg;base64,{logo_w}" width="130">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#CC0000; font-family:WuerthExtra;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- AREA VISUAL ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="viewport-container">', unsafe_allow_html=True)
    
    # Globo dinámico
    if st.session_state.descuento > 0:
        st.markdown(f'''
            <div class="sticker-badge">
                <span style="font-size:50px; line-height:1;">{st.session_state.descuento}%</span>
                <span style="font-size:15px;">OFF</span>
            </div>
        ''', unsafe_allow_html=True)
    
    # Imagen de Herramienta (Tamaño controlado)
    st.image(os.path.join(path_prod, img_actual), width=450)
    
    # Nombre
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-title">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación compacta
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("◀"):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with c2:
        if st.button("🎯 SELECCIONAR HERRAMIENTA"):
            st.toast(f"Seleccionada: {nombre}")
    with c3:
        if st.button("▶"):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- CALCULADORA (REINTEGRADA) ---
st.markdown('<div class="calc-box">', unsafe_allow_html=True)
st.subheader("CALCULADORA DE DESCUENTO")
col_c1, col_c2 = st.columns(2)
with col_c1:
    entrega = st.selectbox("¿Qué entrega el cliente?", ["Máquina Completa", "Máquina Parcial", "Solo Batería/Cargador"])
with col_c2:
    if st.button("APLICAR DESCUENTO"):
        if "Completa" in entrega: st.session_state.descuento = 25
        elif "Parcial" in entrega: st.session_state.descuento = 15
        else: st.session_state.descuento = 10
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
