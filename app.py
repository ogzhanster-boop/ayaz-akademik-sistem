import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Ayaz Akademik Karar Sistemi", layout="wide")

st.title("🎯 Ayaz Profesyonel Akademik Karar Sistemi")

HEDEF_PUAN = 460

# Session State Veri Saklama
if "veri" not in st.session_state:
st.session_state.veri = pd.DataFrame(columns=["Tarih", "Deneme", "GunlukSoru"])

# Sidebar
st.sidebar.header("📌 Veri Girişi")

il = st.sidebar.selectbox("İl Seçiniz", ["İstanbul", "Ankara", "İzmir", "Diğer"])

deneme = st.sidebar.number_input("Deneme Puanı", 0, 500, 400)
gunluk_soru = st.sidebar.number_input("Günlük Çözülen Soru", 0, 500, 120)

if st.sidebar.button("Veriyi Kaydet"):
yeni_veri = pd.DataFrame({
"Tarih": [datetime.now()],
"Deneme": [deneme],
"GunlukSoru": [gunluk_soru]
})
st.session_state.veri = pd.concat([st.session_state.veri, yeni_veri], ignore_index=True)

st.subheader("📊 Performans Paneli")

if not st.session_state.veri.empty:

df = st.session_state.veri

ortalama = df["Deneme"].mean()
son_puan = df["Deneme"].iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Son Deneme", son_puan)
col2.metric("Ortalama Puan", round(ortalama,1))
col3.metric("Hedef", HEDEF_PUAN)

# Trend Grafiği
fig = px.line(df, x="Tarih", y="Deneme", title="Deneme Puan Trend")
st.plotly_chart(fig, use_container_width=True)

# Projeksiyon Hesabı
if len(df) > 1:
x = np.arange(len(df))
y = df["Deneme"]
coef = np.polyfit(x, y, 1)
trend = coef[0]

tahmini_6ay = son_puan + trend * 24

st.subheader("🔮 6 Aylık Projeksiyon")
st.write("Tahmini 6 Ay Sonra Puan:", round(tahmini_6ay,1))

if tahmini_6ay < HEDEF_PUAN:
st.error("⚠ Hedef risk altında. Çalışma yoğunluğu artırılmalı.")
else:
st.success("✔ Hedef doğrultusunda ilerleniyor.")

else:
st.info("Henüz veri girilmedi.")
