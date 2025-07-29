import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io

st.title("Aplikasi Kesihatan Ringkas")

# -------------------
# Nama Pengguna
# -------------------

nama = st.text_input("Masukkan nama anda:")

st.markdown("---")

# -------------------
# Kalkulator BMI
# -------------------

st.header("📏 Kalkulator BMI")

berat = st.number_input("Berat (kg)", min_value=1.0, format="%.1f")
tinggi = st.number_input("Tinggi (cm)", min_value=1.0, format="%.1f")

bmi = None
kategori_bmi = ""
if berat and tinggi:
    bmi = berat / ((tinggi / 100) ** 2)
    st.write(f"BMI: {bmi:.2f}")

    if bmi < 18.5:
        kategori_bmi = "Kurus"
    elif bmi < 25:
        kategori_bmi = "Normal"
    elif bmi < 30:
        kategori_bmi = "Berlebihan berat"
    else:
        kategori_bmi = "Obes"

    st.write(f"Status: **{kategori_bmi}**")

st.markdown("---")

# -------------------
# Pengira Kalori Ringkas
# -------------------

st.header("🔥 Pengira Kalori Harian Ringkas")

gender = st.selectbox("Pilih jantina:", ["Lelaki", "Perempuan"])
default_cal = 2500 if gender == "Lelaki" else 2000

target_cal = st.number_input(
    "Sasaran kalori harian (kcal):", 
    value=default_cal
)

eaten = st.number_input(
    "Masukkan jumlah kalori yang telah dimakan (kcal):", 
    min_value=0,
    value=0
)

baki = target_cal - eaten

if nama:
    st.write(f"**{nama}**, jumlah kalori dimakan: **{eaten} kcal**")
else:
    st.write(f"Jumlah kalori dimakan: **{eaten} kcal**")

if baki > 0:
    st.success(f"Kalori belum cukup: {baki} kcal lagi")
elif baki < 0:
    st.error(f"Terlampau {abs(baki)} kcal dari sasaran!")
else:
    st.info("Tepat cukup kalori!")

# -------------------
# Papar & Simpan Graf
# -------------------

if nama and berat and tinggi and bmi is not None:
    # Data hari ini
    data_hari_ini = {
        "Nama": [nama],
        "Berat (kg)": [berat],
        "Tinggi (cm)": [tinggi],
        "BMI": [round(bmi, 2)],
        "Kategori BMI": [kategori_bmi],
        "Jantina": [gender],
        "Kalori Dimakan": [eaten],
        "Baki Kalori": [baki]
    }
    df_hari_ini = pd.DataFrame(data_hari_ini)

    # Graf bar kalori hari ini
    graf_baki = max(baki, 0)
    fig, ax = plt.subplots(figsize=(5,3))
    bars = ax.bar(["Dimakan", "Baki"], [eaten, graf_baki], color=["orange", "green"])
    ax.set_ylabel("Kalori (kcal)")
    ax.set_title("Kalori Harian")

    # Letak info pengguna atas graf
    info_teks = f"Nama: {nama}  |  Berat: {berat}kg  |  Tinggi: {tinggi}cm  |  Status: {kategori_bmi}"
    
    plt.tight_layout()
    plt.figtext(0.5, 1.02, info_teks, wrap=True, horizontalalignment='center', fontsize=10)

    # Label atas bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.0f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    st.pyplot(fig)

    # Simpan ke CSV
    nama_fail_csv = f"data_kesihatan_{nama}.csv" if nama else "data_kesihatan.csv"
    csv = df_hari_ini.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Muat Turun Data Kesihatan (CSV)",
        data=csv,
        file_name=nama_fail_csv,
        mime='text/csv'
    )

    # Simpan graf ke PNG dalam memory
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    plt.close(fig)

    st.download_button(
        label="📸 Muat Turun Graf Kalori (PNG)",
        data=img_buffer,
        file_name=f"graf_kalori_{nama}.png" if nama else "graf_kalori.png",
        mime="image/png"
    )

else:
    st.info("Sila lengkapkan maklumat Nama, Berat dan Tinggi sebelum meneruskan.")
