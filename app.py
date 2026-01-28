import streamlit as st
import base64
import os
import random
import pandas as pd
from fpdf import FPDF
from datetime import datetime

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

# --- CARGA DE DATOS (LISTA_PRECIOS.XLSX) ---
@st.cache_data
def load_prices():
    file_path = "Lista_Precios.xlsx"
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path, sheet_name="Hoja1")
        df.columns = [c.strip() for c in df.columns]
        # Filtro estricto: Solo filas con datos completos
        columnas_req = ["Producto", "Imagen", "Código", "Precio"]
        df = df.dropna(subset=columnas_req)
        return df
    except Exception as e:
        st.error(f"Error cargando Excel: {e}")
        return pd.DataFrame()

df_precios = load_prices()

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'dto_base' not in st.session_state: st.session_state.dto_base = 0
if 'nombre_cliente' not in st.session_state: st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state: st.session_state.numero_cliente = ""
if 'tab_actual' not in st.session_state: st.session_state.tab_actual = "CALCULADORA"

# --- CONFIGURACIÓN DE PÁGINA ---
red_stripe_base64 = get_base64("favicon.png") 
st.set_page_config(page_title="Würth Plan Recambio", page_icon=f"data:image/png;base64,{red_stripe_base64}", layout="centered")

fondo_path = get_random_bg()
logo_base64 = get_base64("logo_wurth.jpg")
f_bold = get_base64("WuerthBold.ttf")

# --- CSS INTEGRAL ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url('data:font/ttf;base64,{f_bold}'); }}
    .element-container:has(h1) a, .element-container:has(h2) a, .element-container:has(h3) a, 
    .element-container:has(h4) a, .element-container:has(h5) a, .element-container:has(h6) a,
    [data-testid="stHeaderActionElements"] {{ display: none !important; }}
    header {{ visibility: hidden; }}
    button[title="View fullscreen"] {{ visibility: hidden; }}
    .stApp {{ background: none; }}
    .bg-layer {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; background-image: url("data:image/png;base64,{get_base64(fondo_path)}");
        background-size: cover; background-position: center; opacity: 0.12;
    }}
    .card {{ background-color: white; padding: 50px 40px; border-radius: 15px; border: 1px solid #ddd; box-shadow: 0px 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center; }}
    .card-title {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 34px; margin-bottom: 30px; text-transform: uppercase; line-height: 1.2; }}
    .big-num {{ color: #CC0000; font-family: 'WuerthBold'; font-size: 90px; line-height: 1; }}
    .small-num {{ color: #333; font-family: 'WuerthBold'; font-size: 40px; margin-top: 5px; }}
    .btn-active button {{ background-color: #28a745 !important; color: white !important; border: none !important; }}
    </style>
    <div class="bg-layer"></div>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown(f"""
    <div style="display: flex; background-color: white; height: 130px; border-radius: 12px; overflow: hidden; margin-bottom: 20px;">
        <div style="width: 200px; display: flex; align-items: center; justify-content: center;"><img src="data:image/jpeg;base64,{logo_base64}" width="120"></div>
        <div style="flex: 1; background-color: #CC0000; display: flex; align-items: center; justify-content: center;"><h1 style="color: white; font-family: 'WuerthBold'; font-size: 40px; margin: 0;">PLAN RECAMBIO</h1></div>
    </div>
    """, unsafe_allow_html=True)

# --- DATOS CLIENTE ---
col_n, col_v = st.columns([1.5, 1])
with col_n: st.session_state.nombre_cliente = st.text_input("NOMBRE DEL CLIENTE", value=st.session_state.nombre_cliente)
with col_v: st.session_state.numero_cliente = st.text_input("N° CLIENTE", value=st.session_state.numero_cliente)

# --- NAVEGACIÓN ---
c1, c2, c3 = st.columns(3)
if c1.button("📊 CALCULADORA", use_container_width=True): st.session_state.tab_actual = "CALCULADORA"
if c2.button("🛠️ CATÁLOGO", use_container_width=True): st.session_state.tab_actual = "CATÁLOGO"
if c3.button("🛒 PEDIDO", use_container_width=True): st.session_state.tab_actual = "PEDIDO"
st.divider()

# --- PESTAÑA 2: CATÁLOGO ---
if st.session_state.tab_actual == "CATÁLOGO":
    st.markdown('<div class="card"><div class="card-title">Seleccionar Máquina Nueva</div>', unsafe_allow_html=True)
    p = "assets/productos"
    
    # DICCIONARIO SINCRONIZADO CON EXCEL
    nombres_reales = {
        "ABSR 12 COMPACT_2.png": "Taladro Destornillador ABS Compacto",
        "ABSR 20 COMBI_1.png": "Taladro Atornillador ABSR 20 Combinado",
        "ABSR 20 COMBI_2.png": "Taladro Atornillador ABSR 20 Compact",
        "ABSR 20 PWR COMBI_1.png": "Taladro Percutor y Atornillador ABSR 20 PWR Combi",
        "AWSR 20 COMPACT_1.png": "Amoladora Angular AWSR 20 Compact",
        "ASSR 20_3.png": "Atornillador de Impacto Master ASSR 20 14 inch Compact",                     
        "ASSR 20 - 12 POWER_1.png": "LLave de Impacto ASSR 20 - 1/2 Compact 20V / 4.0AH",
        "ASSR 20 - 34_1.png": "LLave de Impacto REDSTRIPE ASSR 20 - 3/4 20V / 8.0AH",
        "ABHR 20 LIGHT_1.png": "Rotomartillo Light",
        "ABHR 20 POWER_1.png": "Rotomartillo Power"
    }

    if os.path.exists(p):
        archivos = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if archivos and not df_precios.empty:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            
            # Sincronización estricta por nombre
            lista_imagenes_excel = df_precios['Imagen'].tolist()
            archivos_validos = [f for f in archivos if mostrar_nombre(f) in lista_imagenes_excel]
            
            if archivos_validos:
                sel = st.selectbox("Producto:", archivos_validos, format_func=mostrar_nombre)
                nombre_visible = mostrar_nombre(sel)
                
                datos_prod = df_precios[df_precios['Imagen'] == nombre_visible].iloc[0]
                precio_lista = float(datos_prod['Precio'])
                codigo_prod = str(datos_prod['Código'])
                
                ci, cs = st.columns(2)
                with ci: st.image(os.path.join(p, sel), width=280)
                with cs:
                    st.markdown(f"### Precio: ${precio_lista:,.2f}")
                    st.write(f"**Código:** {codigo_prod}")
                    
                    num_en_carro = len(st.session_state.carrito)
                    faltantes_30 = 3 - num_en_carro
                    if num_en_carro >= 3:
                        st.success("¡Beneficio 30% activado!")
                    else:
                        st.info(f"Faltan {max(0, faltantes_30)} unidad(es) para el 30%.")

                    if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                        st.session_state.carrito.append({"prod": nombre_visible, "precio": precio_lista, "dto": 20})
                        if len(st.session_state.carrito) >= 3:
                            for it in st.session_state.carrito: it['dto'] = 30
                        st.rerun()
            else:
                st.warning("No hay productos que coincidan entre las fotos y el Excel.")

# (Resto del código idéntico para Pedido y Calculadora)
