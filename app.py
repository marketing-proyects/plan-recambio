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

# Carga de Tipografías
f_bold = get_base64("WuerthBold.ttf")
f_book = get_base64("WuerthBook.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")

# --- LÓGICA DE DIRECTORIOS ---
path_fondos = "assets2/"  # Carpeta exclusiva para fondos
path_prod = "assets/productos/"

fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))] if os.path.exists(path_fondos) else []
productos = [f for f in os.listdir(path_prod) if f.lower().endswith(('.png'))] if os.path.exists(path_prod) else []

# Persistencia de imágenes en la sesión
if 'bg_actual' not in st.session_state and fondos:
    st.session_state.bg_actual = random.choice(fondos)
if 'prod_actual' not in st.session_state and productos:
    st.session_state.prod_actual = random.choice(productos)

# --- ESTILOS CSS ---
bg_base64 = get_base64(os.path.join(path_fondos, st.session_state.bg_actual)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    /* Fondo con imagen aleatoria y opacidad controlada */
    .stApp {{
        background: linear-gradient(rgba(242, 242, 242, 0.88), rgba(242, 242, 242, 0.88)), 
                    url(data:image/jpg;base64,{bg_base64});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; }}
    
    .logo-box {{ padding: 15px; display: flex; align-items: center; gap: 20px; }}

    .product-card {{
        position: relative;
        background-color: rgba(255, 255, 255, 0.98);
        padding: 45px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.12);
        margin-top: 10px;
    }}

    .discount-badge {{
        position: absolute;
        top: -20px;
        right: -20px;
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
        box-shadow: 0 5px 15px rgba(204,0,0,0.4);
        z-index: 100;
        border: 5px solid white;
    }}

    .discount-badge .num {{ font-size: 40px; line-height: 1; }}
    .discount-badge .off {{ font-size: 12px; font-family: 'WuerthBold'; }}

    .stButton>button {{
        background-color: #CC0000;
        color: white;
        font-family: 'WuerthBold';
        border-radius: 6px;
        padding: 12px;
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER (Doble Logo y Título) ---
c_logos, c_tit = st.columns([2, 3])
with c_logos:
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("logo_wurth.jpg"): st.image("logo_wurth.jpg", width=140)
    with col2:
        if os.path.exists("logo_red_stripe.jpg"): st.image("logo_red_stripe.jpg", width=140)
    st.markdown('</div>', unsafe_allow_html=True)

with c_tit:
    st.markdown("<h1 style='color: #CC0000; text-align: right; font-family: WuerthExtra; font-size: 3.5rem; margin-top:20px;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tabs = st.tabs(["📊 1. CALCULADORA", "🛠️ 2. CATÁLOGO", "📝 3. CONSOLIDACIÓN"])

# --- FASE 1: CALCULADORA ---
with tabs[0]:
    col_ui, col_img = st.columns([1, 1.2])
    
    with col_ui:
        st.subheader("Configuración de Beneficio")
        # Punto 1: Nombres simplificados
        entrega = st.selectbox("Equipo entregado", 
                             ["Máquina Completa", 
                              "Máquina Parcial", 
                              "Batería / Cargador"])
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        
        if st.button("CALCULAR DESCUENTO"):
            if "Completa" in entrega: st.session_state.descuento_seleccionado = 25
            elif "Parcial" in entrega: st.session_state.descuento_seleccionado = 15
            else: st.session_state.descuento_seleccionado = 10
            st.rerun()

    with col_img:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        # Badge de % dinámico
        if st.session_state.get('descuento_seleccionado', 0) > 0:
            st.markdown(f'''
                <div class="discount-badge">
                    <span class="num">{st.session_state.descuento_seleccionado}%</span>
                    <span class="off">OFF</span>
                </div>
            ''', unsafe_allow_html=True)
        
        if productos:
            img_path = os.path.join(path_prod, st.session_state.prod_actual)
            st.image(img_path, width=380)
            nombre = st.session_state.prod_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f'<p style="font-family:WuerthBold; font-size:1.4rem; color:#333;">{nombre}</p>', unsafe_allow_html=True)
        
        if st.button("🔄 ACTUALIZAR VISTA"):
            if fondos: st.session_state.bg_actual = random.choice(fondos)
            if productos: st.session_state.prod_actual = random.choice(productos)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
