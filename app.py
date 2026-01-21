import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de archivos críticos
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
if 'descuento' not in st.session_state: st.session_state.descuento = 25 # Default para ver el globo

# --- ESTILO CSS LIMPIO ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con opacidad real del 75% */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor de imagen central */
    .product-container {{
        position: relative;
        text-align: center;
        margin: 0 auto;
        max-width: 600px;
    }}

    /* EL GLOBO: Posicionado sobre la herramienta */
    .badge-sticker {{
        position: absolute;
        top: -10px;
        right: -20px;
        background-color: #CC0000;
        color: white;
        width: 160px;
        height: 160px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 4px solid white;
        box-shadow: 0 10px 30px rgba(204,0,0,0.5);
        z-index: 99;
        transform: rotate(8deg);
    }}

    .tool-name-label {{
        font-family: 'WuerthBold';
        font-size: 2.2rem;
        color: white;
        background: #121212;
        padding: 10px 30px;
        display: inline-block;
        margin-top: -30px;
        text-transform: uppercase;
    }}

    /* Estilo de botones negros minimalistas */
    .stButton>button {{
        background-color: #121212;
        color: white;
        font-family: 'WuerthBold';
        border-radius: 0;
        border: none;
        padding: 15px;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
        color: white;
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

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4rem; margin-top:0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- ÁREA CENTRAL DE HERRAMIENTA ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="product-container">', unsafe_allow_html=True)
    
    # Globo de descuento "flotante"
    st.markdown(f'''
        <div class="badge-sticker">
            <span style="font-size:65px; line-height:1;">{st.session_state.descuento}%</span>
            <span style="font-size:20px;">AHORRO</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Imagen de herramienta
    st.image(os.path.join(path_prod, img_actual), width=550)
    
    # Nombre de la herramienta
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-name-label">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación Simple debajo
    st.write("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ ANTERIOR MODELO", use_container_width=True):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with col2:
        if st.button("SIGUIENTE MODELO ➡️", use_container_width=True):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- CALCULADORA (Simple y separada) ---
st.divider()
st.subheader("CALCULADORA DE BENEFICIO")
c_sel, c_btn = st.columns([3, 1])
with c_sel:
    entrega = st.selectbox("Equipo entregado por el cliente:", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"], label_visibility="collapsed")
with c_btn:
    if st.button("CALCULAR", use_container_width=True):
        if "Completa" in entrega: st.session_state.descuento = 25
        elif "Parcial" in entrega: st.session_state.descuento = 15
        else: st.session_state.descuento = 10
        st.rerun()
