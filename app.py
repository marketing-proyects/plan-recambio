import streamlit as st
import base64
import os
import random

# --- FUNCIONES DE SOPORTE ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def get_random_bg():
    bg_dir = "assets2/fondos"
    if os.path.exists(bg_dir):
        fondos = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return os.path.join(bg_dir, random.choice(fondos)) if fondos else None
    return None

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
font_bold = get_base64("WuerthBold.ttf")

# --- CSS REFINADO ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{font_bold}'); }}
    
    .stApp {{ background: none; }}
    
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; 
        background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; 
        opacity: 0.10; /* Fondo casi imperceptible */
    }}

    [data-testid="block-container"] {{
        background-color: rgba(242, 242, 242, 0.9); /* Fondo gris claro con bloque sólido */
        padding: 0 !important; border-radius: 12px;
        box-shadow: 0px 15px 50px rgba(0,0,0,0.3); max-width: 950px; margin-top: 30px;
    }}

    /* Cabecera con Título Centrado */
    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
    }}
    .header-logo {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; }}
    .header-title {{
        flex: 2.5; background-color: #CC0000; display: flex; align-items: center; 
        justify-content: center; /* TÍTULO CENTRADO */
    }}
    .header-title h1 {{ color: white !important; font-family: 'WuerthBold'; font-size: 55px !important; margin: 0; text-align: center; }}

    /* Estilo de Tabs (Menú) */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 20px !important;
        height: 60px; color: #333;
    }}

    .info-block {{
        background-color: white; padding: 30px; border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }}
    
    .discount-big {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 110px; text-align: center; margin: 0;
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; right: 20px; width: 150px; opacity: 0.8; }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="header-container">
        <div class="header-logo"><img src="data:image/jpeg;base64,{logo_base64}" width="120"></div>
        <div class="header-title"><h1>PLAN RECAMBIO</h1></div>
    </div>
    """, unsafe_allow_html=True)

# Pestañas con nombres actualizados
tabs = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Pedido"])

# --- TAB 1: CALCULADORA ---
with tabs[0]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding: 20px 0 10px 0;'>Ingresar lo que entrega el cliente</h3>", unsafe_allow_html=True)
    
    c_input, c_result = st.columns([1.2, 0.8])
    
    with c_input:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        # Menú desplegable para opciones de entrega
        opcion_entrega = st.selectbox(
            "Seleccione tipo de entrega:",
            ["Máquina Completa (20%)", "Máquina sin batería (10%)", "Solo Batería o Cargador (5%)"]
        )
        cantidad = st.number_input("Cantidad entregada:", min_value=0, step=1, value=1)
        
        # Mapeo de valores para el cálculo
        val_map = {"Máquina Completa (20%)": 20, "Máquina sin batería (10%)": 10, "Solo Batería o Cargador (5%)": 5}
        puntos_base = val_map[opcion_entrega] * cantidad
        
        st.info(f"Has seleccionado {cantidad} unidad(es) de: {opcion_entrega}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c_result:
        st.markdown('<div class="info-block" style="text-align:center;">', unsafe_allow_html=True)
        st.write("**Descuento Calculado**")
        
        # Lógica de tope de descuento
        if cantidad >= 3:
            dto_final = min(puntos_base, 30)
        elif cantidad > 0:
            dto_final = min(puntos_base, 20)
        else:
            dto_final = 0
            
        st.markdown(f'<div class="discount-big">{dto_final}%</div>', unsafe_allow_html=True)
        if st.button("Guardar para el Pedido", use_container_width=True):
            st.session_state['dto_final'] = dto_final
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: CATÁLOGO ---
with tabs[1]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding-top:20px;'>Catálogo de Herramientas</h3>", unsafe_allow_html=True)
    st.markdown('<div class="info-block">', unsafe_allow_html=True)
    # Lógica de catálogo similar a la anterior pero con diseño limpio
    prod_path = "assets/productos"
    if os.path.exists(prod_path):
        productos = [f for f in os.listdir(prod_path) if f.endswith('.png')]
        sel = st.selectbox("Seleccione herramienta del catálogo:", productos)
        st.image(os.path.join(prod_path, sel), width=300)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
