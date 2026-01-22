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
if 'entregas_total' not in st.session_state: st.session_state.entregas_total = 0

# --- CONFIGURACIÓN DE PÁGINA ---
# Asegúrate de que el nombre del archivo coincida con tu logo cuadrado
red_stripe_base64 = get_base64("favicon.png") 

st.set_page_config(
    page_title="Würth Plan Recambio", 
    page_icon=f"data:image/png;base64,{red_stripe_base64}", 
    layout="centered"
)

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS INTEGRAL (DISEÑO Y CENTRADO) ---
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

    .stTabs [data-baseweb="tab-list"] {{ background-color: transparent !important; }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'WuerthBold' !important; font-size: 18px !important;
        background-color: #e8e8e8; border-radius: 10px 10px 0 0 !important;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #f5f5f5 !important; color: #CC0000 !important; }}

    /* Botón verde para beneficio activado */
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

t1, t2, t3 = st.tabs(["📊 CALCULADORA", "🛠️ CATÁLOGO", "🛒 PEDIDO"])

with t1:
    st.markdown('<div class="card"><div class="card-title">Ingresar entregas del cliente</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        qc = st.number_input("Máquinas Completas (20% c/u)", 0, 100, 0, key="n1")
        qs = st.number_input("Máquinas sin batería (10% c/u)", 0, 100, 0, key="n2")
        qb = st.number_input("Solo Batería o Cargador (5% c/u)", 0, 100, 0, key="n3")
        
        total_entregas = qc + qs + qb
        st.markdown(f'<div style="margin-top:20px;"><b>Unidades Entregadas</b><div class="small-num">{total_entregas}</div></div>', unsafe_allow_html=True)
        
    with c2:
        val = (qc * 20) + (qs * 10) + (qb * 5)
        st.markdown(f'<div style="margin-top:20px;"><b>SUMATORIA DESCUENTOS</b><div class="big-num">{val}%</div></div>', unsafe_allow_html=True)
        
        # Lógica de activación
        if st.session_state.dto_base >= 20:
             st.markdown('<div class="btn-active">', unsafe_allow_html=True)
             st.button("BENEFICIO ACTIVADO", use_container_width=True)
             st.markdown('</div>', unsafe_allow_html=True)
             st.success("El beneficio de recambio ya está activo.")
        else:
            if val >= 20:
                st.markdown('<div class="btn-active">', unsafe_allow_html=True)
                if st.button("ACTIVAR RECAMBIO (20%)", use_container_width=True):
                    st.session_state.dto_base = 20
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.button("MÍNIMO 20% REQUERIDO", use_container_width=True, disabled=True)
                
    st.markdown('</div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="card"><div class="card-title">Seleccionar Máquina Nueva</div>', unsafe_allow_html=True)
    
    if st.session_state.dto_base < 20:
        st.warning("Debe completar al menos el 20% en la CALCULADORA para acceder al beneficio.")
    else:
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
                def mostrar_nombre(archivo):
                    return nombres_reales.get(archivo, archivo)

                sel = st.selectbox("Seleccionar producto:", archivos, format_func=mostrar_nombre)

                ci, cs = st.columns(2)
                with ci:
                    st.image(os.path.join(p, sel), width=280)
                with cs:
                    # Lógica de escala de descuento
                    items_en_carrito = len(st.session_state.carrito)
                    dto_actual = 30 if (items_en_carrito + 1) >= 3 else 20
                    
                    st.write(f"**Producto:** {mostrar_nombre(sel)}")
                    st.write(f"**Descuento Aplicable:** {dto_actual}%")
                    
                    if dto_actual < 30:
                        st.caption("Añada 3 o más unidades para obtener 30% de descuento.")
                    else:
                        st.success("¡Descuento por volumen activado (30%)!")

                    if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                        st.session_state.carrito.append({
                            "prod": mostrar_nombre(sel), 
                            "dto": dto_actual
                        })
                        # Actualizar todos al 30% si llegamos al umbral
                        if len(st.session_state.carrito) >= 3:
                            for item in st.session_state.carrito:
                                item['dto'] = 30
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc = st.columns([3, 1, 1])
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"**-{item['dto']}%**")
            if cc.button("Quitar", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                # Revertir al 20% si bajamos de 3 unidades
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito:
                        it['dto'] = 20
                st.rerun()
        
        st.divider()
        total_herramientas = len(st.session_state.carrito)
        dto_final = 30 if total_herramientas >= 3 else 20
        st.write(f"**Total de herramientas:** {total_herramientas}")
        st.write(f"**Descuento aplicado:** {dto_final}%")
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
