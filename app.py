import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

# --- FUNCIONES DE SOPORTE ---
def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carga de recursos
f_bold = get_base64("WuerthBold.ttf")
f_book = get_base64("WuerthBook.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")

# --- ESTILOS MEJORADOS (CSS) ---
st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthBook'; src: url(data:font/ttf;base64,{f_book}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    html, body, [class*="css"] {{ font-family: 'WuerthBook', sans-serif; background-color: #F2F2F2; }}
    
    /* 1. Ajuste Logo para evitar cortes */
    .logo-container {{
        padding: 20px 0 10px 10px;
    }}

    /* Estilo de la Tarjeta de Producto (Limpio, sin rectángulos vacíos) */
    .product-display {{
        position: relative;
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}

    /* 3. Icono de Descuento Rojo */
    .discount-badge {{
        position: absolute;
        top: -15px;
        right: -15px;
        background-color: #CC0000;
        color: white;
        width: 90px;
        height: 90px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-family: 'WuerthExtra';
        box-shadow: 0 4px 12px rgba(204,0,0,0.4);
        z-index: 100;
        border: 4px solid white;
    }}

    .discount-badge .percent {{ font-size: 35px; line-height: 1; }}
    .discount-badge .text {{ font-size: 10px; text-transform: uppercase; }}

    .product-title {{
        font-family: 'WuerthBold';
        color: #333;
        margin-top: 20px;
        font-size: 1.3rem;
        text-transform: uppercase;
    }}

    /* Botones Würth */
    .stButton>button {{
        background-color: #CC0000;
        color: white;
        font-family: 'WuerthBold';
        border-radius: 5px;
        border: none;
        padding: 10px;
        width: 100%;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #000000;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE DATOS (Session State) ---
if 'descuento_seleccionado' not in st.session_state:
    st.session_state.descuento_seleccionado = 0
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- LÓGICA DE IMÁGENES ALEATORIAS ---
path_img = "assets/productos/"
imagenes = [f for f in os.listdir(path_img) if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(path_img) else []
if 'img_actual' not in st.session_state and imagenes:
    st.session_state.img_actual = random.choice(imagenes)

# --- HEADER (Punto 1: Logo ajustado) ---
col_logo, col_tit = st.columns([1.5, 4])
with col_logo:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists("logo_wurth.jpg"):
        st.image("logo_wurth.jpg", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
with col_tit:
    st.markdown(f"<h1 style='padding-top:20px;'>PLAN RECAMBIO</h1>", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
tabs = st.tabs(["📊 1. CALCULADORA", "🛠️ 2. CATÁLOGO", "📝 3. CONSOLIDACIÓN"])

# --- FASE 1: CALCULADORA ---
with tabs[0]:
    col_input, col_visual = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("Configuración de Beneficio")
        entrega = st.selectbox("Tipo de equipo entregado", 
                             ["Máquina Completa (Herramienta + 2 Bat + Cargador)", 
                              "Máquina Parcial (Solo Herramienta)", 
                              "Batería o Cargador Suelto"])
        cantidad = st.number_input("Cantidad de unidades a entregar", min_value=1, step=1)
        
        if st.button("CALCULAR DESCUENTO"):
            # Lógica temporal: Definimos valores para ver el cambio visual
            if "Completa" in entrega: st.session_state.descuento_seleccionado = 25
            elif "Parcial" in entrega: st.session_state.descuento_seleccionado = 15
            else: st.session_state.descuento_seleccionado = 10
            st.success(f"¡Descuento de {st.session_state.descuento_seleccionado}% activado!")

    with col_visual:
        # Contenedor de la herramienta
        st.markdown('<div class="product-display">', unsafe_allow_html=True)
        
        # Punto 3: Badge de descuento dinámico
        desc = st.session_state.descuento_seleccionado
        if desc > 0:
            st.markdown(f'''
                <div class="discount-badge">
                    <span class="percent">{desc}%</span>
                    <span class="text">OFF</span>
                </div>
            ''', unsafe_allow_html=True)
        
        if imagenes:
            img_path = os.path.join(path_img, st.session_state.img_actual)
            # Punto 2: Imagen auto-ajustada (no tan grande)
            st.image(img_path, width=350)
            
            nombre = st.session_state.img_actual.split('.')[0].replace('_', ' ').upper()
            st.markdown(f'<p class="product-title">{nombre}</p>', unsafe_allow_html=True)
        
        if st.button("🔄 MOSTRAR OTRO MODELO"):
            st.session_state.img_actual = random.choice(imagenes)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- FASE 2: CATÁLOGO (Mejora 2) ---
with tabs[1]:
    st.subheader("Catálogo de Recambio")
    if st.session_state.descuento_seleccionado == 0:
        st.warning("Debe calcular el descuento en la Fase 1 para ver los precios finales.")
    else:
        # Simulación de catálogo
        productos = [
            {"cod": "0700123", "desc": "Taladro Percutor M-CUBE", "precio": 450},
            {"cod": "0700456", "desc": "Amoladora Angular AWS", "precio": 380},
            {"cod": "0700789", "desc": "Atornillador de Impacto", "precio": 410}
        ]
        
        for p in productos:
            precio_final = p['precio'] * (1 - st.session_state.descuento_seleccionado/100)
            with st.expander(f"{p['desc']} - Cód: {p['cod']}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Precio Lista", f"USD {p['precio']}")
                c2.metric("Precio Recambio", f"USD {precio_final:.2f}", delta=f"-{st.session_state.descuento_seleccionado}%")
                if c3.button("Añadir al pedido", key=p['cod']):
                    st.session_state.carrito.append({"desc": p['desc'], "precio": precio_final})
                    st.toast(f"{p['desc']} añadido")

# --- FASE 3: CONSOLIDACIÓN ---
with tabs[2]:
    st.subheader("Resumen del Pedido")
    if not st.session_state.carrito:
        st.write("No hay productos seleccionados.")
    else:
        for item in st.session_state.carrito:
            st.write(f"✅ {item['desc']} --- **USD {item['precio']:.2f}**")
        
        st.divider()
        st.markdown("### TOTAL ESTIMADO: USD " + str(sum(i['precio'] for i in st.session_state.carrito)))
        st.caption("Nota: Este cálculo no incluye fletes ni impuestos.")
        if st.button("REINICIAR PLAN"):
            st.session_state.carrito = []
            st.session_state.descuento_seleccionado = 0
            st.rerun()
