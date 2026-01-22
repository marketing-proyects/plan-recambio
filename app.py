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
    current_bg_dir = bg_dir if os.path.exists(bg_dir) else "."
    fondos = [f for f in os.listdir(current_bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return os.path.join(current_bg_dir, random.choice(fondos)) if fondos else None

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'dto_base' not in st.session_state: st.session_state.dto_base = 0
if 'nombre_cliente' not in st.session_state: st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state: st.session_state.numero_cliente = ""
if 'tab_actual' not in st.session_state: st.session_state.tab_actual = "CALCULADORA"

# --- CONFIGURACIÓN DE PÁGINA ---
# Usamos el logo cuadrado de Red Stripe que creamos
red_stripe_base64 = get_base64("favicon.png") 

st.set_page_config(
    page_title="Würth Plan Recambio", 
    page_icon=f"data:image/png;base64,{red_stripe_base64}", 
    layout="centered"
)

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS INTEGRAL ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    
    header {{ visibility: hidden; }}
    .stMarkdown a {{ display: none !important; }}
    
    .stApp {{ background: none; }}
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.12;
    }}

    /* Inputs */
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {{
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #CC0000 !important;
        border-radius: 0px !important;
        font-family: 'WuerthBold' !important;
        color: #333 !important;
        font-size: 18px !important;
    }}

    div[data-testid="stNumberInput"] > div, div[data-baseweb="input"] {{
        background-color: transparent !important;
        border: none !important;
    }}

    /* Tarjeta */
    .card {{ 
        background-color: white; padding: 50px 40px; border-radius: 15px; 
        border: 1px solid #ddd; box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        text-align: center;
    }}
    
    .card-title {{
        color: #CC0000; font-family: 'WuerthBold'; font-size: 34px;
        margin-bottom: 30px; text-transform: uppercase;
        line-height: 1.2;
    }}

    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 90px; line-height: 1; }}
    .small-num {{ color: #333; font-family: 'WuerthBold'; font-size: 40px; margin-top: 5px; }}

    /* Navegación estilo Tabs con Radio */
    .nav-container {{
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
        background: #e8e8e8;
        border-radius: 12px 12px 0 0;
        overflow: hidden;
    }}
    .nav-item {{
        flex: 1;
        padding: 15px;
        text-align: center;
        font-family: 'WuerthBold';
        cursor: pointer;
        color: #666;
        transition: 0.3s;
    }}
    .nav-item.active {{
        background: #f5f5f5;
        color: #CC0000;
        border-bottom: 3px solid #CC0000;
    }}

    /* Botón verde */
    .btn-active button {{
        background-color: #28a745 !important;
        color: white !important;
        border: none !important;
    }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div style="display: flex; background-color: white; height: 130px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;">
        <div style="width: 200px; display: flex; align-items: center; justify-content: center;">
            <img src="data:image/jpeg;base64,{logo_base64}" width="120">
        </div>
        <div style="flex: 1; background-color: #CC0000; display: flex; align-items: center; justify-content: center;">
            <h1 style="color: white; font-family: 'WuerthBold'; font-size: 40px; margin: 0;">PLAN RECAMBIO</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- DATOS CLIENTE ---
col_n, col_v = st.columns([1.5, 1])
with col_n:
    st.session_state.nombre_cliente = st.text_input("NOMBRE DEL CLIENTE", value=st.session_state.nombre_cliente)
with col_v:
    st.session_state.numero_cliente = st.text_input("N° CLIENTE", value=st.session_state.numero_cliente)

# --- NAVEGACIÓN CONTROLADA ---
col1, col2, col3 = st.columns(3)
if col1.button("📊 CALCULADORA", use_container_width=True): st.session_state.tab_actual = "CALCULADORA"
if col2.button("🛠️ CATÁLOGO", use_container_width=True): st.session_state.tab_actual = "CATÁLOGO"
if col3.button("🛒 PEDIDO", use_container_width=True): st.session_state.tab_actual = "PEDIDO"

st.divider()

# --- LÓGICA DE PESTAÑAS ---
if st.session_state.tab_actual == "CALCULADORA":
    st.markdown('<div class="card"><div class="card-title">Ingresar entregas del cliente</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        qc = st.number_input("Máquinas Completas (20% c/u)", 0, 100, 0, key="n1")
        qs = st.number_input("Máquinas sin batería (10% c/u)", 0, 100, 0, key="n2")
        qb = st.number_input("Solo Batería o Cargador (5% c/u)", 0, 100, 0, key="n3")
        total_ent = qc + qs + qb
        st.markdown(f'<div style="margin-top:20px;"><b>Unidades Entregadas</b><div class="small-num">{total_ent}</div></div>', unsafe_allow_html=True)
        
    with c2:
        val_real = (qc * 20) + (qs * 10) + (qb * 5)
        val_vis = min(val_real, 20) # TOPEADO AL 20%
        
        st.markdown(f'<div style="margin-top:20px;"><b>SUMATORIA DESCUENTOS</b><div class="big-num">{val_vis}%</div></div>', unsafe_allow_html=True)
        
        if st.session_state.dto_base >= 20:
             st.success("¡Beneficio de recambio activado!")
        else:
            if val_real >= 20:
                st.markdown('<div class="btn-active">', unsafe_allow_html=True)
                if st.button("ACTIVAR RECAMBIO", use_container_width=True):
                    st.session_state.dto_base = 20
                    st.session_state.tab_actual = "CATÁLOGO" # SALTO AUTOMÁTICO
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.button("MÍNIMO 20% REQUERIDO", use_container_width=True, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.tab_actual == "CATÁLOGO":
    st.markdown('<div class="card"><div class="card-title">Seleccionar Máquina Nueva</div>', unsafe_allow_html=True)
    p = "assets/productos"
    nombres_reales = {
        "ABSR 12 COMPACT_2.png": "Taladro Destornillador ABS Compacto",
        "ABSR 20 COMBI_1.png": "Taladro Atornillador ABSR 20 Combinado",
        "ABSR 20 COMBI_2.png": "Taladro Atornillador ABSR 20 Compact",
        "ABSR 20 PWR COMBI_1.png": "Taladro Percutor y Atornillador ABSR 20 PWR Combi",
        "AWSR 20 COMPACT_1.png": "Amoladora Angular AWS R 20 - 115 Compact",
        "ASSR 20_3.png": "Atornillador de Impacto Master ASSR 20 14 inch Compact",                     
        "ASSR 20 - 12 POWER_1.png": "LLave de Impacto sin carbones",
        "ASSR 20 - 34_1.png": "LLave de Impacto 3/4",
        "ABHR 20 LIGHT_1.png": "Rotomartillo Ligth",
        "ABHR 20 POWER_1.png": "Rotomartillo Power"
    }

    if os.path.exists(p):
        archivos = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if archivos:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            sel = st.selectbox("Producto:", archivos, format_func=mostrar_nombre)
            ci, cs = st.columns(2)
            with ci: st.image(os.path.join(p, sel), width=280)
            with cs:
                # Lógica de Descuento
                num_en_carro = len(st.session_state.carrito)
                if st.session_state.dto_base < 20:
                    st.error("Descuento 0%: Pase por la calculadora.")
                    dto_item = 0
                else:
                    # CORRECCIÓN: Solo muestra 30% si el PRÓXIMO item es el 3ro o más
                    dto_item = 30 if (num_en_carro + 1) >= 3 else 20
                    st.write(f"**Descuento Aplicable:** {dto_item}%")
                    if (num_en_carro + 1) >= 3:
                        st.success("¡Beneficio especial 30% aplicado!")
                    else:
                        st.caption("Añada 3 unidades para obtener el 30% en todo.")

                if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                    st.session_state.carrito.append({"prod": mostrar_nombre(sel), "dto": dto_item})
                    if len(st.session_state.carrito) >= 3:
                        for it in st.session_state.carrito: it['dto'] = 30
                    st.toast(f"✅ {mostrar_nombre(sel)} añadido") # NOTIFICACIÓN
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc = st.columns([3, 1, 1])
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"**-{item['dto']}%**")
            if cc.button("Quitar", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20 if st.session_state.dto_base >= 20 else 0
                st.rerun()
        st.divider()
        n = len(st.session_state.carrito)
        final_dto = 30 if n >= 3 else (20 if st.session_state.dto_base >= 20 else 0)
        st.write(f"**Unidades:** {n} | **Descuento Final:** {final_dto}%")
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
