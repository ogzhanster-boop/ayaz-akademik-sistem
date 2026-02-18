import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="Ayaz Akademik Karar Sistemi", layout="wide")

st.title("🎯 Ayaz Profesyonel Akademik Karar Sistemi")

HEDEF_PUAN = 460
DATA_FILE = "veriler.csv"

# Veri yükleme
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "Tarih","Deneme",
        "Turkce","Matematik","Fen",
        "Inkilap","Din","Ingilizce",
        "ToplamNet"
    ])

# Sidebar veri girişi
st.sidebar.header("📌 Deneme Girişi")

deneme = st.sidebar.number_input("Deneme Puanı", 0, 500, 400)

turkce = st.sidebar.number_input("Türkçe Net", 0.0, 20.0, 15.0)
matematik = st.sidebar.number_input("Matematik Net", 0.0, 20.0, 12.0)
fen = st.sidebar.number_input("Fen Net", 0.0, 20.0, 14.0)
inkilap = st.sidebar.number_input("İnkılap Net", 0.0, 10.0, 8.0)
din = st.sidebar.number_input("Din Net", 0.0, 10.0, 8.0)
ingilizce = st.sidebar.number_input("İngilizce Net", 0.0, 10.0, 8.0)

if st.sidebar.button("Veriyi Kaydet"):

    toplam_net = (
        turkce + matematik + fen +
        inkilap + din + ingilizce
    )

    yeni_veri = pd.DataFrame({
        "Tarih":[datetime.now()],
        "Deneme":[deneme],
        "Turkce":[turkce],
        "Matematik":[matematik],
        "Fen":[fen],
        "Inkilap":[inkilap],
        "Din":[din],
        "Ingilizce":[ingilizce],
        "ToplamNet":[toplam_net]
    })

    df = pd.concat([df, yeni_veri], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("Veri kaydedildi.")

# Panel
st.subheader("📊 Performans Paneli")

if not df.empty:

    son_puan = df["Deneme"].iloc[-1]
    ortalama = df["Deneme"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Son Deneme", son_puan)
    col2.metric("Ortalama", round(ortalama,1))
    col3.metric("Hedefe Mesafe", HEDEF_PUAN - son_puan)

    fig = px.line(df, x="Tarih", y="Deneme", title="Deneme Trend")
    st.plotly_chart(fig, use_container_width=True)

    # Ders ortalamaları
    dersler = ["Turkce","Matematik","Fen","Inkilap","Din","Ingilizce"]
    ort_ders = df[dersler].mean()

    st.subheader("📚 Ders Analizi")

    fig2 = px.bar(
        x=ort_ders.index,
        y=ort_ders.values,
        title="Ders Ortalama Netleri"
    )
    st.plotly_chart(fig2, use_container_width=True)

    zayif_iki = ort_ders.nsmallest(2)
    st.warning(f"Zayıf Dersler: {zayif_iki.index[0]} ve {zayif_iki.index[1]}")

    # Trend analizi
    if len(df) > 1:
        x = np.arange(len(df))
        y = df["Deneme"]
        trend = np.polyfit(x, y, 1)[0]

        tahmini_6ay = son_puan + trend * 24

        st.subheader("🔮 6 Aylık Projeksiyon")
        st.write("Tahmini 6 Ay Sonra:", round(tahmini_6ay,1))

        if tahmini_6ay < HEDEF_PUAN:
            st.error("⚠ Hedef risk altında. Haftalık plan artırılmalı.")
        else:
            st.success("✔ Hedef doğrultusunda ilerleniyor.")

else:
    st.info("Henüz veri girilmedi.")
