import streamlit as st
import os
import random

# --- LÓGICA DE IMAGEN ALEATORIA ---
path_productos = "assets/productos/"

# Verificamos si la carpeta existe y tiene imágenes
if os.path.exists(path_productos):
    lista_imagenes = [f for f in os.listdir(path_productos) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
else:
    lista_imagenes = []

# Selección aleatoria
if lista_imagenes:
    # Usamos session_state para que la imagen solo cambie al recargar la página 
    # o al realizar una acción específica, evitando que parpadee en cada clic.
    if 'imagen_actual' not in st.session_state:
        st.session_state.imagen_actual = random.choice(lista_imagenes)
    
    imagen_mostrar = os.path.join(path_productos, st.session_state.imagen_actual)
else:
    imagen_mostrar = None # O una imagen por defecto

# --- DENTRO DE LA FASE 1 (Visualización) ---
with col_visual:
    st.markdown('<div class="wuerth-card">', unsafe_allow_html=True)
    
    if imagen_mostrar:
        st.image(imagen_mostrar, use_container_width=True)
        # Extraemos el nombre del archivo para mostrarlo como título (quitando extensión)
        nombre_prod = st.session_state.imagen_actual.split('.')[0].replace('_', ' ').upper()
        st.markdown(f"**MODELO: {nombre_prod}**")
    
    st.metric("Beneficio", f"{st.session_state.descuento_global}%", delta="Plan Recambio")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Ver otro modelo"):
        st.session_state.imagen_actual = random.choice(lista_imagenes)
        st.rerun()
