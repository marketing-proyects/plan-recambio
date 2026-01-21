import streamlit as st
import base64
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Plan Recambio | Würth", layout="wide")

def get_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Recursos
f_bold = get_base64("WuerthBold.ttf")
f_extra = get_base64("WuerthExtraBoldCond.ttf")
logo_w = get_base64("logo_wurth.jpg")
logo_rs = get_base64("logo_red_stripe.png")

# Lógica de archivos
path_fondos = "assets2/" 
path_prod = "assets/productos/"
fondos = [f for f in os.listdir(path_fondos) if f.lower().endswith(('.jpg', '.png'))] if os.path.exists(path_fondos) else []
productos = sorted([f for f in os.listdir(path_prod) if f.lower().endswith('.png')]) if os.path.exists(path_prod) else []

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'bg' not in st.session_state and fondos: st.session_state.bg = random.choice(fondos)

# --- CSS DE ALTO IMPACTO ---
bg_base64 = get_base64(os.path.join(path_fondos, st.session_state.bg)) if fondos else ""

st.markdown(f"""
    <style>
    @font-face {{ font-family: 'WuerthBold'; src: url(data:font/ttf;base64,{f_bold}); }}
    @font-face {{ font-family: 'WuerthExtra'; src: url(data:font/ttf;base64,{f_extra}); }}

    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), 
                    url(data:image/jpg;base64,{bg_base64});
        background-size: cover;
        background-position: center;
    }}

    /* Contenedor Central Único */
    .main-showcase {{
        position: relative;
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        padding: 40px;
    }}

    /* EL GLOBO: Grande y sobre la herramienta */
    .floating-badge {{
        position: absolute;
        top: 20px;
        right: 1
