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

# --- CSS MEJORADO ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{font_bold}'); }}
    
    .stApp {{ background: none; }}
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.7;
    }}

    /* Rectángulo de Seguridad y Contenedores */
    [data-testid="block-container"] {{
        background-color: #F2F2F2; padding: 0 !important; border-radius: 10px;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.4); max-width: 950px; margin-top: 20px;
    }}

    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 10px 10px 0 0;
    }}
    .header-logo {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; }}
    .header-title {{
        flex: 2.5; background-color: #CC0000; display: flex; align-items: center; 
        justify-content: flex-start; padding-left: 50px; /* Separación borde izquierdo */
    }}
    .header-title h1 {{ color: white !important; font-family: 'WuerthBold'; font-size: 55px !important; margin: 0; }}

    /* Bloques de color para contener información */
    .info-block {{
        background-color: white; padding: 25px; border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;
    }}
    
    .discount-display {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 80px; text-align: center; margin: 0;
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; right: 20px; width: 180px; }}
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

tab1, tab2, tab3 = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Consolidación"])

# --- LÓGICA DE DESCUENTOS ---
with tab1:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; margin-top:20px;'>Ingresar lo que entrega el cliente</h3>", unsafe_allow_html=True)
    
    col_input, col_res = st.columns([1.2, 1])
    
    with col_input:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        q_completa = st.number_input("Máquina Completa (20% dto)", min_value=0, step=1)
        q_sin_bat = st.number_input("Máquina sin batería (10% dto)", min_value=0, step=1)
        q_solo_bat = st.number_input("Solo Batería o Cargador (5% dto)", min_value=0, step=1)
        
        total_items = q_completa + q_sin_bat + q_solo_bat
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res:
        st.markdown('<div class="info-block" style="text-align:center;">', unsafe_allow_html=True)
        st.write("**Descuento Calculado**")
        
        # Lógica de tope de descuento por unidad
        # Máximo 20% para 1 o 2 herramientas, 30% para 3 o más
        base_dto = (q_completa * 20) + (q_sin_bat * 10) + (q_solo_bat * 5)
        
        if total_items >= 3:
            final_dto = min(base_dto, 30)
        elif total_items > 0:
            final_dto = min(base_dto, 20)
        else:
            final_dto = 0
            
        st.markdown(f'<p class="discount-display">{final_dto}%</p>', unsafe_allow_html=True)
        st.write(f"Items entregados: {total_items}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Confirmar para Selección", use_container_width=True):
            st.session_state['dto_ganado'] = final_dto
            st.info("Descuento guardado. Pasa a la pestaña de Catálogo.")

# --- CATÁLOGO ---
with tab2:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; margin-top:20px;'>Selección de Herramienta</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="info-block">', unsafe_allow_html=True)
    prod_path = "assets/productos"
    if os.path.exists(prod_path):
        opciones = os.listdir(prod_path)
        seleccion = st.selectbox("Elija la herramienta para aplicar el descuento:", opciones)
        
        c1, c2 = st.columns(2)
        with c1:
            st.image(os.path.join(prod_path, seleccion), width=250)
        with c2:
            dto = st.session_state.get('dto_ganado', 0)
            st.markdown(f"### Descuento a aplicar: <span style='color:red'>{dto}%</span>", unsafe_allow_html=True)
            st.write(f"Producto: {seleccion}")
            if st.button("Agregar a Consolidación"):
                st.success("Agregado con éxito.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Logo
if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
