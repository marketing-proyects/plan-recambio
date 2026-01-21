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
    # Fallback al directorio actual si no existe la carpeta específica
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

# --- CSS DEFINITIVO ---
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

    .main-body {{
        background-color: rgba(242, 242, 242, 0.98);
        border-radius: 0 0 12px 12px;
        box-shadow: 0px 20px 60px rgba(0,0,0,0.4);
        padding-bottom: 40px;
    }}

    /* CABECERA: Título centrado y corregido */
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
        font-size: 48px !important; /* Ajustado para evitar desconfiguración */
        margin: 0 !important; padding: 0 !important;
        text-align: center; line-height: 1.2;
        letter-spacing: 1px;
    }}

    /* MENÚ INSTITUCIONAL */
    .stTabs [data-baseweb="tab-list"] {{ 
        gap: 0; padding: 0; background-color: #e0e0e0; width: 100%;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 22px !important; 
        height: 70px; color: #444; flex: 1; text-align: center;
    }}
    .stTabs [aria-selected="true"] {{ 
        color: #CC0000 !important; border-bottom: 4px solid #CC0000 !important;
        background-color: #f8f8f8;
    }}

    .card {{ background-color: white; padding: 30px; border-radius: 15px; margin: 20px; border: 1px solid #ddd; }}
    
    /* DESCUENTO CON ESPACIADO AL BOTÓN */
    .big-num {{ 
        color: #CC0000; font-family: 'WuerthBold'; 
        font-size: 110px; text-align: center; 
        line-height: 1; margin-bottom: 30px; /* Espacio extra abajo */
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; right: 20px; width: 140px; pointer-events: none; }}
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

with st.container():
    st.markdown('<div class="main-body">', unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "🛒 PEDIDO"])

    with t1:
        st.markdown("<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:20px 0;'>Ingresar entregas del cliente</h2>", unsafe_allow_html=True)
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
            # Cambio de nombre solicitado
            if st.button("SUMATORIA DE DESCUENTOS", use_container_width=True):
                st.session_state.bolsa_puntos = val
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown("<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:20px 0;'>Seleccionar Máquina Nueva</h2>", unsafe_allow_html=True)
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
            else:
                st.warning("No hay productos en la carpeta.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown("<h2 style='color:#CC0000; font-family:WuerthBold; text-align:center; padding:20px 0;'>Resumen del Pedido</h2>", unsafe_allow_html=True)
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
            if st.button("Borrar Todo"):
                st.session_state.carrito = []
                st.rerun()
        else:
            st.info("El pedido está vacío.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
