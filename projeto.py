import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Localização GPS Exata", layout="centered")

st.title("🌐 Captura Automática de Localização Exata (GPS)")

coords = streamlit_js_eval(
    js_code="await new Promise((resolve, reject) => { navigator.geolocation.getCurrentPosition(pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}), err => reject(err)); });",
    key="get_geolocation",
)

if coords:
    st.success(f"Localização Capturada: {coords}")
    
    # Salvar no CSV
    filename = "gps_logs.csv"
    coords_data = pd.DataFrame([{
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = pd.concat([df, coords_data], ignore_index=True)
    else:
        df = coords_data
    
    df.to_csv(filename, index=False)
    st.success("Localização salva com sucesso no arquivo gps_logs.csv")
else:
    st.info("Aguardando permissão de localização no navegador...")
