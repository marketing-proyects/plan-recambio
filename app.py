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

# Carga de recursos (Fuentes y Logos)
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de archivos (Fondos y Productos)
path_fondos = "assets2/" 
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)
if 'descuento' not in st.session_state: st.session_state.descuento = 0

# --- ESTILOS CSS LIMPIOS (FOCO EN EL GLOBO Y FONDO) ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con transparencia real para ver assets2 */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor de la herramienta sin cuadros grises */
    .product-stage {{
        position: relative;
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
        background: transparent !important;
    }}

    /* EL GLOBO: Grande, Rojo y cerca de la herramienta */
    .sticker-badge {{
        position: absolute;
        top: 10px;
        right: -10px;
        background-color: #CC0000;
        color: white;
        width: 170px;
        height: 170px;
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

    .tool-name-tag {{
        font-family: 'WuerthBold';
        font-size: 2.2rem;
        color: white;
        background: #121212;
        padding: 12px 30px;
        display: inline-block;
        margin-top: -25px;
        text-transform: uppercase;
    }}

    /* Botoneras estilo minimalista */
    .stButton>button {{
        background-color: #121212;
        color: white;
        font-family: 'WuerthBold';
        border-radius: 0;
        border: none;
        padding: 15px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 50px;">
        <img src="data:image/png;base64,{logo_rs}" width="300">
        <img src="data:image/jpg;base64,{logo_w}" width="160">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4.5rem; margin-top:0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- VISUALIZACIÓN DE PRODUCTO ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="product-stage">', unsafe_allow_html=True)
    
    # Globo de ahorro (Badge)
    if st.session_state.descuento > 0:
        st.markdown(f'''
            <div class="sticker-badge">
                <span style="font-size:70px; line-height:1;">{st.session_state.descuento}%</span>
                <span style="font-size:22px;">OFF</span>
            </div>
        ''', unsafe_allow_html=True)
    
    # Imagen de la herramienta (Tamaño equilibrado)
    st.image(os.path.join(path_prod, img_actual), width=500)
    
    # Etiqueta con el nombre
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-name-tag">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación del Carrusel
    st.write("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ MODELO ANTERIOR", use_container_width=True):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with col2:
        if st.button("SIGUIENTE MODELO ➡️", use_container_width=True):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- CALCULADORA DE DESCUENTOS ---
st.divider()
st.subheader("CALCULADORA DE BENEFICIO")
c_ui, c_act = st.columns([3, 1])
with c_ui:
    entrega = st.selectbox("Seleccione qué entrega el cliente:", 
                         ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"], label_visibility="collapsed")
with c_act:
    if st.button("APLICAR", use_container_width=True):
        if "Completa" in entrega: st.session_state.descuento = 25
        elif "Parcial" in entrega: st.session_state.descuento = 15
        else: st.session_state.descuento = 10
        st.rerun()
