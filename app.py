import streamlit as st
import base64
import os
import random
from PIL import Image

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

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'bolsa_puntos' not in st.session_state:
    st.session_state.bolsa_puntos = 0

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS DEFINITIVO (ELIMINACIÓN DE ESPACIOS) ---
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

    /* ELIMINACIÓN DE ESPACIOS FANTASMA ENTRE ELEMENTOS */
    [data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
    
    .main-body {{
        background-color: rgba(242, 242, 242, 0.98);
        border-radius: 0 0 12px 12px;
        box-shadow: 0px 20px 60px rgba(0,0,0,0.4);
        padding: 20px;
        margin-top: 0px;
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
        font-size: 44px !important; margin: 0 !important;
        text-align: center; line-height: 1.1;
    }}

    /* MENÚ */
    .stTabs [data-baseweb="tab-list"] {{ 
        gap: 8px; padding: 0px 0px 10px 0px; 
        background-color: transparent !important; 
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 18px !important; 
        height: 55px; color: #444; flex: 1; text-align: center;
        background-color: #e8e8e8;
        border-radius: 10px 10px 0 0 !important; 
        border: none !important;
    }}
    .stTabs [aria-selected="true"] {{ 
        color: #CC0000 !important; 
        background-color: white !important;
        border-bottom: none !important;
    }}

    /* TARJETAS */
    .card {{ 
        background-color: white; padding: 25px; border-radius: 12px; 
        margin-bottom: 15px; border: 1px solid #ddd;
    }}
    
    .big-num {{ 
        color: #CC0000; font-family: 'WuerthBold'; 
        font-size: 90px; text-align: center; 
        line-height: 1; margin-bottom: 20px;
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; left: 20px; width: 260px; opacity: 0.9; }}
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

# --- CUERPO DE LA APP ---
# Usamos un solo bloque contenedor para evitar franjas blancas entre secciones
with st.container():
    st.markdown('<div class="main-body">', unsafe_allow_html=True)
    
    # FICHA DE CLIENTE: Ubicada DENTRO de los rectángulos que veías vacíos
    st.markdown('<div class="card" style="padding: 15px; margin-top: 10px;">', unsafe_allow_html=True)
    c_cli, c_num = st.columns([2, 1])
    with c_cli:
        nombre = st.text_input("Nombre del Cliente", placeholder="Escriba aquí...", key="client_name")
    with c_num:
        numero = st.text_input("N° de Cliente", placeholder="000000", key="client_id")
    st.markdown('</div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "🛒 PEDIDO"])

    with t1:
        st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:10px 0;'>Ingresar entregas</h3>", unsafe_allow_html=True)
        col_inputs, col_visual = st.columns([1.1, 0.9])
        
        with col_inputs:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            qc = st.number_input("Máquina Completa (20%)", 0, 50, 0, key="in1")
            qs = st.number_input("Máquina sin batería (10%)", 0, 50, 0, key="in2")
            qb = st.number_input("Batería o Cargador (5%)", 0, 50, 0, key="in3")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_visual:
            st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
            puntos = (qc * 20) + (qs * 10) + (qb * 5)
            st.write("Bolsa Total Acumulada")
            st.markdown(f'<div class="big-num">{puntos}%</div>', unsafe_allow_html=True)
            if st.button("CONFIRMAR DESCUENTOS", use_container_width=True):
                st.session_state.bolsa_puntos = puntos
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        # Contenido del Catálogo
        st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:10px 0;'>Catálogo de Herramientas</h3>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"Vincular compra para: **{nombre if nombre else 'Cliente nuevo'}**")
        # Aquí iría el selector de imágenes de productos
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        # Contenido del Pedido
        st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:10px 0;'>Resumen del Pedido</h3>", unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"Cliente: {nombre} ({numero})")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# LOGO RED STRIPE (Izquierda abajo, doble tamaño)
if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
