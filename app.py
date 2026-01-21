import streamlit as st
from PIL import Image
import os

# Configuración de página
st.set_page_config(page_title="Würth - Plan Recambio", layout="centered")

# Aplicar fuentes y estilos personalizados mediante CSS
st.markdown(f"""
    <style>
    @font-face {{
        font-family: 'WuerthBold';
        src: url('WuerthBold.ttf');
    }}
    .main {{
        background-color: #f5f5f5;
    }}
    .stButton>button {{
        background-color: #cc0000;
        color: white;
        width: 100%;
        border-radius: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Encabezado con Logo y Título
col1, col2 = st.columns([1, 3])
with col1:
    st.image("logo_wurth.jpg", width=100)
with col2:
    st.markdown("<h1 style='color: white; background-color: #cc0000; padding: 20px; text-align: center;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# Navegación por pestañas (Tabs)
tab1, tab2, tab3 = st.tabs(["1. Calculadora", "2. Catálogo", "3. Consolidación"])

with tab1:
    st.subheader("Cálculo de Beneficio")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write("Complete lo que el cliente entrega:")
        
        # Selector de productos (usando los archivos de tu carpeta assets/productos)
        productos = [f for f in os.listdir("assets/productos") if f.endswith('.png')]
        seleccion = st.selectbox("Máquina Completa", productos)
        
        # Mostrar imagen del producto seleccionado
        img_path = os.path.join("assets/productos", seleccion)
        st.image(img_path, width=150)
        
        cantidad = st.number_input("Cantidad", min_value=0, value=1)

    with col_right:
        st.markdown("<p style='color: #cc0000; font-weight: bold;'>Descuento Aplicable</p>", unsafe_allow_html=True)
        st.markdown("<h2 style='font-size: 60px;'>20%</h2>", unsafe_allow_html=True)
        
        if st.button("Calcular y Aplicar"):
            st.success(f"Aplicado para {cantidad} unidad(es)")
