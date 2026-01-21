import streamlit as st
import base64
import os
import random

# --- SOPORTE DE ARCHIVOS ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def get_random_bg():
    bg_dir = "assets2/fondos"
    current_bg_dir = bg_dir if os.path.exists(bg_dir) else "."
    fondos = [f for f in os.listdir(current_bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return os.path.join(current_bg_dir, random.choice(fondos)) if fondos else None

# --- ESTADOS ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'bolsa_puntos' not in st.session_state: st.session_state.bolsa_puntos = 0

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS DEFINITIVO (QUITA CLIPS Y BLOQUES BLANCOS) ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    
    header {{ visibility: hidden; }}
    
    /* 1. QUITA EL CLIP/ENLACE DE LOS TITULOS */
    .stMarkdown a {{ display: none !important; }}
    
    /* 2. QUITA LOS RECUADROS BLANCOS DE LOS INPUTS */
    div[data-testid="stNumberInput"] > div {{
        background-color: transparent !important;
        border: none !important;
    }}
    
    div[data-baseweb="input"] {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* 3. ESTILO DE LINEA ROJA FINA */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {{
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #CC0000 !important;
        border-radius: 0px !important;
        font-family: 'WuerthBold' !important;
        color: #333 !important;
    }}

    .stApp {{ background: none; }}
    
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.12;
    }}

    .card {{ 
        background-color: white; padding: 25px; border-radius: 15px; 
        border: 1px solid #ddd; box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }}
    
    .card-title {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 26px;
        text-align: center; margin-bottom: 20px;
    }}

    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 80px; text-align: center; }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div style="display: flex; background-color: white; height: 120px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;">
        <div style="width: 180px; display: flex; align-items: center; justify-content: center;">
            <img src="data:image/jpeg;base64,{logo_base64}" width="110">
        </div>
        <div style="flex: 1; background-color: #CC0000; display: flex; align-items: center; justify-content: center;">
            <h1 style="color: white; font-family: 'WuerthBold'; font-size: 35px; margin: 0;">PLAN RECAMBIO</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CALCULADORA UNIFICADA ---
st.markdown('<div class="card"><div class="card-title">Ingresar entregas del cliente</div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.2, 0.8])
with c1:
    qc = st.number_input("Máquinas Completas (20%)", 0, 100, 0, key="n1")
    qs = st.number_input("Máquinas sin batería (10%)", 0, 100, 0, key="n2")
    qb = st.number_input("Solo Batería o Cargador (5%)", 0, 100, 0, key="n3")
with c2:
    val = (qc * 20) + (qs * 10) + (qb * 5)
    st.markdown(f'<div style="text-align:center;"><b>Bolsa Disponible</b><div class="big-num">{val}%</div></div>', unsafe_allow_html=True)
    if st.button("CARGAR BOLSA", use_container_width=True):
        st.session_state.bolsa_puntos = val
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
