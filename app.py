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

# --- CSS ACTUALIZADO ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{font_bold}'); }}
    
    .stApp {{ background: none; }}
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; 
        background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.12;
    }}

    [data-testid="block-container"] {{
        background-color: rgba(242, 242, 242, 0.95);
        padding: 0 !important; border-radius: 12px;
        box-shadow: 0px 15px 50px rgba(0,0,0,0.3); max-width: 950px; margin-top: 30px;
    }}

    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
    }}
    .header-logo {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; }}
    .header-title {{
        flex: 2.5; background-color: #CC0000; 
        display: flex; align-items: center; /* CENTRADO EN ALTURA */
        justify-content: center; 
    }}
    .header-title h1 {{ 
        color: white !important; font-family: 'WuerthBold'; font-size: 55px !important; 
        margin: 0; line-height: 160px; /* Asegura el centrado vertical del texto */
    }}

    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 22px !important; height: 70px;
    }}

    .info-block {{
        background-color: white; padding: 30px; border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }}
    
    .total-pool {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 80px; text-align: center; margin: 0;
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; right: 20px; width: 140px; }}
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

tabs = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Pedido"])

# --- TAB 1: CALCULADORA (MULTIPLE ENTREGA) ---
with tabs[0]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding: 20px 0;'>Ingresar entregas del cliente</h3>", unsafe_allow_html=True)
    
    col_in, col_pool = st.columns([1.2, 0.8])
    
    with col_in:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        q_c = st.number_input("Máquinas Completas (20% c/u)", min_value=0, step=1)
        q_s = st.number_input("Máquinas sin batería (10% c/u)", min_value=0, step=1)
        q_b = st.number_input("Solo Batería o Cargador (5% c/u)", min_value=0, step=1)
        
        total_puntos = (q_c * 20) + (q_s * 10) + (q_b * 5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pool:
        st.markdown('<div class="info-block" style="text-align:center;">', unsafe_allow_html=True)
        st.write("**Bolsa de Descuento Acumulada**")
        st.markdown(f'<div class="total-pool">{total_puntos}%</div>', unsafe_allow_html=True)
        st.write("Este porcentaje se puede repartir en el pedido.")
        if st.button("Confirmar Bolsa de Puntos", use_container_width=True):
            st.session_state['bolsa_puntos'] = total_puntos
            st.success("Puntos cargados correctamente.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: CATÁLOGO ---
with tabs[1]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding-top:20px;'>Explorar Catálogo</h3>", unsafe_allow_html=True)
    st.markdown('<div class="info-block">', unsafe_allow_html=True)
    prod_path = "assets/productos"
    if os.path.exists(prod_path):
        lista = [f for f in os.listdir(prod_path) if f.endswith('.png')]
        sel_prod = st.selectbox("Ver producto:", lista)
        st.image(os.path.join(prod_path, sel_prod), width=350)
        st.write(f"**Referencia:** {sel_prod}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: PEDIDO (REPARTO DE LOGICA) ---
with tabs[2]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding-top:20px;'>Configuración del Pedido</h3>", unsafe_allow_html=True)
    
    puntos_disponibles = st.session_state.get('bolsa_puntos', 0)
    
    st.markdown(f'<div class="info-block">', unsafe_allow_html=True)
    st.markdown(f"#### Puntos disponibles para repartir: <span style='color:red'>{puntos_disponibles}%</span>", unsafe_allow_html=True)
    
    # Ejemplo de reparto para la primera máquina del pedido
    st.write("---")
    st.write("**Máquina 1 del pedido:**")
    reparto = st.slider("Asignar descuento a esta unidad (%)", 0, 30, value=min(puntos_disponibles, 30))
    
    if st.button("Añadir al pedido y descontar de la bolsa"):
        if puntos_disponibles >= reparto:
            st.session_state['bolsa_puntos'] -= reparto
            st.success(f"Aplicado {reparto}% a la unidad. Quedan {st.session_state['bolsa_puntos']}% disponibles.")
            st.rerun()
        else:
            st.error("No tienes suficientes puntos en la bolsa.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
