import streamlit as st
import base64
import os
import random

# 1. Lógica de selección aleatoria de fondo
def get_random_bg():
    bg_dir = "assets2/fondos"
    if os.path.exists(bg_dir):
        fondos = [f for f in os.listdir(bg_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if fondos:
            return os.path.join(bg_dir, random.choice(fondos))
    return None

def set_bg_with_opacity(image_file, opacity=0.7):
    with open(image_file, "rb") as f:
        data = f.read()
    base64_image = base64.b64encode(data).decode()
    
    # CSS para capa de fondo aislada
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: none;
        }}
        .bg-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            overflow: hidden;
        }}
        .bg-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: {opacity};
        }}
        
        /* Ajuste del "Rectángulo de Seguridad" */
        [data-testid="block-container"] {{
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
            margin-top: 2rem;
            max-width: 900px;
        }}
        </style>
        <div class="bg-container">
            <img src="data:image/png;base64,{base64_image}">
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Ejecución ---
st.set_page_config(page_title="Würth - Plan Recambio", layout="wide")

# Aplicar fondo aleatorio con 70% de opacidad
fondo_seleccionado = get_random_bg()
if fondo_seleccionado:
    set_bg_with_opacity(fondo_seleccionado, opacity=0.7)

# Cabecera de la App
st.image("logo_wurth.jpg", width=120)
st.markdown("<h2 style='text-align: center; color: #333;'>Calculadora Plan Recambio</h2>", unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["1. Calculadora", "2. Catálogo", "3. Consolidación"])

with tab1:
    col_input, col_result = st.columns(2)
    with col_input:
        st.write("### Complete lo que el cliente entrega:")
        # Aquí puedes seguir con los selectores de productos
