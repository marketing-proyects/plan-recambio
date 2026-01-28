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

# --- CARGA DE PRECIOS ---
@st.cache_data
def load_prices():
    # Tu CSV tiene una fila inicial "Power Tools", por eso skiprows=1 para leer los headers correctamente
    df = pd.read_csv("Lista_Precios - CORDLESS MACHINES.xlsx - Hoja1.csv", skiprows=1)
    # Limpiamos los nombres de productos (quitar saltos de línea y espacios extra) para que coincidan con el mapeo
    df['Producto_Match'] = df['Producto'].str.replace('\n', ' ').str.strip()
    return df

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
    
    # Mapeo manual para vincular imágenes con los nombres del Excel
    nombres_reales = {
        "ABSR 12 COMPACT_2.png": "TALADRO ATORNILLADOR ABSR 12 COMPACT 12V / 2.0AH",
        "ABSR 20 COMBI_1.png": "TALADRO ATORNILLADOR ABSR 20 COMBI 20 V / 2.0AH",
        "ABSR 20 COMBI_2.png": "TALADRO ATORNILLADOR ABSR 20 COMPACT 20 V / 2.0AH",
        "ABSR 20 PWR COMBI_1.png": "TALADRO PERCUTOR Y ATORNILLADOR ABSR 20 PWR COMBI 20 V / 4.0AH",
        "AWSR 20 COMPACT_1.png": "AMOLADORA ANGULAR AWSR 20 COMPACT 18V / 2.0AH",
        "ASSR 20_3.png": "ATORNILLADOR DE IMPACTO ASSR 20 20V / 4.0AH",
        "ASSR 20 - 12 POWER_1.png": "LLAVE DE IMPACTO ASSR 20 - 1/2 COMPACT 20V / 4.0AH",
        "ASSR 20 - 34_1.png": "LLAVE DE IMPACTO REDSTRIPE ASSR 20 - 3/4 20V / 8.0AH",
        "ABHR 20 LIGHT_1.png": "ROTOMARTILLO ABHR 20 LIGHT 20V / 4.0AH",
        "ABHR 20 POWER_1.png": "ROTOMARTILLO ABHR 20 POWER 18V / 5.0AH"
    }

    if os.path.exists(p):
        archivos = sorted([f for f in os.listdir(p) if f.lower().endswith('.png')])
        if archivos:
            def mostrar_nombre(archivo): return nombres_reales.get(archivo, archivo)
            sel = st.selectbox("Producto:", archivos, format_func=mostrar_nombre)
            
            # Buscamos el precio en el CSV
            nombre_a_buscar = mostrar_nombre(sel).upper()
            row = df_precios[df_precios['Producto_Match'].str.upper() == nombre_a_buscar]
            precio_lista = float(row['Precio'].iloc[0]) if not row.empty else 0.0

            ci, cs = st.columns(2)
            with ci: st.image(os.path.join(p, sel), width=280)
            with cs:
                st.markdown(f"### Precio Lista: **${precio_lista:,.2f}**")
                num_en_carro = len(st.session_state.carrito)
                
                if st.session_state.dto_base < 20:
                    st.error("Requiere completar la calculadora.")
                    dto_actual = 0
                else:
                    dto_actual = 30 if num_en_carro >= 2 else 20
                    if num_en_carro < 2:
                        st.info(f"Siguiente unidad activará el 30%")

                if st.button("AÑADIR AL PEDIDO", use_container_width=True):
                    st.session_state.carrito.append({
                        "prod": mostrar_nombre(sel), 
                        "precio": precio_lista,
                        "dto": 20
                    })
                    # Si al añadir llegamos a 3, todos suben al 30%
                    if len(st.session_state.carrito) >= 3:
                        for it in st.session_state.carrito: it['dto'] = 30
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PESTAÑA 3: PEDIDO ---
elif st.session_state.tab_actual == "PEDIDO":
    st.markdown(f'<div class="card"><div class="card-title">Pedido: {st.session_state.nombre_cliente}</div>', unsafe_allow_html=True)
    if st.session_state.carrito:
        total_acumulado = 0
        for i, item in enumerate(st.session_state.carrito):
            ca, cb, cc, cd = st.columns([2.5, 1, 1, 0.5])
            precio_con_dto = item['precio'] * (1 - item['dto']/100)
            total_acumulado += precio_con_dto
            
            ca.write(f"**{i+1}.** {item['prod']}")
            cb.write(f"${item['precio']:,.2f}")
            cc.write(f"**-{item['dto']}%**")
            if cd.button("❌", key=f"del_{i}"):
                st.session_state.carrito.pop(i)
                if len(st.session_state.carrito) < 3:
                    for it in st.session_state.carrito: it['dto'] = 20 if st.session_state.dto_base >= 20 else 0
                st.rerun()
        
        st.divider()
        st.markdown(f"## TOTAL FINAL: ${total_acumulado:,.2f}")

        # --- GENERACIÓN DE PDF ---
        def generate_pdf():
            pdf = FPDF()
            pdf.add_page()
            
            # Título y Logo (si existe)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="RESUMEN DE VENTA - WÜRTH", ln=True, align='C')
            pdf.ln(10)
            
            # Datos Cliente
            pdf.set_font("Arial", '', 12)
            pdf.cell(200, 8, txt=f"Cliente: {st.session_state.nombre_cliente}", ln=True)
            pdf.cell(200, 8, txt=f"N° Cliente: {st.session_state.numero_cliente}", ln=True)
            pdf.ln(10)
            
            # Tabla
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(100, 10, "Producto", 1)
            pdf.cell(30, 10, "P. Lista", 1, 0, 'C')
            pdf.cell(20, 10, "Dto", 1, 0, 'C')
            pdf.cell(40, 10, "P. Final", 1, 1, 'C')
            
            pdf.set_font("Arial", '', 9)
            for it in st.session_state.carrito:
                pf = it['precio'] * (1 - it['dto']/100)
                # Cortar nombre si es muy largo
                nombre_p = it['prod'][:50] + "..." if len(it['prod']) > 50 else it['prod']
                pdf.cell(100, 10, nombre_p, 1)
                pdf.cell(30, 10, f"${it['precio']:,.2f}", 1, 0, 'C')
                pdf.cell(20, 10, f"{it['dto']}%", 1, 0, 'C')
                pdf.cell(40, 10, f"${pf:,.2f}", 1, 1, 'C')
            
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(190, 10, txt=f"MONTO TOTAL A PAGAR: ${total_acumulado:,.2f}", ln=True, align='R')
            
            return pdf.output(dest='S').encode('latin-1')

        pdf_bytes = generate_pdf()
        st.download_button(
            label="📄 DESCARGAR DETALLE EN PDF",
            data=pdf_bytes,
            file_name=f"Cotizacion_{st.session_state.nombre_cliente}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("No hay productos seleccionados.")
    st.markdown('</div>', unsafe_allow_html=True)
