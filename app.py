import streamlit as st
import base64
import os
import random

# 1. Función para seleccionar fondo aleatorio de tu carpeta assets2/fondos
def get_random_bg():
    bg_dir = "assets2/fondos"
    if os.path.exists(bg_dir):
        # Filtramos solo archivos de imagen
        fondos = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if fondos:
            return os.path.join(bg_dir, random.choice(fondos))
    return None

def apply_custom_styles(bg_image_path):
    with open(bg_image_path, "rb") as f:
        data = f.read()
    base64_image = base64.b64encode(data).decode()
    
    st.markdown(
        f"""
        <style>
        /* Capa de fondo aislada con opacidad */
        .stApp {{
            background: none;
        }}
        .bg-layer {{
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -1;
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            opacity: 0.7;
        }}

        /* Contenedor Principal (El "Rectángulo de Seguridad") */
        [data-testid="block-container"] {{
            background-color: #f8f9fa;
            padding: 0rem !important;
            margin-top: 50px;
            border-radius: 10px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
            max-width: 950px;
            overflow: hidden;
        }}

        /* Estilo para las "Tarjetas" de información */
        .info-card {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
            height: 100%;
        }}

        /* Ajuste de Tabs para que parezcan los de la imagen */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0px;
            background-color: #eee;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            background-color: #f1f1f1;
            border: 1px solid #ddd;
            flex-grow: 1;
        }}
        </style>
        <div class="bg-layer"></div>
        """,
        unsafe_allow_html=True
    )

# --- Configuración Inicial ---
st.set_page_config(page_title="Würth - Plan Recambio", layout="centered")

# Aplicar fondo y estilos
fondo = get_random_bg()
if fondo:
    apply_custom_styles(fondo)

# --- Maquetación de la Interfaz ---

# Header: Logo y Título Rojo
header_html = """
<div style="display: flex; background-color: white; align-items: stretch; border-bottom: 3px solid #cc0000;">
    <div style="padding: 20px; flex: 1; display: flex; justify-content: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Wuerth_Group_logo.svg/1200px-Wuerth_Group_logo.svg.png" width="80">
    </div>
    <div style="background-color: #cc0000; flex: 3; display: flex; align-items: center; justify-content: center;">
        <h1 style="color: white; margin: 0; font-family: sans-serif; letter-spacing: 2px;">PLAN RECAMBIO</h1>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Tabs de navegación
tab1, tab2, tab3 = st.tabs(["1. Calculadora", "2. Catálogo", "3. Consolidación"])

with tab1:
    st.markdown("<h3 style='color: #cc0000; padding: 10px 0;'>Cálculo de Beneficio</h3>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.write("**Complete lo que el cliente entrega:**")
        
        # Selector dinámico basado en tus archivos de assets/productos
        path_prod = "assets/productos"
        lista_productos = [f for f in os.listdir(path_prod) if f.endswith('.png')] if os.path.exists(path_prod) else ["No hay productos"]
        
        seleccion = st.selectbox("Máquina Completa", lista_productos)
        
        if os.path.exists(os.path.join(path_prod, seleccion)):
            st.image(os.path.join(path_prod, seleccion), width=150)
        
        st.number_input("Cantidad", min_value=0, value=1)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="info-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("<p style='color: #cc0000; font-weight: bold;'>Descuento Aplicable</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px; margin: 0;'>20%</h1>", unsafe_allow_html=True)
        
        if st.button("Calcular y Aplicar"):
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
