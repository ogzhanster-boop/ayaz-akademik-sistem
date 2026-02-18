import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Ayaz Akademik Sistem", layout="wide")

st.title("📊 Ayaz Akademik Karar Sistemi")

st.sidebar.header("Veri Girişi")

deneme_puani = st.sidebar.number_input("Deneme Puanı", 0, 500, 400)
gunluk_soru = st.sidebar.number_input("Günlük Çözülen Soru", 0, 500, 100)

st.metric("Son Deneme Puanı", deneme_puani)
st.metric("Günlük Soru", gunluk_soru)

data = pd.DataFrame({
"Kategori": ["Deneme Puanı", "Günlük Soru"],
"Değer": [deneme_puani, gunluk_soru]
})

fig = px.bar(data, x="Kategori", y="Değer")

st.plotly_chart(fig, use_container_width=True)
