import streamlit as st
import pandas as pd
import base64
import os
import random
import re

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

# --- LÓGICA DE DATOS (NUEVA) ---
@st.cache_data
def cargar_datos_csv():
    file_path = "Lista_Precios - CORDLESS MACHINES.xlsx - Hoja1.csv"
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_csv(file_path, skiprows=1)
        df.columns = [c.strip() for c in df.columns]
        df['Producto_Limpio'] = df['Producto'].str.replace('\n', ' ', regex=True).str.strip()
        return df
    except: return None

def buscar_precio_y_info(nombre_app, df):
    if df is None: return None
    palabras_app = set(re.findall(r'\w+', nombre_app.lower()))
    for _, row in df.iterrows():
        palabras_csv = set(re.findall(r'\w+', str(row['Producto_Limpio']).lower()))
        if len(palabras_app.intersection(palabras_csv)) / len(palabras_app) >= 0.7:
            return row
    return None

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'dto_base' not in st.session_state: st.session_state.dto_base = 0
if 'nombre_cliente' not in st.session_state: st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state: st.session_state.numero_cliente = ""
if 'tab_actual' not in st.session_state: st.session_state.tab_actual = "CALCULADORA"

df_precios = cargar_datos_csv()

# --- CONFIGURACIÓN DE PÁGINA ---
red_stripe_base64 = get_base64("favicon.png") 
st.set_page_config(page_title="Würth Plan Recambio", page_icon=f"data:image/png;base64,{red_stripe_base64}", layout="centered")

# --- ESTILOS (TU CSS ORIGINAL) ---
bg_file = get_random_bg()
bg_base64 = get_base64(bg_file)
font_base64 = get_base64("assets/fonts/WuerthBold.ttf")

st.markdown(f"""
<style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{font_base64}'); }}
    .stApp {{ background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed; background-size: cover; }}
    .card {{ background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); margin-bottom: 20px; }}
    .card-title {{ font-family: 'WuerthBold', sans-serif; color: #CC0000; font-size: 20px; margin-bottom: 10px; }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
col1, col2, col3 = st.columns(3)
if col1.button("CALCULADORA", use_container_width=True): st.session_state.tab_actual = "CALCULADORA"; st.rerun()
if col2.button("CATÁLOGO", use_container_width=True): st.session_state.tab_actual = "CATÁLOGO"; st.rerun()
if col3.button("PEDIDO", use_container_width=True): st.session_state.tab_actual = "PEDIDO"; st.rerun()

# --- PESTAÑA 1: CALCULADORA ---
if st.session_state.tab_actual == "CALCULADORA":
    st.markdown('<div class="card"><div class="card-title">Datos del Cliente</div>', unsafe_allow_html=True)
    st.session_state.nombre_cliente = st.text_input("Nombre / Razón Social", value=st.session_state.nombre_cliente)
    st.session_state.numero_cliente = st.text_input("N° de Cliente", value=st.session_state.numero_cliente)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Criterios de Recambio</div>', unsafe_allow_html=True)
    c1 = st.checkbox("Herramienta de la competencia")
    c2 = st.checkbox("Herramienta Würth antigua (fuera de garantía)")
    c3 = st.checkbox("Plan fidelización / Crecimiento de parque")
    if c1 or c2 or c3:
        st.session_state.dto_base = 20
        st.success("CALIFICA PARA EL PLAN RECAMBIO (20% Base)")
    else:
        st.session_state.dto_base = 0
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 2: CATÁLOGO ---
elif st.session_state.tab_actual == "CATÁLOGO":
    st.markdown('<div class="card"><div class="card-title">Seleccionar Máquina Nueva</div>', unsafe_allow_html=True)
    path_prod = "assets/productos"
    nombres_reales = {
        "ABSR 12 COMPACT_2.png": "Taladro Destornillador ABSR 12 Compacto",
        "ABSR 20 COMBI_1.png": "Taladro Atornillador ABSR 20 Combi",
        "ABSR 20 COMBI_2.png": "Taladro Atornillador ABSR 20 Compact",
        "ABSR 20 PWR COMBI_1.png": "Taladro Percutor y Atornillador ABSR 20 PWR Combi",
        "AWSR 20 COMPACT_1.png": "Amoladora Angular AWS R 20 - 115 Compact",
        "ASSR 20_3.png": "Atornillador de Impacto Master ASSR 20 Compact",                     
        "ASSR 20 - 12 POWER_1.png": "LLave de Impacto sin carbones 1/2 Power",
        "ASSR 20 - 34_1.png": "LLave de Impacto 3/4",
        "ABHR 20 LIGHT_1.png": "Rotomartillo ABHR 20 Light",
        "ABHR 20 POWER_1.png": "Rotomartillo ABHR 20 Power"
    }

    if os.path.exists(path_prod):
        files = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')])
        if files:
            def mostrar_nombre(f): return nombres_reales.get(f, f)
            sel = st.selectbox("Equipo:", files, format_func=mostrar_nombre)
            
            # --- INTEGRACIÓN DE PRECIO Y CARACTERÍSTICAS ---
            info = buscar_precio_y_info(mostrar_nombre(sel), df_precios)
            
            col_img, col_txt = st.columns([1, 1])
            with col_img:
                st.image(os.path.join(path_prod, sel), use_container_width=True)
            
            with col_txt:
                if info is not None:
                    st.markdown(f"### Precio: **${float(info['Precio']):,.2f}**")
                    with st.expander("➕ Ver características"):
                        st.write(f"**Voltaje:** {info.get('Voltaje', 'N/A')}")
                        st.write(f"**Potencia:** {info.get('Potencia', 'N/A')}")
                        st.caption(str(info.get('Características', '')).replace('\n', ' '))
                else:
                    st.info("Precio no disponible.")

                if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                    if st.session_state.dto_base >= 20:
                        p_val = float(info['Precio']) if info is not None else 0
                        st.session_state.carrito.append({"prod": mostrar_nombre(sel), "precio": p_val, "dto": 20})
                        if len(st.session_state.carrito) >= 3:
                            for it in st.session_state.carrito: it['dto'] = 30
                        st.toast(f"✅ {mostrar_nombre(sel)} añadido")
                        st.rerun()
                    else:
                        st.error("No califica para el plan.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 3: PEDIDO ---
elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        total = 0
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc = st.columns([3, 1, 1])
            p_final = item.get('precio', 0) * (1 - item['dto']/100)
            total += p_final
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"**-{item['dto']}%** (${p_final:,.2f})")
            if cc.button("Quitar", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20
                st.rerun()
        st.divider()
        st.markdown(f"### TOTAL: ${total:,.2f}")
    else:
        st.info("Carrito vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
