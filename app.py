import streamlit as st
import base64
import os
import random

# --- 1. CONFIGURACIÓN Y CARGA DE ACTIVOS ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de archivos (Asegúrate que los nombres coincidan exactamente)
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

# --- 2. INYECCIÓN DE CSS (ELIMINACIÓN DE ESTÉTICA "DASHBOARD") ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo de pantalla completa con lavado sutil */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor central de la herramienta - SIN CUADROS */
    .product-showcase {{
        position: relative;
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
        background: transparent !important;
    }}

    /* GLOBO REDONDO: Estilo Sticker de alta visibilidad */
    .discount-sticker {{
        position: absolute;
        top: 20px;
        right: -30px;
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

    .tool-name {{
        font-family: 'WuerthBold';
        font-size: 2rem;
        color: white;
        background: #121212;
        padding: 12px 30px;
        display: inline-block;
        margin-top: -20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Botones minimalistas */
    .stButton>button {{
        background-color: #121212;
        color: white;
        border: none;
        border-radius: 0;
        font-family: 'WuerthBold';
        padding: 15px;
        width: 100%;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{ background-color: #CC0000; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 60px;">
        <img src="data:image/png;base64,{logo_rs}" width="300">
        <img src="data:image/jpg;base64,{logo_w}" width="150">
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; font-family:WuerthExtra; color:#CC0000; font-size:4.5rem; margin:0;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- 4. ÁREA VISUAL CENTRAL ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="product-showcase">', unsafe_allow_html=True)
    
    # El Globo de Descuento (Sticker)
    st.markdown(f'''
        <div class="discount-sticker">
            <span style="font-size:75px; line-height:1;">25%</span>
            <span style="font-size:24px;">OFF</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Imagen de la herramienta (tamaño controlado para evitar scrolls)
    st.image(os.path.join(path_prod, img_actual), width=500)
    
    # Nombre
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-name">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación compacta debajo
    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ ANTERIOR"):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with c2:
        if st.button("SIGUIENTE ➡️"):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- 5. CALCULADORA (Limpia) ---
st.divider()
st.subheader("CÁLCULO DE BENEFICIO")
entrega = st.selectbox("Seleccione el equipo que entrega el cliente:", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
st.button("CONFIRMAR Y CALCULAR PRECIO")
