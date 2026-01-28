import streamlit as st
import pandas as pd
import base64
import os
import random
import difflib

# --- SOPORTE DE ARCHIVOS Y DATOS ---
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

@st.cache_data
def cargar_datos_csv():
    # Cargamos el CSV saltando la primera fila de título si es necesario
    try:
        df = pd.read_csv("Lista_Precios - CORDLESS MACHINES.xlsx - Hoja1.csv", skiprows=1)
        return df
    except:
        return None

def buscar_info_producto(nombre_app, df):
    if df is None: return None
    # Buscamos la mejor coincidencia en la columna 'Producto'
    lista_productos_csv = df['Producto'].tolist()
    # difflib.get_close_matches usa ratio de similitud (0.8 = 80%)
    matches = difflib.get_close_matches(nombre_app, lista_productos_csv, n=1, cutoff=0.6)
    
    if matches:
        return df[df['Producto'] == matches[0]].iloc[0]
    return None

# --- INICIALIZACIÓN ---
df_precios = cargar_datos_csv()

if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'dto_base' not in st.session_state: st.session_state.dto_base = 0
if 'nombre_cliente' not in st.session_state: st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state: st.session_state.numero_cliente = ""
if 'tab_actual' not in st.session_state: st.session_state.tab_actual = "CALCULADORA"

# --- CONFIGURACIÓN DE PÁGINA ---
red_stripe_base64 = get_base64("favicon.png") 
st.set_page_config(page_title="Würth Plan Recambio", page_icon=f"data:image/png;base64,{red_stripe_base64}", layout="centered")

# CSS e Inyección de Estilos (Mantenemos tu estilo original)
# ... (Se mantiene igual al original para no alterar visuales) ...

# --- PESTAÑA 2: CATÁLOGO (ACTUALIZADA) ---
if st.session_state.tab_actual == "CATÁLOGO":
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
            sel_img = st.selectbox("Producto:", archivos, format_func=mostrar_nombre)
            nombre_bonito = mostrar_nombre(sel_img)
            
            # Buscamos en el Excel
            info_excel = buscar_info_producto(nombre_bonito, df_precios)
            
            ci, cs = st.columns(2)
            with ci: 
                st.image(os.path.join(p, sel_img), use_container_width=True)
            
            with cs:
                if info_excel is not None:
                    precio_lista = info_excel['Precio']
                    st.markdown(f"### Precio Lista: **${precio_lista:,.2f}**")
                    
                    with st.expander("➕ Ver características técnicas"):
                        st.write(f"**Voltaje:** {info_excel['Voltage']}")
                        st.write(f"**Potencia:** {info_excel['Power']}")
                        st.caption(f"{info_excel['Technical detailing']}")
                else:
                    st.warning("Producto no encontrado en el Excel de precios.")
                    precio_lista = 0

                # Lógica de Descuentos
                num_en_carro = len(st.session_state.carrito)
                if st.session_state.dto_base < 20:
                    st.error("Descuento 0%: Pase por la calculadora.")
                    dto_item = 0
                else:
                    faltantes = 3 - num_en_carro
                    dto_item = 30 if num_en_carro >= 2 else 20 # Si ya hay 2, el que sigue es el 3ero (30%)
                    if num_en_carro < 2:
                        st.info(f"Faltan {3 - num_en_carro} para el 30% en todo.")

                if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                    st.session_state.carrito.append({
                        "prod": nombre_bonito, 
                        "dto": dto_item, 
                        "precio": precio_lista
                    })
                    if len(st.session_state.carrito) >= 3:
                        for it in st.session_state.carrito: it['dto'] = 30
                    st.toast(f"✅ {nombre_bonito} añadido")
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ... (El resto del código de la pestaña PEDIDO se ajustaría para mostrar el precio total)
