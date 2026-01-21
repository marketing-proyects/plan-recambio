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

# Inyección de Estilo
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; background-color: #F2F2F2; }}
    h1, h2, h3, .stMetric label {{ font-family: 'WuerthExtra', sans-serif !important; color: #CC0000; text-transform: uppercase; }}
    
    .wuerth-card {{
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-bottom: 6px solid #CC0000;
    }}
    
    .stButton>button {{
        background-color: #CC0000;
        color: white;
        font-family: 'WuerthBold';
        border: none;
        width: 100%;
    }}
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE IMÁGENES ---
path_img = "assets/productos/"
imagenes = [f for f in os.listdir(path_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(path_img) else []

if 'img_actual' not in st.session_state and imagenes:
    st.session_state.img_actual = random.choice(imagenes)

# --- INTERFAZ ---
# Header con Logo JPG
col_logo, col_tit = st.columns([1, 4])
with col_logo:
    if os.path.exists("logo_wurth.jpg"):
        st.image("logo_wurth.jpg", width=160)
with col_tit:
    st.title("Plan Recambio")

tabs = st.tabs(["📊 1. CALCULADORA", "🛠️ 2. CATÁLOGO", "📝 3. CONSOLIDACIÓN"])

with tabs[0]:
    col_izq, col_der = st.columns([1.2, 1])
    
    with col_izq:
        st.subheader("Configuración de Recambio")
        st.selectbox("Tipo de equipo entregado", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
        st.number_input("Cantidad", min_value=1, step=1)
        st.button("Calcular Beneficio")
        st.info("La lógica comercial se integrará en esta sección una vez definida.")

    with col_der:
        st.markdown('<div class="wuerth-card">', unsafe_allow_html=True)
        if imagenes:
            st.image(os.path.join(path_img, st.session_state.img_actual), use_container_width=True)
            nombre = st.session_state.img_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f"### {nombre}")
        
        if st.button("🔄 Cambiar Vista de Producto"):
            st.session_state.img_actual = random.choice(imagenes)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
