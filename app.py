import streamlit as st
import base64
import os
import random
import pandas as pd
from fpdf import FPDF
from io import BytesIO

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

# --- CARGA DE DATOS (EXCEL SIMPLIFICADO) ---
@st.cache_data
def load_prices():
    try:
        # Cargamos el archivo simplificado
        df = pd.read_excel("Lista_Precios.xlsx", sheet_name="Hoja1")
        # Filtro: Solo filas donde Producto, Imagen, Código y Precio tengan datos
        df = df.dropna(subset=["Producto", "Imagen", "Código", "Precio"])
        return df
    except Exception as e:
        st.error(f"Error cargando Lista_Precios.xlsx: {e}")
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
    header {{ visibility: hidden; }}
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

# --- PESTAÑA 2: CATÁLOGO ---
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
        "ABHR 20 LIGHT_1.png": "Rotomartillo Light",
        "ABHR 20 POWER_1.png": "Rotomartillo Power"
    }

    if os.path.exists(p):
        archivos = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if archivos:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            
            # Filtramos el selectbox: solo mostramos archivos que están mapeados en el Excel (columna Imagen)
            opciones_validas = [f for f in archivos if mostrar_nombre(f) in df_precios['Imagen'].values]
            
            if opciones_validas:
                sel = st.selectbox("Producto:", opciones_validas, format_func=mostrar_nombre)
                
                # Buscamos la fila correspondiente en el Excel usando el nombre visible
                nombre_visible = mostrar_nombre(sel)
                info_prod = df_precios[df_precios['Imagen'] == nombre_visible].iloc[0]
                
                ci, cs = st.columns(2)
                with ci: st.image(os.path.join(p, sel), width=280)
                with cs:
                    # Mostramos Precio y Código del Excel
                    st.markdown(f"### Precio: ${info_prod['Precio']:,.2f}")
                    st.write(f"**Código:** {info_prod['Código']}")
                    
                    num_en_carro = len(st.session_state.carrito)
                    if st.session_state.dto_base < 20:
                        st.error("Descuento 0%: Pase por la calculadora.")
                        dto_item = 0
                    else:
                        faltantes = 3 - num_en_carro
                        if num_en_carro >= 2:
                            st.success("¡Beneficio 30% activado!")
                            dto_item = 30
                        else:
                            dto_item = 20
                            st.info(f"Faltan {faltantes if faltantes > 0 else 0} unidad(es) para el 30%.")

                    if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                        st.session_state.carrito.append({
                            "prod": nombre_visible, 
                            "precio": float(info_prod['Precio']),
                            "dto": 20
                        })
                        if len(st.session_state.carrito) >= 3:
                            for it in st.session_state.carrito: it['dto'] = 30
                        st.toast(f"✅ {nombre_visible} añadido")
                        st.rerun()
            else:
                st.warning("No se encontraron productos con información completa en el Excel.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 3: PEDIDO ---
elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        monto_total = 0.0
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc, cd = st.columns([2.5, 1, 1, 0.5])
            p_lista = item['precio']
            descuento = item['dto']
            subtotal = p_lista * (1 - descuento/100)
            monto_total += subtotal
            
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"${p_lista:,.2f}")
            cc.write(f"**-{descuento}%**")
            if cd.button("❌", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20 if st.session_state.dto_base >= 20 else 0
                st.rerun()
        
        st.divider()
        st.markdown(f"### Monto Total Final: ${monto_total:,.2f}")
        
        # --- GENERACIÓN DE PDF ---
        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Resumen de Pedido - Würth Plan Recambio", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Cliente: {st.session_state.nombre_cliente}", ln=True)
            pdf.cell(0, 10, f"Nro Cliente: {st.session_state.numero_cliente}", ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(100, 10, "Producto", 1)
            pdf.cell(30, 10, "Precio Lista", 1)
            pdf.cell(20, 10, "Dto", 1)
            pdf.cell(40, 10, "Subtotal", 1, ln=True)
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.carrito:
                sb = it['precio'] * (1 - it['dto']/100)
                pdf.cell(100, 10, it['prod'][:50], 1)
                pdf.cell(30, 10, f"${it['precio']:,.2f}", 1)
                pdf.cell(20, 10, f"{it['dto']}%", 1)
                pdf.cell(40, 10, f"${sb:,.2f}", 1, ln=True)
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, f"TOTAL: ${monto_total:,.2f}", ln=True, align='R')
            return pdf.output(dest='S').encode('latin-1')

        pdf_bytes = generate_pdf()
        st.download_button(
            label="📥 DESCARGAR DETALLE EN PDF",
            data=pdf_bytes,
            file_name=f"Venta_{st.session_state.nombre_cliente.replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("El pedido está vacío.")
    st.markdown('</div>', unsafe_allow_html=True)
