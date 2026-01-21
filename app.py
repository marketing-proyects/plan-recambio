import streamlit as st
import base64
import os

# Función para convertir imagen local a formato compatible con CSS
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(bin_file):
    bin_str = get_base64_of_bin_file(bin_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    
    /* Rectángulo de seguridad (Contenedor central) */
    [data-testid="block-container"] {{
        background-color: rgba(255, 255, 255, 0.95); /* Blanco con leve transparencia */
        padding: 3rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# 1. Configuración de fondo
# Elegimos uno de tus archivos en assets2/fondos (por ejemplo, el primero)
fondo_path = "assets2/fondos/ai-generated-1762847146870.png" # Ajusta el nombre según tu archivo
if os.path.exists(fondo_path):
    set_png_as_page_bg(fondo_path)

# --- El resto de tu lógica de la calculadora iría aquí abajo ---
st.title("Calculadora Plan Recambio")
