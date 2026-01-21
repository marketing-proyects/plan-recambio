import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def get_base64(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception as e:
        return ""
    return ""

# Carga de recursos
f_bold = get_base64("WuerthBold.ttf")
f_book = get_base64("WuerthBook.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")

# --- LÓGICA DE DIRECTORIOS Y CARRUSEL ---
path_fondos = "assets2/" 
path_prod = "assets/productos/"

fondos = sorted([f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]) if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith(('.png'))]) if os.path.exists(path_prod) else []

# Inicialización de índices para el carrusel
if 'indice_prod' not in st.session_state: st.session_state.indice_prod = 0
if 'pausa_carrusel' not in st.session_state: st.session_state.pausa_carrusel = False
if 'bg_actual' not in st.session_state and fondos: st.session_state.bg_actual = random.choice(fondos)

# --- AUTO-REFRESH (Cada 3 segundos) ---
if not st.session_state.pausa_carrusel:
    # Esto refresca la app automáticamente
    st.empty() # Placeholder para el timer
    # Usamos un truco de streamlit para simular el auto-cambio
    # Nota: Requiere interactividad o st_autorefresh si fuera externo, 
    # aquí lo simularemos con la lógica de botones para estabilidad.

# --- ESTILOS MEJORADOS ---
bg_path = os.path.join(path_fondos, st.session_state.bg_actual) if fondos else ""
bg_base64 = get_base64(bg_path)

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), 
                    url(data:image/jpeg;base64,{bg_base64});
        background-size: cover;
        background-position: center;
        transition: background 1s ease-in-out;
    }}

    /* BADGE GRANDE Y CERCA */
    .discount-badge {{
        position: absolute;
        top: -30px;
        left: 50%;
        transform: translateX(40px); /* Ajustado para estar "encima" de la máquina */
        background-color: #CC0000;
        color: white;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        box-shadow: 0 10px 30px rgba(204,0,0,0.6);
        z-index: 100;
        border: 4px solid white;
    }}

    /* BOTÓN "QUIERO ESTA HERRAMIENTA" */
    .stButton>button.quiero-btn {{
        background-color: #000000 !important;
        color: #CC0000 !important;
        font-size: 1.5rem !important;
        height: 80px !important;
        border: 2px solid #CC0000 !important;
        font-family: 'WuerthBold' !important;
    }}

    .nav-btn {{
        background: rgba(0,0,0,0.5) !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
logo_w_b64 = get_base64("logo_wurth.jpg")
logo_rs_b64 = get_base64("logo_red_stripe.png")

st.markdown(f'''
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 40px;">
        <img src="data:image/png;base64,{logo_rs_b64}" width="350">
        <img src="data:image/jpg;base64,{logo_w_b64}" width="180">
    </div>
''', unsafe_allow_html=True)

# --- CARRUSEL Y ACCIÓN ---
if productos:
    prod_file = productos[st.session_state.indice_prod]
    
    col_prev, col_main, col_next = st.columns([1, 8, 1])
    
    with col_prev:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        if st.button("⬅️", key="prev"):
            st.session_state.indice_prod = (st.session_state.indice_prod - 1) % len(productos)
            st.rerun()

    with col_main:
        st.markdown('<div style="position: relative; text-align: center;">', unsafe_allow_html=True)
        
        # Badge
        if st.session_state.get('descuento_seleccionado', 0) > 0:
            st.markdown(f'''
                <div class="discount-badge">
                    <span style="font-size:55px; line-height:1;">{st.session_state.descuento_seleccionado}%</span>
                    <span style="font-size:18px;">AHORRO</span>
                </div>
            ''', unsafe_allow_html=True)
        
        st.image(os.path.join(path_prod, prod_file), width=550)
        nombre = prod_file.split('.')[0].replace('_', ' ').upper()
        st.markdown(f"<h2 style='color:black; font-family:WuerthBold; background:rgba(255,255,255,0.6); padding:10px;'>{nombre}</h2>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_next:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        if st.button("➡️", key="next"):
            st.session_state.indice_prod = (st.session_state.indice_prod + 1) % len(productos)
            st.rerun()

    # BOTÓN DE ACCIÓN CENTRAL
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🎯 QUIERO ESTA HERRAMIENTA", use_container_width=True, type="primary"):
            st.session_state.pausa_carrusel = True
            st.balloons()
            st.success(f"Has seleccionado: {nombre}. Procede a calcular tu descuento abajo.")

# --- SECCIÓN DE CÁLCULO (Aparece tras elegir) ---
if st.session_state.pausa_carrusel:
    st.divider()
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        st.subheader("Paso 2: Tu Entrega")
        entrega = st.selectbox("¿Qué vas a entregarnos?", ["Máquina Completa", "Máquina Parcial", "Batería / Cargador"])
        if st.button("CONFIRMAR Y CALCULAR"):
            if "Completa" in entrega: st.session_state.descuento_seleccionado = 25
            elif "Parcial" in entrega: st.session_state.descuento_seleccionado = 15
            else: st.session_state.descuento_seleccionado = 10
            st.rerun()
