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

# --- CSS DE ALTO IMPACTO (FONDO Y GLOBO) ---
bg_data = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo corregido para que se aprecien las imágenes de assets2 */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/jpeg;base64,{bg_data}) no-repeat center center fixed;
        background-size: cover;
    }}

    /* Contenedor central compacto */
    .showcase-wrapper {{
        position: relative;
        max-width: 650px;
        margin: 0 auto;
        text-align: center;
    }}

    /* GLOBO DE DESCUENTO: Grande y sobre la herramienta */
    .discount-sticker {{
        position: absolute;
        top: 20px;
        right: 20px;
        background: #CC0000;
        color: white;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        border: 4px solid white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        z-index: 100;
        transform: rotate(10deg);
    }}

    .tool-label-black {{
        font-family: 'WuerthBold';
        font-size: 2.2rem;
        color: white;
        background: #121212;
        padding: 10px 25px;
        display: inline-block;
        margin-top: -20px;
    }}

    /* Estilo de la calculadora */
    .calc-section {{
        background: rgba(255, 255, 255, 0.9);
        padding: 25px;
        border-radius: 15px;
        margin-top: 30px;
        border-top: 6px solid #CC0000;
    }}

    .stButton>button {{
        background-color: #121212;
        color: white;
        border-radius: 0;
        font-family: 'WuerthBold';
        height: 3rem;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
        <img src="data:image/png;base64,{logo_rs}" width="300">
        <img src="data:image/jpg;base64,{logo_w}" width="150">
    </div>
''', unsafe_allow_html=True)

# --- ESCENARIO DE PRODUCTO ---
if productos:
    img_actual = productos[st.session_state.idx]
    
    st.markdown('<div class="showcase-wrapper">', unsafe_allow_html=True)
    
    # Globo de Descuento
    if st.session_state.descuento > 0:
        st.markdown(f'''
            <div class="discount-sticker">
                <span style="font-size:60px; line-height:1;">{st.session_state.descuento}%</span>
                <span style="font-size:20px;">OFF</span>
            </div>
        ''', unsafe_allow_html=True)
    
    # Imagen de Herramienta (Tamaño controlado)
    st.image(os.path.join(path_prod, img_actual), width=500)
    
    # Etiqueta de Nombre
    nombre = img_actual.split('.')[0].replace('_', ' ').upper()
    st.markdown(f'<div class="tool-label-black">{nombre}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegación Simple
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ ANTERIOR MODELO", use_container_width=True):
            st.session_state.idx = (st.session_state.idx - 1) % len(productos)
            st.rerun()
    with col_nav2:
        if st.button("SIGUIENTE MODELO ➡️", use_container_width=True):
            st.session_state.idx = (st.session_state.idx + 1) % len(productos)
            st.rerun()

# --- CALCULADORA ---
st.markdown('<div class="calc-section">', unsafe_allow_html=True)
st.markdown("<h3 style='color:#121212; font-family:WuerthBold;'>CÁLCULO DE BENEFICIO</h3>", unsafe_allow_html=True)
c_sel, c_btn = st.columns([3, 1])
with c_sel:
    entrega = st.selectbox("¿Qué equipo entrega el cliente?", 
                         ["Máquina Completa", "Máquina Parcial", "Solo Batería/Cargador"], label_visibility="collapsed")
with c_btn:
    if st.button("CALCULAR", use_container_width=True):
        if "Completa" in entrega: st.session_state.descuento = 25
        elif "Parcial" in entrega: st.session_state.descuento = 15
        else: st.session_state.descuento = 10
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
