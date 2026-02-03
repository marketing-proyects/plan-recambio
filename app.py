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
        # Limpieza de espacios para evitar fallos de coincidencia
        df['Imagen'] = df['Imagen'].astype(str).str.strip()
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
    
    /* OCULTAR ICONOS DE ENLACE / CLIP / ANCHORS */
    .element-container:has(h1) a, .element-container:has(h2) a, .element-container:has(h3) a, 
    .element-container:has(h4) a, .element-container:has(h5) a, .element-container:has(h6) a,
    [data-testid="stHeaderActionElements"] {{
        display: none !important;
    }}
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

# --- PESTAÑA 1: CALCULADORA ---
if st.session_state.tab_actual == "CALCULADORA":
    st.markdown('<div class="card"><div class="card-title">Ingresar entregas del cliente</div>', unsafe_allow_html=True)
    ca, cb = st.columns([1.2, 0.8])
    with ca:
        qc = st.number_input("Máquinas Completas (20% c/u)", 0, 100, 0, key="n1")
        qs = st.number_input("Máquinas sin batería (10% c/u)", 0, 100, 0, key="n2")
        qb = st.number_input("Solo Batería o Cargador (5% c/u)", 0, 100, 0, key="n3")
        total_u = qc + qs + qb
        st.markdown(f'<div><b>Unidades Entregadas</b><div class="small-num">{total_u}</div></div>', unsafe_allow_html=True)
        st.markdown(
    f'<div style="color: red;"><b>Puedes adquirir esta misma cantidad de herramientas con el descuento especial de este Plan Recambio</b></div>', 
    unsafe_allow_html=True
)
    with cb:
        val_real = (qc * 20) + (qs * 10) + (qb * 5)
        val_vis = min(val_real, 20)
        st.markdown(f'<div><b>SUMATORIA DESCUENTOS</b><div class="big-num">{val_vis}%</div></div>', unsafe_allow_html=True)
        if st.session_state.dto_base >= 20:
             st.success("¡Beneficio activado!")
        elif val_real >= 20:
            st.markdown('<div class="btn-active">', unsafe_allow_html=True)
            if st.button("ACTIVAR RECAMBIO", use_container_width=True):
                st.session_state.dto_base = 20
                st.session_state.tab_actual = "CATÁLOGO"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.button("MÍNIMO 20% REQUERIDO", use_container_width=True, disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 2: CATÁLOGO (ORDENADO POR PRECIO) ---
elif st.session_state.tab_actual == "CATÁLOGO":
    st.markdown('<div class="card"><div class="card-title">Seleccionar Máquina Nueva</div>', unsafe_allow_html=True)
    p = "assets/productos"
    
    nombres_reales = {
        "ABSR 12 COMPACT_2.png": "Taladro Destornillador ABS Compacto",
        "ABSR 20 COMBI_1.png": "Taladro Atornillador ABSR 20 Combinado",
        "ABSR 20 COMBI_2.png": "Taladro Atornillador ABSR 20 Compact",
        "ABSR 20 PWR COMBI_1.png": "Taladro Percutor y Atornillador ABSR 20 PWR Combi",
        "AWSR 20 COMPACT_1.png": "Amoladora Angular AWSR 20 Compact",
        "ASSR 20_3.png": "Atornillador de Impacto Master ASSR 20 14 inch Compact",                     
        "ASSR 20 - 12 POWER_1.png": "LLave de Impacto ASSR 20 - 1/2 Compact 20V",
        "ASSR 20 - 34_1.png": "LLave de Impacto ASSR 20 - 3/4 20V",
        "ABHR 20 LIGHT_1.png": "Rotomartillo Light",
        "ABHR 20 POWER_1.png": "Rotomartillo Power"
    }

    if os.path.exists(p):
        archivos = [f for f in os.listdir(p) if f.lower().endswith('.png')]
        if archivos and not df_precios.empty:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            
            # ORDENAMOS POR PRECIO
            # 1. Filtramos los productos del excel que tienen una imagen mapeada en la app
            df_valido = df_precios[df_precios['Imagen'].isin(nombres_reales.values())].copy()
            # 2. Ordenamos el DataFrame por precio
            df_ordenado = df_valido.sort_values(by='Precio', ascending=True)
            
            # 3. Creamos la lista de archivos basada en ese orden
            nombre_a_archivo = {v: k for k, v in nombres_reales.items()}
            archivos_finales = [nombre_a_archivo[n] for n in df_ordenado['Imagen'].tolist() if nombre_a_archivo[n] in archivos]
            
            if archivos_finales:
                sel = st.selectbox("Producto:", archivos_finales, format_func=mostrar_nombre)
                nombre_visible = mostrar_nombre(sel).strip()
                
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
                        dto_item = 30
                    else:
                        dto_item = 20
                        st.info(f"Faltan {max(0, faltantes_30)} unidad(es) para el 30%.")

                    if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                        st.session_state.carrito.append({"prod": nombre_visible, "precio": precio_lista, "dto": dto_item})
                        if len(st.session_state.carrito) >= 3:
                            for it in st.session_state.carrito: it['dto'] = 30
                        st.toast(f"✅ {nombre_visible} añadido")
                        st.rerun()
            else:
                st.warning("No se encontraron coincidencias entre el Excel y las fotos.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 3: PEDIDO ---
elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Resumen de Venta</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        total_acumulado = 0
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc, cd = st.columns([2.5, 1, 1, 0.5])
            subtotal = item['precio'] * (1 - item['dto']/100)
            total_acumulado += subtotal
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"${item['precio']:,.2f}")
            cc.write(f"**-{item['dto']}%**")
            if cd.button("❌", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20 if st.session_state.dto_base >= 20 else 0
                st.rerun()
        
        st.divider()
        st.markdown(f"### Total Final: ${total_acumulado:,.2f}")
        
        def generate_pdf():
            pdf = FPDF()
            pdf.set_auto_page_break(auto=False)
            pdf.add_page()
            if os.path.exists("logo_wurth.jpg"): pdf.image("logo_wurth.jpg", x=160, y=10, w=35)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "RESUMEN DE VENTA - PLAN RECAMBIO", ln=True, align='L')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 8, f"Cliente: {st.session_state.nombre_cliente}", ln=True)
            pdf.cell(0, 8, f"Nro. Cliente: {st.session_state.numero_cliente}", ln=True)
            pdf.cell(0, 8, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(100, 10, "Producto", 1, 0, 'C')
            pdf.cell(30, 10, "P. Lista", 1, 0, 'C')
            pdf.cell(20, 10, "Dto", 1, 0, 'C')
            pdf.cell(40, 10, "Subtotal", 1, 1, 'C')
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.carrito:
                sb = it['precio'] * (1 - it['dto']/100)
                pdf.cell(100, 10, it['prod'][:55], 1)
                pdf.cell(30, 10, f"${it['precio']:,.2f}", 1, 0, 'R')
                pdf.cell(20, 10, f"{it['dto']}%", 1, 0, 'C')
                pdf.cell(40, 10, f"${sb:,.2f}", 1, 1, 'R')
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, f"TOTAL: ${total_acumulado:,.2f}", ln=True, align='R')
            pdf.set_y(270)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 10, "Documento no oficial - Solo para fines informativos", 0, 0, 'C')
            return pdf.output(dest='S').encode('latin-1')

        pdf_bytes = generate_pdf()
        st.download_button(label="📥 DESCARGAR PDF", data=pdf_bytes, file_name=f"Venta_{st.session_state.nombre_cliente}.pdf", mime="application/pdf", use_container_width=True)
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
