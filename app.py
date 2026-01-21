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

# --- CSS REFINADO (OPACIDAD AL 15%) ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{font_bold}'); }}
    
    .stApp {{ background: none; }}
    
    /* Capa de fondo con opacidad reducida para que apenas se vea */
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; 
        background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; 
        background-position: center; 
        opacity: 0.15; /* AJUSTE: Ahora es casi imperceptible */
    }}

    [data-testid="block-container"] {{
        background-color: #F2F2F2; padding: 0 !important; border-radius: 12px;
        box-shadow: 0px 15px 50px rgba(0,0,0,0.3); max-width: 950px; margin-top: 30px;
    }}

    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
        border-bottom: 2px solid #eee;
    }}
    .header-logo {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; }}
    .header-title {{
        flex: 2.5; background-color: #CC0000; display: flex; align-items: center; 
        justify-content: flex-start; padding-left: 60px; /* Separación solicitada */
    }}
    .header-title h1 {{ color: white !important; font-family: 'WuerthBold'; font-size: 50px !important; margin: 0; }}

    .info-block {{
        background-color: white; padding: 30px; border-radius: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        border: 1px solid #eef;
    }}
    
    .discount-number {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 90px; text-align: center; margin: 10px 0;
    }}
    
    .footer-logo {{ position: fixed; bottom: 20px; right: 20px; width: 160px; opacity: 0.9; }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div class="header-container">
        <div class="header-logo"><img src="data:image/jpeg;base64,{logo_base64}" width="110"></div>
        <div class="header-title"><h1>PLAN RECAMBIO</h1></div>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["📊 1. Calculadora", "🛠️ 2. Catálogo", "📝 3. Consolidación"])

# --- TAB 1: CALCULADORA DE ENTREGAS ---
with tabs[0]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding-top:20px;'>Ingresar lo que entrega el cliente</h3>", unsafe_allow_html=True)
    
    c_left, c_right = st.columns([1.1, 0.9])
    
    with c_left:
        st.markdown('<div class="info-block">', unsafe_allow_html=True)
        q_completa = st.number_input("Máquina Completa (20% c/u)", min_value=0, step=1, value=0)
        q_sin_bat = st.number_input("Máquina sin batería (10% c/u)", min_value=0, step=1, value=0)
        q_solo_bat = st.number_input("Batería o Cargador (5% c/u)", min_value=0, step=1, value=0)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="info-block" style="text-align:center;">', unsafe_allow_html=True)
        st.write("**Descuento Máximo por Unidad**")
        
        # Lógica de negocio
        items = q_completa + q_sin_bat + q_solo_bat
        suma_puntos = (q_completa * 20) + (q_sin_bat * 10) + (q_solo_bat * 5)
        
        # Tope según cantidad de herramientas
        if items >= 3:
            dto_final = min(suma_puntos, 30)
        elif items > 0:
            dto_final = min(suma_puntos, 20)
        else:
            dto_final = 0
            
        st.markdown(f'<div class="discount-number">{dto_final}%</div>', unsafe_allow_html=True)
        st.markdown(f"**Total entregado:** {items} componentes", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Guardar Beneficio", use_container_width=True):
            st.session_state['dto_val'] = dto_final
            st.toast(f"¡Beneficio del {dto_final}% guardado!")

# --- TAB 2: CATÁLOGO ---
with tabs[1]:
    st.markdown("<h3 style='color: #CC0000; font-family: WuerthBold; padding-top:20px;'>Selección de Herramienta a Comprar</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="info-block">', unsafe_allow_html=True)
    prod_path = "assets/productos"
    if os.path.exists(prod_path):
        opciones = [f for f in os.listdir(prod_path) if f.endswith('.png')]
        seleccion = st.selectbox("Elija la herramienta de catálogo:", opciones)
        
        col_img, col_txt = st.columns([1, 1])
        with col_img:
            st.image(os.path.join(prod_path, seleccion), use_container_width=True)
        with col_txt:
            dto_activo = st.session_state.get('dto_val', 0)
            st.markdown(f"### Descuento Aplicable: <span style='color:red'>{dto_activo}%</span>", unsafe_allow_html=True)
            st.markdown(f"**Modelo:** {seleccion}")
            if st.button("Confirmar Selección", use_container_width=True):
                st.success(f"Añadido: {seleccion} con -{dto_activo}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer Logo flotante
if red_stripe_base64:
    st.markdown(f'<img src="data:image/png;base64,{red_stripe_base64}" class="footer-logo">', unsafe_allow_html=True)
