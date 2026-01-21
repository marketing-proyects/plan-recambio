import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de recursos
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

# --- ESTILOS (SOLUCIÓN FONDO Y LOGOS) ---
bg_path = os.path.join(path_fondos, st.session_state.bg_actual) if fondos else ""
bg_base64 = get_base64(bg_path)
# Detectar extensión para el MIME type del fondo
bg_ext = "png" if bg_path.lower().endswith(".png") else "jpeg"

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* FONDO REPARADO: Gradiente mucho más transparente (0.2) para que se vea la foto */
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)), 
                    url(data:image/{bg_ext};base64,{bg_base64});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; color: #121212; }}
    
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 30px 40px;
        background: rgba(255,255,255,0.1); /* Sutil barra superior */
    }}

    .product-visual-container {{
        position: relative;
        text-align: center;
        padding: 20px;
        background: transparent;
    }}

    .discount-badge {{
        position: absolute;
        top: 0px;
        right: 15%;
        background-color: #CC0000;
        color: white;
        width: 110px;
        height: 110px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        box-shadow: 0 6px 20px rgba(204,0,0,0.5);
        z-index: 10;
        border: 3px solid white;
    }}

    .stButton>button {{
        background-color: #121212;
        color: white;
        font-family: 'WuerthBold';
        border-radius: 0px;
        padding: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
        border-color: #CC0000;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER (Logos corregidos) ---
logo_w_b64 = get_base64("logo_wurth.jpg")
logo_rs_b64 = get_base64("logo_red_stripe.png")

st.markdown(f'''
    <div class="header-container">
        <div><img src="data:image/png;base64,{logo_rs_b64}" width="320"></div>
        <div><img src="data:image/jpg;base64,{logo_w_b64}" width="180"></div>
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='color: #CC0000; font-family: WuerthExtra; font-size: 4rem; text-align: center; text-shadow: 2px 2px 4px rgba(255,255,255,0.5);'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "📝 CONSOLIDACIÓN"])

with tabs[0]:
    col_ui, col_img = st.columns([1, 1.2])
    
    with col_ui:
        st.markdown("### PARÁMETROS DE RECAMBIO")
        entrega = st.selectbox("CATEGORÍA DE ENTREGA", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
        cantidad = st.number_input("CANTIDAD", min_value=1, step=1)
        
        if st.button("CALCULAR DESCUENTO"):
            if "Completa" in entrega: st.session_state.descuento_seleccionado = 25
            elif "Parcial" in entrega: st.session_state.descuento_seleccionado = 15
            else: st.session_state.descuento_seleccionado = 10
            st.rerun()

    with col_img:
        st.markdown('<div class="product-visual-container">', unsafe_allow_html=True)
        
        if st.session_state.get('descuento_seleccionado', 0) > 0:
            st.markdown(f'''
                <div class="discount-badge">
                    <span style="font-size:45px; line-height:1;">{st.session_state.descuento_seleccionado}%</span>
                    <span style="font-size:14px;">OFF</span>
                </div>
            ''', unsafe_allow_html=True)
        
        if productos:
            img_path = os.path.join(path_prod, st.session_state.prod_actual)
            st.image(img_path, width=450)
            nombre = st.session_state.prod_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f'<p style="font-family:WuerthBold; font-size:1.8rem; color:#121212; background: rgba(255,255,255,0.4); display: inline-block; padding: 5px 15px;">{nombre}</p>', unsafe_allow_html=True)
        
        if st.button("🔄 SIGUIENTE MODELO"):
            if fondos: st.session_state.bg_actual = random.choice(fondos)
            if productos: st.session_state.prod_actual = random.choice(productos)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
