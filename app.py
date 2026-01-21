import streamlit as st
import base64
import os
import random

# --- FUNCIONES DE SOPORTE ---

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_random_bg():
    # Buscamos en la raíz o assets según tu estructura
    bg_dir = "assets2/fondos" if os.path.exists("assets2/fondos") else "."
    fondos = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return os.path.join(bg_dir, random.choice(fondos)) if fondos else None

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

# Selección de fondo aleatorio
fondo_path = get_random_bg()
fondo_base64 = get_base64(fondo_path) if fondo_path else ""

# Carga de imágenes para la interfaz
logo_wurth = get_base64("logo_wurth.jpg") if os.path.exists("logo_wurth.jpg") else ""
red_stripe = get_base64("logo_red_stripe.png") if os.path.exists("logo_red_stripe.png") else ""

# --- CSS PERSONALIZADO (Fuentes y Maquetación) ---
st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'WuerthBold';
        src: url('data:font/ttf;base64,{get_base64("WuerthBold.ttf")}');
    }}
    @font-face {{
        font-family: 'WuerthBook';
        src: url('data:font/ttf;base64,{get_base64("WuerthBook.ttf")}');
    }}

    /* Fondo Aleatorio con Opacidad Aislada */
    .stApp {{
        background: none;
    }}
    .bg-layer {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        background-image: url("data:image/png;base64,{fondo_base64}");
        background-size: cover;
        background-position: center;
        opacity: 0.7;
    }}

    /* Contenedor Principal (Rectángulo de Seguridad) */
    [data-testid="block-container"] {{
        background-color: #F2F2F2;
        padding: 0 !important;
        margin-top: 30px;
        border-radius: 8px;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.4);
        max-width: 900px;
        font-family: 'WuerthBook', sans-serif;
    }}

    /* Cabecera Exacta */
    .header-container {{
        display: flex;
        background-color: white;
        height: 180px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        overflow: hidden;
    }}
    .header-logo {{
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }}
    .header-title {{
        flex: 2.5;
        background-color: #CC0000;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .header-title h1 {{
        color: white !important;
        font-family: 'WuerthBold', sans-serif;
        font-size: 60px !important;
        margin: 0;
        letter-spacing: 1px;
    }}

    /* Estilo de Tarjetas Blancas */
    .card {{
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        height: 100%;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }}

    /* Franja Roja inferior decorativa */
    .footer-stripe {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 200px;
        opacity: 0.8;
    }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- ESTRUCTURA VISUAL ---

# 1. Cabecera Estilo Würth
st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            <img src="data:image/jpeg;base64,{logo_wurth}" width="120">
        </div>
        <div class="header-title">
            <h1>PLAN RECAMBIO</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. Navegación (Tabs)
tab1, tab2, tab3 = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Consolidación"])

with tab1:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; margin-top: 20px;'>Cálculo de Beneficio</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<p style='color: #CC0000; font-family: WuerthBold;'>Complete lo que el cliente entrega:</p>", unsafe_allow_html=True)
        
        # Selector de productos desde assets/productos
        prod_path = "assets/productos"
        opciones = os.listdir(prod_path) if os.path.exists(prod_path) else ["Sin archivos"]
        seleccion = st.selectbox("Máquina Completa", opciones)
        
        if os.path.exists(os.path.join(prod_path, seleccion)):
            st.image(os.path.join(prod_path, seleccion), width=180)
        
        st.number_input("Cantidad", min_value=1, value=1)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='color: #CC0000; font-family: WuerthBold;'>Descuento Aplicable</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 100px; font-family: WuerthBold; color: #CC0000; margin: 10px 0;'>20%</h1>", unsafe_allow_html=True)
        
        if st.button("Calcular y Aplicar"):
            st.success("¡Descuento aplicado con éxito!")
        st.markdown('</div>', unsafe_allow_html=True)

# 3. Logo Red Stripe (Decorativo en esquina)
if red_stripe:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe}" class="footer-stripe">', unsafe_allow_html=True)
