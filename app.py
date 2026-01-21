import streamlit as st
import base64
import os
import random

# --- SOPORTE DE ARCHIVOS ---
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

# --- INICIALIZACIÓN DE SESIÓN (Para no perder el pedido) ---
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
if 'bolsa_puntos' not in st.session_state:
    st.session_state.bolsa_puntos = 0

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Würth Plan Recambio", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
red_stripe_base64 = get_base64("logo_red_stripe.png")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS REFINADO ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    
    .stApp {{ background: none; }}
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.08;
    }}

    [data-testid="block-container"] {{
        background-color: rgba(242, 242, 242, 0.98); padding: 0 !important;
        border-radius: 12px; box-shadow: 0px 15px 50px rgba(0,0,0,0.3);
        max-width: 950px; margin-top: 30px;
    }}

    /* Cabecera: Centrado total */
    .header-container {{
        display: flex; background-color: white; height: 160px; border-radius: 12px 12px 0 0;
    }}
    .header-logo {{ flex: 1; display: flex; align-items: center; justify-content: center; }}
    .header-title {{
        flex: 2.5; background-color: #CC0000; display: flex; 
        align-items: center; justify-content: center; /* Centrado en altura y ancho */
    }}
    .header-title h1 {{ 
        color: white !important; font-family: 'WuerthBold'; font-size: 50px !important; 
        margin: 0; text-transform: uppercase;
    }}

    /* Estilo Menú (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; padding: 0 20px; }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 18px !important; height: 60px;
    }}

    .card {{ background-color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #eee; }}
    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 80px; text-align: center; }}
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

t1, t2, t3 = st.tabs(["📊 1. CALCULADORA", "🛠️ 2. CATÁLOGO", "🛒 3. PEDIDO"])

# --- TAB 1: CALCULADORA ---
with t1:
    st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:20px 0;'>Ingresar entregas del cliente</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        q_comp = st.number_input("Máquinas Completas (20% c/u)", 0, 100, 0)
        q_sinb = st.number_input("Máquinas sin batería (10% c/u)", 0, 100, 0)
        q_batc = st.number_input("Solo Batería o Cargador (5% c/u)", 0, 100, 0)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card" style="text-align:center;">', unsafe_allow_html=True)
        total_p = (q_comp * 20) + (q_sinb * 10) + (q_batc * 5)
        st.write("**Total Bolsa Acumulada**")
        st.markdown(f'<div class="big-num">{total_p}%</div>', unsafe_allow_html=True)
        if st.button("Confirmar Bolsa", use_container_width=True):
            st.session_state.bolsa_puntos = total_p
            st.toast("Bolsa de puntos actualizada")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: CATÁLOGO ---
with t2:
    st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:20px 0;'>Seleccionar Herramienta Nueva</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    path = "assets/productos"
    if os.path.exists(path):
        prods = [f for f in os.listdir(path) if f.endswith('.png')]
        seleccion = st.selectbox("Elegir del catálogo:", prods)
        
        col_img, col_act = st.columns(2)
        with col_img:
            st.image(os.path.join(path, seleccion), width=250)
        with col_act:
            st.write(f"**Producto:** {seleccion}")
            disponible = st.session_state.bolsa_puntos
            dto_a_usar = st.slider("Asignar descuento (%)", 0, 30, value=min(disponible, 30))
            
            if st.button("Añadir al Pedido"):
                if disponible >= dto_a_usar:
                    st.session_state.carrito.append({"prod": seleccion, "dto": dto_a_usar})
                    st.session_state.bolsa_puntos -= dto_a_usar
                    st.success("Añadido al pedido.")
                    st.rerun()
                else:
                    st.error("Puntos insuficientes.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: PEDIDO ---
with t3:
    st.markdown("<h3 style='color:#CC0000; font-family:WuerthBold; padding:20px 0;'>Resumen del Pedido</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Bolsa restante:** {st.session_state.bolsa_puntos}%")
    
    if st.session_state.carrito:
        # Tabla de resumen
        for idx, item in enumerate(st.session_state.carrito):
            col_a, col_b, col_c = st.columns([3, 1, 1])
            col_a.write(f"**{idx+1}.** {item['prod']}")
            col_b.write(f"**-{item['dto']}%**")
            if col_c.button("❌", key=f"del_{idx}"):
                st.session_state.bolsa_puntos += item['dto']
                st.session_state.carrito.pop(idx)
                st.rerun()
        
        st.write("---")
        if st.button("Finalizar y Limpiar Todo"):
            st.session_state.carrito = []
            st.session_state.bolsa_puntos = 0
            st.rerun()
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
