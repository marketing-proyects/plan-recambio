import streamlit as st
import base64
import random
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth Uruguay", layout="wide", initial_sidebar_state="collapsed")

# --- CARGA DE RECURSOS (Fuentes y Estilo) ---
def load_custom_assets():
    def get_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # Intentamos cargar fuentes, si fallan usamos sans-serif
    try:
        f_bold = get_base64("WuerthBold.ttf")
        f_book = get_base64("WuerthBook.ttf")
        f_extra = get_base64("WuerthExtraBoldCond.ttf")
    except:
        f_bold = f_book = f_extra = ""

    st.markdown(f"""
        <style>
        @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
        @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
        @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

        html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; background-color: #F2F2F2; }}
        h1, h2, h3 {{ font-family: 'WuerthExtra', sans-serif !important; color: #CC0000; }}
        
        .wuerth-card {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #CC0000;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.05);
            text-align: center;
        }}
        
        .stButton>button {{
            background-color: #CC0000;
            color: white;
            font-family: 'WuerthBold';
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)

load_custom_assets()

# --- LÓGICA DE IMÁGENES ALEATORIAS ---
path_productos = "assets/productos/"
if os.path.exists(path_productos):
    imagenes = [f for f in os.listdir(path_productos) if f.lower().endswith('.png')]
else:
    imagenes = []

if 'img_display' not in st.session_state and imagenes:
    st.session_state.img_display = random.choice(imagenes)

# --- HEADER ---
col_l, col_r = st.columns([1, 4])
with col_l:
    if os.path.exists("logo_wuerth.png"):
        st.image("logo_wuerth.png", width=120)
    else:
        st.subheader("WÜRTH")

with col_r:
    st.title("PLAN RECAMBIO")

# --- NAVEGACIÓN ---
tabs = st.tabs(["📊 1. CALCULADORA", "🛠️ 2. CATÁLOGO", "📝 3. CONSOLIDACIÓN"])

# --- FASE 1: CALCULADORA ---
with tabs[0]:
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### Selección de Entrega")
        tipo_e = st.selectbox("El cliente entrega:", 
                            ["Máquina Completa (Herramienta + 2 Bat + Cargador)", 
                             "Máquina Parcial (Solo Herramienta)", 
                             "Batería / Cargador suelto"])
        cantidad = st.number_input("Cantidad de unidades", min_value=1, step=1)
        
        st.info("La lógica de descuentos se aplicará automáticamente en el siguiente paso.")
        if st.button("Calcular Beneficio"):
            st.success("Descuento pre-calculado. Revise el catálogo.")

    with col2:
        st.markdown('<div class="wuerth-card">', unsafe_allow_html=True)
        if imagenes:
            img_path = os.path.join(path_productos, st.session_state.img_display)
            st.image(img_path, use_container_width=True)
            # Mostrar nombre del producto basado en el archivo
            nombre_limpio = st.session_state.img_display.replace('.png', '').replace('_', ' ').upper()
            st.markdown(f"**NUEVA GENERACIÓN: {nombre_limpio}**")
        
        if st.button("🔄 Ver otra máquina"):
            st.session_state.img_display = random.choice(imagenes)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- FASES SIGUIENTES (Placeholders) ---
with tabs[1]:
    st.subheader("Modelos disponibles para el recambio")
    st.write("Aquí aparecerá la lista de precios con el descuento aplicado.")

with tabs[2]:
    st.subheader("Resumen del Pedido")
    st.caption("Nota: Precios sujetos a variaciones. No incluye impuestos ni fletes.")
