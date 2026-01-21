import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth Black Label", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

f_bold = get_base64("WuerthBold.ttf")
f_book = get_base64("WuerthBook.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")

# --- LÓGICA DE DIRECTORIOS ---
path_fondos = "assets2/" 
path_prod = "assets/productos/"

fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = [f for f in os.listdir(path_prod) if f.lower().endswith(('.png'))] if os.path.exists(path_prod) else []

if 'bg_actual' not in st.session_state and fondos:
    st.session_state.bg_actual = random.choice(fondos)
if 'prod_actual' not in st.session_state and productos:
    st.session_state.prod_actual = random.choice(productos)

# --- ESTILOS "BLACK LABEL" ---
bg_base64 = get_base64(os.path.join(path_fondos, st.session_state.bg_actual)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con opacidad al 75% (Punto 1) */
    .stApp {{
        background: linear-gradient(rgba(18, 18, 18, 0.75), rgba(18, 18, 18, 0.75)), 
                    url(data:image/jpg;base64,{bg_base64});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; color: white; }}
    
    /* Contenedor de Logos (Punto 2) */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 30px;
    }}

    .product-card {{
        position: relative;
        background-color: rgba(30, 30, 30, 0.85); /* Gris muy oscuro con transparencia */
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }}

    /* Badge de Descuento Black & Red */
    .discount-badge {{
        position: absolute;
        top: -15px;
        right: -15px;
        background-color: #CC0000;
        color: white;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        box-shadow: 0 5px 20px rgba(204,0,0,0.6);
        z-index: 100;
        border: 3px solid #1e1e1e;
    }}

    /* Botones Estilo Negro/Gris */
    .stButton>button {{
        background-color: #000000;
        color: white;
        font-family: 'WuerthBold';
        border: 1px solid #444;
        border-radius: 4px;
        padding: 12px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{
        background-color: #CC0000; /* Rojo solo en el hover para impacto */
        border: 1px solid #CC0000;
        color: white;
    }}

    /* Estilo de los Tabs en modo oscuro */
    .stTabs [data-baseweb="tab-list"] {{ background-color: transparent; }}
    .stTabs [data-baseweb="tab"] {{
        color: #999;
        font-family: 'WuerthBold';
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color: white; }}
    .stTabs [aria-selected="true"] {{ color: white !important; border-bottom-color: #CC0000 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER (Punto 2: Re-ubicación de logos) ---
# Usamos HTML para tener control total de la posición
logo_w_b64 = get_base64("logo_wurth.jpg")
logo_rs_b64 = get_base64("logo_red_stripe.jpg")

st.markdown(f'''
    <div class="header-container">
        <div style="flex: 1;">
            <img src="data:image/jpg;base64,{logo_rs_b64}" width="220" style="filter: brightness(1.1);">
        </div>
        <div style="flex: 1; text-align: right;">
            <img src="data:image/jpg;base64,{logo_w_b64}" width="90" style="opacity: 0.8;">
        </div>
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='color: white; font-family: WuerthExtra; font-size: 3rem; text-align: center; margin-bottom: 30px;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tabs = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "📝 CONSOLIDACIÓN"])

with tabs[0]:
    col_ui, col_img = st.columns([1, 1.2])
    
    with col_ui:
        st.markdown("### CONFIGURACIÓN")
        entrega = st.selectbox("EQUIPO ENTREGADO", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
        cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
        
        if st.button("CALCULAR BENEFICIO"):
            if "Completa" in entrega: st.session_state.descuento_seleccionado = 25
            elif "Parcial" in entrega: st.session_state.descuento_seleccionado = 15
            else: st.session_state.descuento_seleccionado = 10
            st.rerun()

    with col_img:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        if st.session_state.get('descuento_seleccionado', 0) > 0:
            st.markdown(f'''<div class="discount-badge"><span style="font-size:38px;">{st.session_state.descuento_seleccionado}%</span><span style="font-size:10px;">OFF</span></div>''', unsafe_allow_html=True)
        
        if productos:
            img_path = os.path.join(path_prod, st.session_state.prod_actual)
            st.image(img_path, width=380)
            nombre = st.session_state.prod_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f'<p style="font-family:WuerthBold; font-size:1.4rem; color:white; letter-spacing:1px;">{nombre}</p>', unsafe_allow_html=True)
        
        if st.button("🔄 ACTUALIZAR VISTA"):
            if fondos: st.session_state.bg_actual = random.choice(fondos)
            if productos: st.session_state.prod_actual = random.choice(productos)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
