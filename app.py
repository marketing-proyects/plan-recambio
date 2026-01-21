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

# --- ESTILOS BLACK LABEL ---
bg_base64 = get_base64(os.path.join(path_fondos, st.session_state.bg_actual)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con opacidad al 75% sobre NEGRO */
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                    url(data:image/jpg;base64,{bg_base64});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; color: white; }}
    
    /* Header con logos posicionados */
    .header-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px;
    }}

    /* ELIMINACIÓN DEL CUADRO GRIS: Contenedor Invisible */
    .product-visual-container {{
        position: relative;
        text-align: center;
        padding: 20px;
        background: transparent; /* Eliminamos el fondo gris/blanco */
    }}

    .discount-badge {{
        position: absolute;
        top: 0px;
        right: 15%;
        background-color: #CC0000;
        color: white;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        box-shadow: 0 4px 20px rgba(204,0,0,0.6);
        z-index: 10;
        border: 2px solid white;
    }}

    /* Botoneras Estilo Negro Label */
    .stButton>button {{
        background-color: #121212;
        color: white;
        font-family: 'WuerthBold';
        border: 1px solid #333;
        border-radius: 0px; /* Estilo más industrial */
        padding: 15px;
        width: 100%;
        text-transform: uppercase;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #CC0000;
        border: 1px solid #CC0000;
    }}

    /* Input styling */
    .stSelectbox label, .stNumberInput label {{ color: #999 !important; font-family: 'WuerthBold'; }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
logo_w_b64 = get_base64("logo_wurth.jpg")
logo_rs_b64 = get_base64("logo_red_stripe.jpg")

st.markdown(f'''
    <div class="header-container">
        <div><img src="data:image/jpg;base64,{logo_rs_b64}" width="280"></div>
        <div><img src="data:image/jpg;base64,{logo_w_b64}" width="80"></div>
    </div>
''', unsafe_allow_html=True)

st.markdown("<h1 style='color: white; font-family: WuerthExtra; font-size: 3rem; text-align: center;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

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
        # Aquí eliminamos el div con fondo y usamos uno transparente
        st.markdown('<div class="product-visual-container">', unsafe_allow_html=True)
        
        # Badge flotante
        if st.session_state.get('descuento_seleccionado', 0) > 0:
            st.markdown(f'''
                <div class="discount-badge">
                    <span style="font-size:42px; line-height:1;">{st.session_state.descuento_seleccionado}%</span>
                    <span style="font-size:12px;">OFF</span>
                </div>
            ''', unsafe_allow_html=True)
        
        if productos:
            img_path = os.path.join(path_prod, st.session_state.prod_actual)
            # La imagen ahora flota sobre el fondo de la app al 75%
            st.image(img_path, width=400)
            nombre = st.session_state.prod_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f'<p style="font-family:WuerthBold; font-size:1.5rem; color:white; margin-top:10px;">{nombre}</p>', unsafe_allow_html=True)
        
        if st.button("🔄 ACTUALIZAR VISTA"):
            if fondos: st.session_state.bg_actual = random.choice(fondos)
            if productos: st.session_state.prod_actual = random.choice(productos)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
