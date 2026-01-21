import streamlit as st
import base64
import os
import random
import time
from datetime import datetime, timedelta

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

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'bolsa_puntos' not in st.session_state:
    st.session_state.bolsa_puntos = 0

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS PARA EL RELOJ Y LIMPIEZA ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    
    header {{ visibility: hidden; }}
    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 950px;
    }}
    
    .stApp {{ background: none; }}
    
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.12;
    }}

    .main-body {{ background-color: transparent; padding-bottom: 40px; }}

    /* ESTILO RELOJ DIGITAL */
    .timer-label {{
        background-color: #333; color: white;
        font-family: 'WuerthBold'; font-size: 18px;
        height: 60px; display: flex; align-items: center; justify-content: center;
        border-radius: 10px 0 0 10px; border-right: 1px solid #555;
    }}
    .timer-clock {{
        background-color: #222; color: #00FF00; /* Verde digital */
        font-family: 'Courier New', Courier, monospace; font-size: 35px; font-weight: bold;
        height: 60px; display: flex; align-items: center; justify-content: center;
        border-radius: 0 10px 10px 0; box-shadow: inset 0 0 10px #000;
    }}

    /* CABECERA */
    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
        overflow: hidden; margin-bottom: 5px;
    }}
    .header-logo {{ width: 220px; display: flex; align-items: center; justify-content: center; }}
    .header-title {{
        flex: 1; background-color: #CC0000; 
        display: flex; align-items: center; justify-content: center; 
    }}
    .header-title h1 {{ 
        color: white !important; font-family: 'WuerthBold' !important; 
        font-size: 44px !important; margin: 0 !important; text-align: center;
    }}

    /* MENÚ */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; padding: 10px 20px; }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 20px !important; 
        height: 60px; color: #666; flex: 1; text-align: center;
        background-color: #e8e8e8; border-radius: 12px 12px 0 0 !important; 
    }}
    .stTabs [aria-selected="true"] {{ 
        color: #CC0000 !important; background-color: #f5f5f5 !important;
    }}

    .card {{ 
        background-color: white; padding: 30px; border-radius: 15px; 
        margin: 10px 20px 20px 20px; border: 1px solid #ddd;
    }}
    
    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 100px; text-align: center; }}
    
    .footer-logo {{ position: fixed; bottom: 20px; left: 20px; width: 280px; opacity: 0.9; }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="header-container">
        <div class="header-logo"><img src="data:image/jpeg;base64,{logo_base64}" width="130"></div>
        <div class="header-title"><h1>PLAN RECAMBIO</h1></div>
    </div>
    """, unsafe_allow_html=True)

# --- RELOJ REGRESIVO (Ocupando los bloques blancos) ---
col_t1, col_t2 = st.columns([1.8, 1])

# Lógica del tiempo (puedes cambiar esta fecha a la del fin de la promo)
fin_promo = datetime(2026, 2, 28, 23, 59, 59)
ahora = datetime.now()
restante = fin_promo - ahora

dias = restante.days
horas, rem = divmod(restante.seconds, 3600)
minutos, segundos = divmod(rem, 60)
tiempo_str = f"{dias}d {horas:02d}:{minutos:02d}:{segundos:02d}"

with col_t1:
    st.markdown(f'<div class="timer-label">PLAN RECAMBIO - TIEMPO RESTANTE</div>', unsafe_allow_html=True)
with col_t2:
    st.markdown(f'<div class="timer-clock">{tiempo_str}</div>', unsafe_allow_html=True)

st.markdown('<div class="main-body">', unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "🛒 PEDIDO"])

with t1:
    st.markdown("<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:15px 0;'>Ingresar entregas del cliente</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        qc = st.number_input("Máquinas Completas (20% c/u)", 0, 100, 0, key="n1")
        qs = st.number_input("Máquinas sin batería (10% c/u)", 0, 100, 0, key="n2")
        qb = st.number_input("Solo Batería o Cargador (5% c/u)", 0, 100, 0, key="n3")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
        val = (qc * 20) + (qs * 10) + (qb * 5)
        st.write("**Bolsa Disponible**")
        st.markdown(f'<div class="big-num">{val}%</div>', unsafe_allow_html=True)
        if st.button("SUMATORIA DE DESCUENTOS", use_container_width=True):
            st.session_state.bolsa_puntos = val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ... (El resto del código de Catálogo y Pedido se mantiene igual)

st.markdown('</div>', unsafe_allow_html=True)

if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)

# Script para actualizar el reloj cada segundo (opcional, consume recursos)
# time.sleep(1)
# st.rerun()
