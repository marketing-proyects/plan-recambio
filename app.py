import streamlit as st
import base64
import random
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

# Función para inyectar CSS y fuentes (manteniendo lo anterior)
def local_css():
    st.markdown("""
        <style>
        /* Estilos de Würth */
        .main { background-color: #F2F2F2; }
        .wuerth-card {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { color: #CC0000; font-weight: bold; }
        .stButton>button {
            background-color: #CC0000;
            color: white;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- LÓGICA DE IMAGEN ALEATORIA ---
# Aquí pondrás la lista de nombres de archivos que me pases
# Por ahora uso placeholders para que veas cómo funciona
lista_maquinas = ["maquina1.png", "maquina2.png", "maquina3.png"] 
imagen_aleatoria = random.choice(lista_maquinas)

# --- HEADER CON LOGO ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    # Cuando cargues el logo, reemplaza 'logo_wuerth.png'
    # st.image("logo_wuerth.png", width=150)
    st.markdown("### LOGO WÜRTH") # Placeholder temporal

with col_titulo:
    st.title("PLAN RECAMBIO")

# --- CUERPO DE LA APP (FASE 1) ---
tabs = st.tabs(["📊 Calculadora", "🛠️ Catálogo", "📝 Resumen"])

with tabs[0]:
    col_input, col_visual = st.columns([1, 1])
    
    with col_input:
        st.markdown("### Detalle de Entrega")
        tipo = st.selectbox("¿Qué entrega el cliente?", 
                            ["Máquina Completa", "Máquina Parcial", "Batería/Cargador"])
        cant = st.number_input("Cantidad", min_value=1)
        st.button("Calcular Descuento")

    with col_visual:
        st.markdown('<div class="wuerth-card">', unsafe_allow_html=True)
        # Aquí es donde la imagen cambia con cada refresh
        st.write("### Modelo Sugerido")
        # st.image(f"assets/{imagen_aleatoria}", use_column_width=True)
        st.info(f"Aquí aparecería: {imagen_aleatoria}") 
        
        st.metric("Beneficio", "20%", delta="Plan Recambio")
        st.markdown('</div>', unsafe_allow_html=True)
