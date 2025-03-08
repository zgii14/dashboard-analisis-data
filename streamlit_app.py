import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Analisis Bike Sharing dengan Streamlit")
st.write("Menjelajahi faktor-faktor yang mempengaruhi peminjaman sepeda.")

df_hour = pd.read_csv("data/hour.csv")
df_day = pd.read_csv("data/day.csv")

df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    st.image("bike-sharing.png")
    start_date, end_date = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df_filtered = df_day[(df_day["dteday"] >= pd.to_datetime(start_date)) & 
                     (df_day["dteday"] <= pd.to_datetime(end_date))]

st.subheader("Data Peminjaman Sepeda yang Difilter")
st.dataframe(df_filtered.head())

st.subheader("Rata-rata Peminjaman Sepeda per Musim")

df_season = df_day.groupby("season")["cnt"].mean().reset_index()

season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
df_season["season_label"] = df_season["season"].map(season_labels)

df_season = df_season.sort_values(by="cnt", ascending=True)

colors = ["#63b3ed"] * (len(df_season) - 1) + ["#2b6cb0"]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season_label", y="cnt", data=df_season, palette=colors, ax=ax)

plt.title("Rata-rata Peminjaman Sepeda per Musim", fontsize=14, fontweight="bold")
plt.xlabel("Musim", fontsize=12)
plt.ylabel("Rata-rata Peminjaman", fontsize=12)
plt.ylim(0, df_season["cnt"].max() + 1000)

for i, row in enumerate(df_season.itertuples()):
    ax.text(i, row.cnt + 100, int(row.cnt), ha="center", fontsize=12, fontweight="bold")

st.pyplot(fig)

st.subheader("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca")

df_weather = df_day.groupby("weathersit")["cnt"].mean().reset_index()
weather_labels = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan"}
df_weather["weather_label"] = df_weather["weathersit"].map(weather_labels)
df_weather = df_weather.sort_values(by="cnt", ascending=True)

colors = ["#63b3ed"] * (len(df_weather) - 1) + ["#2b6cb0"]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="weather_label", y="cnt", data=df_weather, palette=colors, ax=ax)
plt.xlabel("Kondisi Cuaca", fontsize=12)
plt.title("Rata-rata Peminjaman Sepeda Berdasarkan Kondisi Cuaca", fontsize=14, fontweight='bold')
plt.ylabel("Rata-rata Peminjaman", fontsize=12)
plt.ylim(0, df_weather["cnt"].max() + 1000)

for i, row in enumerate(df_weather.itertuples()):
    ax.text(i, row.cnt + 100, int(row.cnt), ha="center", fontsize=12, fontweight="bold")

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Dampak Kelembapan terhadap Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df_day["hum"], y=df_day["cnt"], alpha=0.6, color="blue", edgecolor=None, ax=ax)
sns.regplot(x=df_day["hum"], y=df_day["cnt"], scatter=False, color="black", line_kws={"linestyle": "dashed"}, ax=ax)
plt.title("Dampak Kelembapan terhadap Peminjaman Sepeda", fontsize=14, fontweight="bold")
plt.xlabel("Kelembapan (%)", fontsize=12)
plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
plt.ylim(0, df_day["cnt"].max() + 1000)
st.pyplot(fig)

st.subheader("Dampak Kecepatan Angin terhadap Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=df_day["windspeed"], y=df_day["cnt"], alpha=0.6, color="red", edgecolor=None, ax=ax)
sns.regplot(x=df_day["windspeed"], y=df_day["cnt"], scatter=False, color="black", line_kws={"linestyle": "dashed"}, ax=ax)
plt.title("Dampak Kecepatan Angin terhadap Peminjaman Sepeda", fontsize=14, fontweight="bold")
plt.xlabel("Kecepatan Angin", fontsize=12)
plt.ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
plt.ylim(0, df_day["cnt"].max() + 1000)
st.pyplot(fig)

st.subheader("Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari")

df_hourly = df_hour.groupby("hr")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x="hr", y="cnt", data=df_hourly, marker="o", color="b", ax=ax)

plt.title("Pola Peminjaman Sepeda Berdasarkan Jam dalam Sehari", fontsize=14, fontweight="bold")
plt.xlabel("Jam", fontsize=12)
plt.ylabel("Rata-rata Peminjaman", fontsize=12)
plt.xticks(range(0, 24))
plt.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)
