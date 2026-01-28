import streamlit as st
import pandas as pd
import base64
import os
import random
import re

# --- SOPORTE DE ARCHIVOS Y DATOS ---
def get_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def get_random_bg():
    bg_dir = "assets2/fondos"
    if os.path.exists(bg_dir):
        fondos = [f for f in os.listdir(bg_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if fondos:
            return os.path.join(bg_dir, random.choice(fondos))
    return None

@st.cache_data
def cargar_datos_csv():
    file_path = "Lista_Precios - CORDLESS MACHINES.xlsx - Hoja1.csv"
    if not os.path.exists(file_path):
        return None
    try:
        # Cargamos el CSV saltando la primera fila de título (Power Tools,,,)
        df = pd.read_csv(file_path, skiprows=1)
        df.columns = [c.strip() for c in df.columns]
        # Limpiar la columna Producto de saltos de línea para facilitar búsqueda
        df['Producto_Limpio'] = df['Producto'].str.replace('\n', ' ', regex=True).str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar el Excel: {e}")
        return None

def encontrar_producto_csv(nombre_app, df):
    if df is None: return None
    
    # Normalizamos el nombre de la app (quitamos espacios extra y pasamos a minúsculas)
    palabras_app = set(re.findall(r'\w+', nombre_app.lower()))
    
    mejor_match = None
    max_similitud = 0
    
    for _, row in df.iterrows():
        nombre_csv = str(row['Producto_Limpio']).lower()
        palabras_csv = set(re.findall(r'\w+', nombre_csv))
        
        if not palabras_app: continue
        
        # Intersección de palabras para ver cuántas coinciden
        comunes = palabras_app.intersection(palabras_csv)
        similitud = len(comunes) / len(palabras_app)
        
        if similitud > max_similitud:
            max_similitud = similitud
            mejor_match = row
            
    # Devolvemos el resultado si la coincidencia es alta (75-80%)
    if max_similitud >= 0.75:
        return mejor_match
    return None

# --- INICIALIZACIÓN DE ESTADOS ---
if 'carrito' not in st.session_state: st.session_state.carrito = []
if 'dto_base' not in st.session_state: st.session_state.dto_base = 0
if 'nombre_cliente' not in st.session_state: st.session_state.nombre_cliente = ""
if 'numero_cliente' not in st.session_state: st.session_state.numero_cliente = ""
if 'tab_actual' not in st.session_state: st.session_state.tab_actual = "CALCULADORA"

# --- CARGAR DATOS ---
df_precios = cargar_datos_csv()

# --- CONFIGURACIÓN DE PÁGINA ---
red_stripe_base64 = get_base64("favicon.png") 
st.set_page_config(
    page_title="Würth Plan Recambio", 
    page_icon=f"data:image/png;base64,{red_stripe_base64}" if red_stripe_base64 else "🛠️", 
    layout="centered"
)

# --- ESTILOS CSS ---
bg_file = get_random_bg()
bg_base64 = get_base64(bg_file) if bg_file else ""
font_base64 = get_base64("assets/fonts/WuerthBold.ttf")

st.markdown(f"""
<style>
    @font-face {{
        font-family: 'WuerthBold';
        src: url('data:font/ttf;base64,{font_base64}');
    }}
    .stApp {{
        background: url("data:image/png;base64,{bg_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    .card {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border-left: 5px solid #CC0000;
    }}
    .card-title {{
        font-family: 'WuerthBold', sans-serif;
        color: #CC0000;
        font-size: 24px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }}
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
c1, c2, c3 = st.columns(3)
if c1.button("CALCULADORA", use_container_width=True): 
    st.session_state.tab_actual = "CALCULADORA"
    st.rerun()
if c2.button("CATÁLOGO", use_container_width=True): 
    st.session_state.tab_actual = "CATÁLOGO"
    st.rerun()
if c3.button("PEDIDO", use_container_width=True): 
    st.session_state.tab_actual = "PEDIDO"
    st.rerun()

# --- PESTAÑA 1: CALCULADORA ---
if st.session_state.tab_actual == "CALCULADORA":
    st.markdown('<div class="card"><div class="card-title">Datos del Cliente</div>', unsafe_allow_html=True)
    st.session_state.nombre_cliente = st.text_input("Nombre / Razón Social", value=st.session_state.nombre_cliente)
    st.session_state.numero_cliente = st.text_input("N° de Cliente", value=st.session_state.numero_cliente)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Criterios de Recambio</div>', unsafe_allow_html=True)
    f1 = st.checkbox("Herramienta de la competencia")
    f2 = st.checkbox("Herramienta Würth antigua (fuera de garantía)")
    f3 = st.checkbox("Plan fidelización / Crecimiento de parque")
    
    if f1 or f2 or f3:
        st.session_state.dto_base = 20
        st.success("✅ CALIFICA PARA EL PLAN RECAMBIO (20% Base)")
    else:
        st.session_state.dto_base = 0
        st.warning("⚠️ Seleccione un criterio para activar el plan.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 2: CATÁLOGO ---
elif st.session_state.tab_actual == "CATÁLOGO":
    st.markdown('<div class="card"><div class="card-title">Catálogo de Máquinas</div>', unsafe_allow_html=True)
    
    p = "assets/productos"
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

    if os.path.exists(p):
        archivos = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if archivos:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            sel_img = st.selectbox("Seleccione un equipo:", archivos, format_func=mostrar_nombre)
            nombre_bonito = mostrar_nombre(sel_img)
            
            # Buscar info en el Excel (coincidencia del 80%)
            info_excel = encontrar_producto_csv(nombre_bonito, df_precios)
            
            col_img, col_info = st.columns([1, 1])
            with col_img:
                st.image(os.path.join(p, sel_img), use_container_width=True)
            
            with col_info:
                if info_excel is not None:
                    try:
                        precio = float(info_excel['Precio'])
                        st.markdown(f"### Precio: **${precio:,.2f}**")
                    except:
                        st.warning("Precio no disponible en el Excel.")
                        precio = 0
                    
                    # Botón (+) para características técnicas
                    with st.expander("➕ Ver características técnicas"):
                        st.write(f"**Voltaje:** {info_excel.get('Voltaje', 'N/A')}")
                        st.write(f"**Potencia:** {info_excel.get('Potencia', 'N/A')}")
                        st.caption(str(info_excel.get('Características', 'Sin detalles')).replace('\n', ' '))
                else:
                    st.info("No se encontró el precio en el Excel.")
                    precio = 0

                if st.button("AGREGAR AL PEDIDO", use_container_width=True):
                    if st.session_state.dto_base >= 20:
                        nuevo_item = {"prod": nombre_bonito, "precio": precio, "dto": 20}
                        st.session_state.carrito.append(nuevo_item)
                        # Lógica de escala: 3 o más unidades -> 30% en todos
                        if len(st.session_state.carrito) >= 3:
                            for item in st.session_state.carrito: item['dto'] = 30
                        st.toast(f"✅ {nombre_bonito} añadido")
                    else:
                        st.error("Primero califica en la calculadora.")
    else:
        st.error("Carpeta 'assets/productos' no encontrada.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 3: PEDIDO ---
elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        total = 0
        for i, item in enumerate(st.session_state.carrito):
            c_prod, c_det, c_del = st.columns([3, 2, 1])
            precio_final = item['precio'] * (1 - item['dto']/100)
            total += precio_final
            
            c_prod.write(f"**{item['prod']}**")
            c_det.write(f"${item['precio']:,.2f} (-{item['dto']}%) = **${precio_final:,.2f}**")
            
            if c_del.button("❌", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20
                st.rerun()
        st.divider()
        st.markdown(f"## TOTAL FINAL: **${total:,.2f}**")
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
