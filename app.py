import streamlit as st
import base64
import os
import random

# --- 1. CONFIGURACIÓN Y RECURSOS ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de identidades
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de imágenes
path_fondos = "assets2/"
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)

# --- 2. ESTILO CSS (PURO Y LIMPIO) ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con lavado blanco sutil para ver la imagen de assets2 */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor de la herramienta (Sin marcos ni cuadros) */
    .product-stage {{
        position: relative;
        max-width: 700px;
        margin: 0 auto;
        text-align: center;
        background: transparent !important;
    }}

    /* EL GLOBO: Gigante, pegado a la herramienta */
    .sticker-badge {{
        position: absolute;
        top: -10px;
        right: 0px;
        background-color: #CC0000;
        color: white;
        width: 180px;
        height: 180px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 6px solid white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 100;
        transform: rotate(12deg);
    }}

    /* Etiqueta de nombre */
    .tool-title {{
        font-family: 'WuerthBold';
        font-size: 2.2rem;
        color: white;
        background: #121212;
        padding: 10px 30px;
        display: inline-block;
        margin-top: -30px;
        text-transform: uppercase;
    }}

    /* Botones de navegación */
    .stButton>button {{
        background-color: #121212;
        color: white;
        border: none;
        border-radius: 0;
        font-family: 'WuerthBold';
        padding: 15px;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (JERARQUÍA DE LOGOS) ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 60px;">
        <img src="data:image/png;base64,{logo_rs}" width="350">
        <img src="data:image/jpg;base64,{logo_w}" width="160">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4.5rem; margin:0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- 4. ÁREA CENTRAL ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="product-stage">', unsafe_allow_html=True)
    
    # Globo de descuento (Aparece siempre como referencia en esta base)
    st.markdown(f'''
        <div class="sticker-badge">
            <span style="font-size:75px; line-height:1;">25%</span>
            <span style="font-size:22px;">OFF</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Herramienta
    st.image(os.path.join(path_prod, img_actual), width=550)
    
    # Nombre
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-title">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación
    st.write("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ MODELO ANTERIOR"):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with col2:
        if st.button("SIGUIENTE MODELO ➡️"):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- 5. CALCULADORA (BÁSICA) ---
st.divider()
st.subheader("CALCULADORA DE BENEFICIO")
entrega = st.selectbox("Seleccione equipo a entregar", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
st.button("CONFIRMAR SELECCIÓN")
