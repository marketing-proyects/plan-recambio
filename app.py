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
if 'nombre_cliente' not in st.session_state:
    st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state:
    st.session_state.numero_cliente = ""

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS PARA CONVERTIR BLOQUES EN LÍNEAS FINAS ---
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

    /* ELIMINACIÓN DE FONDO DE INPUTS Y CONVERSIÓN A LÍNEA FINA */
    div[data-testid="stTextInput"] {{
        background-color: transparent !important;
    }}
    
    div[data-testid="stTextInput"] input {{
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #CC0000 !important; /* Línea roja fina */
        border-radius: 0px !important;
        padding: 5px 0px !important;
        font-family: 'WuerthBold' !important;
        font-size: 18px !important;
        color: #333 !important;
    }}

    div[data-testid="stTextInput"] label {{
        font-family: 'WuerthBold' !important;
        color: #CC0000 !important;
        font-size: 14px !important;
    }}

    /* ELIMINAR BLOQUES BLANCOS RESIDUALES */
    [data-testid="stVerticalBlock"] > div:empty {{ display: none !important; }}
    .st-emotion-cache-1kyx60e {{ display: none !important; }} 

    .main-body {{
        background-color: transparent;
        padding-bottom: 40px;
    }}

    /* CABECERA */
    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
        overflow: hidden; margin-bottom: 10px;
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
        gap: 10px; padding: 10px 20px; 
        background-color: transparent !important; 
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 20px !important; 
        height: 60px; color: #666; flex: 1; text-align: center;
        background-color: #e8e8e8;
        border-radius: 12px 12px 0 0 !important; 
        border: none !important;
    }}
    
    .stTabs [aria-selected="true"] {{ 
        color: #CC0000 !important; 
        background-color: #f5f5f5 !important;
        border-bottom: none !important;
    }}

    /* TARJETAS */
    .card {{ 
        background-color: white; padding: 30px; border-radius: 15px; 
        margin: 10px 20px 20px 20px; border: 1px solid #ddd;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }}
    
    .big-num {{ 
        color: #CC0000; font-family: 'WuerthBold'; 
        font-size: 100px; text-align: center; 
        line-height: 1; margin-bottom: 25px;
    }}
    
    .footer-logo {{ 
        position: fixed; bottom: 20px; left: 20px; width: 280px; 
        pointer-events: none; z-index: 10; opacity: 0.9;
    }}
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

st.markdown('<div class="main-body">', unsafe_allow_html=True)

# --- FICHA DE CLIENTE (TRANSFORMADA EN LÍNEAS) ---
c_nom, c_num = st.columns([1.5, 1])
with c_nom:
    st.session_state.nombre_cliente = st.text_input("NOMBRE DEL CLIENTE", value=st.session_state.nombre_cliente, key="in_nom")
with c_num:
    st.session_state.numero_cliente = st.text_input("N° CLIENTE", value=st.session_state.numero_cliente, key="in_num")

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

with t2:
    st.markdown("<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:15px 0;'>Seleccionar Máquina Nueva</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    p = "assets/productos"
    if os.path.exists(p):
        prods = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if prods:
            sel = st.selectbox("Catálogo de productos:", prods)
            col_img, col_sel = st.columns(2)
            with col_img:
                img_path = os.path.join(p, sel)
                try:
                    st.image(img_path, width=300)
                except:
                    st.warning("Error al cargar imagen.")
            with col_sel:
                disp = st.session_state.bolsa_puntos
                st.write(f"**Puntos disponibles:** {disp}%")
                dto = st.slider("Asignar descuento (%)", 0, 30, value=min(disp, 30))
                if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                    if disp >= dto:
                        st.session_state.carrito.append({"prod": sel, "dto": dto})
                        st.session_state.bolsa_puntos -= dto
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown(f"<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:15px 0;'>Pedido: {st.session_state.nombre_cliente}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.session_state.carrito:
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc = st.columns([3, 1, 1])
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"**-{item['dto']}%**")
            if cc.button("Quitar", key=f"del_{i}"):
                st.session_state.bolsa_puntos += item['dto']
                st.session_state.carrito.pop(i)
                st.rerun()
        st.write("---")
        st.write(f"**Bolsa residual:** {st.session_state.bolsa_puntos}%")
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
