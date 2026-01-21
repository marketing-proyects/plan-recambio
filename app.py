import streamlit as st
import base64
import os
import random
from datetime import datetime

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

# --- INICIALIZACIÓN ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'bolsa_puntos' not in st.session_state: st.session_state.bolsa_puntos = 0

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS RADICAL (ELIMINA FRANJAS BLANCAS) ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    
    header {{ visibility: hidden; }}
    
    /* Eliminar gaps de Streamlit */
    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
    [data-testid="stHorizontalBlock"] {{ gap: 0rem !important; }}
    .st-emotion-cache-1kyx60e {{ display: none !important; }}
    .st-emotion-cache-z5fcl4 {{ padding: 0 !important; }}
    
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

    /* BARRA DE RELOJ */
    .timer-container {{
        display: flex; width: 100%; height: 50px; margin-bottom: 5px;
    }}
    .timer-label {{
        flex: 1.8; background-color: #333; color: white;
        font-family: 'WuerthBold'; font-size: 16px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 8px 0 0 8px;
    }}
    .timer-clock {{
        flex: 1; background-color: #222; color: #00FF00;
        font-family: 'Courier New', monospace; font-size: 26px; font-weight: bold;
        display: flex; align-items: center; justify-content: center;
        border-radius: 0 8px 8px 0; border: 1px solid #444;
    }}

    /* INPUTS ESTILO LÍNEA (Sin etiquetas que ocupen espacio) */
    div[data-testid="stTextInput"] label {{ display: none !important; }}
    div[data-testid="stTextInput"] input {{
        background-color: rgba(255,255,255,0.7) !important;
        border: none !important;
        border-bottom: 2px solid #CC0000 !important;
        border-radius: 0px !important;
        font-family: 'WuerthBold' !important;
        height: 45px !important;
    }}

    /* CABECERA */
    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
        overflow: hidden;
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

    .stTabs [data-baseweb="tab-list"] {{ gap: 5px; padding: 10px 20px; }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 18px !important; 
        height: 50px; color: #666; flex: 1; background-color: #e8e8e8;
        border-radius: 10px 10px 0 0 !important;
    }}
    .stTabs [aria-selected="true"] {{ 
        color: #CC0000 !important; background-color: #f5f5f5 !important;
    }}

    .card {{ 
        background-color: white; padding: 20px; border-radius: 15px; 
        margin: 5px 20px; border: 1px solid #ddd;
    }}
    
    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 90px; text-align: center; line-height: 1; }}
    
    .footer-logo {{ position: fixed; bottom: 20px; left: 20px; width: 280px; pointer-events: none; opacity: 0.9; }}
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

# --- BARRA RELOJ (Ocupa el primer bloque) ---
col_t1, col_t2 = st.columns([1.8, 1])
fin_promo = datetime(2026, 2, 28, 23, 59, 59)
restante = fin_promo - datetime.now()
t_str = f"{restante.days}d {restante.seconds // 3600:02d}:{(restante.seconds % 3600) // 60:02d}:{restante.seconds % 60:02d}"

with col_t1:
    st.markdown(f'<div class="timer-container"><div class="timer-label">PLAN RECAMBIO - TIEMPO RESTANTE</div>', unsafe_allow_html=True)
with col_t2:
    st.markdown(f'<div class="timer-clock">{t_str}</div></div>', unsafe_allow_html=True)

# --- DATOS CLIENTE (Ocupa el segundo bloque, pegado al reloj) ---
c_nom, c_num = st.columns([1.5, 1])
with c_nom:
    nombre_c = st.text_input("NOMBRE", placeholder="NOMBRE DEL CLIENTE", label_visibility="collapsed")
with c_num:
    numero_c = st.text_input("NUMERO", placeholder="N° CLIENTE", label_visibility="collapsed")

# --- CONTENIDO ---
t1, t2, t3 = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "🛒 PEDIDO"])

with t1:
    st.markdown("<h4 style='color:#CC0000; font-family:WuerthBold; text-align:center; margin:10px 0;'>Ingresar entregas del cliente</h4>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        qc = st.number_input("Máquinas Completas (20%)", 0, 100, 0, key="n1")
        qs = st.number_input("Máquinas sin batería (10%)", 0, 100, 0, key="n2")
        qb = st.number_input("Solo Batería o Cargador (5%)", 0, 100, 0, key="n3")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
        val = (qc * 20) + (qs * 10) + (qb * 5)
        st.write("**Descuento Acumulado**")
        st.markdown(f'<div class="big-num">{val}%</div>', unsafe_allow_html=True)
        if st.button("SUMATORIA DE DESCUENTOS", use_container_width=True):
            st.session_state.bolsa_puntos = val
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ... (El código de las demás pestañas se mantiene, adaptado a este estilo compacto)

if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
