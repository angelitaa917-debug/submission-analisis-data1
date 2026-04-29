import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set(style="whitegrid")
plt.rcParams.update({'font.size': 8})  # supaya proporsional

# =========================
# HELPER FUNCTION
# =========================
def create_monthly_rent_df(df):
    return df.resample(rule='ME', on='dteday').agg({
        "cnt": "sum"
    }).reset_index()

def generate_monthly_insight(df):
    monthly = df.resample(rule='ME', on='dteday')['cnt'].sum()
    growth = ((monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0]) * 100

    if growth > 0:
        return f"📈 Penyewaan meningkat sebesar {growth:.1f}% dari awal hingga akhir periode."
    else:
        return f"📉 Penyewaan menurun sebesar {abs(growth):.1f}%."

def generate_workingday_insight(df):
    work_avg = df[df["workingday"] == 1]["cnt"].mean()
    hol_avg = df[df["workingday"] == 0]["cnt"].mean()

    diff = ((work_avg - hol_avg) / hol_avg) * 100

    if work_avg > hol_avg:
        return f"🏢 Hari kerja lebih tinggi sekitar {diff:.1f}% dibanding hari libur."
    else:
        return f"🎉 Hari libur lebih tinggi sekitar {abs(diff):.1f}% dibanding hari kerja."

def peak_insight(df):
    peak = df.loc[df["cnt"].idxmax()]
    return f"🔥 Puncak terjadi pada {peak['dteday'].date()} dengan {peak['cnt']:,} penyewaan."

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("main_data.csv")
df["dteday"] = pd.to_datetime(df["dteday"])
df.sort_values(by="dteday", inplace=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("Filter Data")

    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    start_date, end_date = st.date_input(
        "Pilih Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# =========================
# FILTER DATA
# =========================
main_df = df[
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date))
]

# =========================
# HEADER
# =========================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Analisis penggunaan sepeda berdasarkan waktu dan tipe hari")
st.markdown("---")

# =========================
# KPI
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total", f"{main_df['cnt'].sum():,}")
col2.metric("Rata-rata", f"{main_df['cnt'].mean():.0f}")
col3.metric("Maksimum", f"{main_df['cnt'].max():,}")

st.info(peak_insight(main_df))

st.markdown("---")

# =========================
# VISUALISASI 1 (TREND)
# =========================
st.subheader("📈 Tren Penyewaan Bulanan")

monthly_df = create_monthly_rent_df(main_df)

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(7,3))  # ukuran sudah ideal
    ax.plot(monthly_df["dteday"], monthly_df["cnt"], marker='o')

    ax.set_title("Tren Bulanan", fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("Jumlah")

    plt.xticks(rotation=20)
    st.pyplot(fig)

with col2:
    st.info(generate_monthly_insight(main_df))

st.markdown("---")

# =========================
# VISUALISASI 2 (WORKING DAY)
# =========================
st.subheader("📊 Working Day vs Holiday")

working_df = main_df.groupby("workingday")["cnt"].mean().reset_index()

col1, col2 = st.columns([1.5, 1])

with col1:
    fig, ax = plt.subplots(figsize=(5,3))  # tidak terlalu besar

    sns.barplot(data=working_df, x="workingday", y="cnt", ax=ax)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Holiday", "Working"])

    ax.set_title("Rata-rata Penyewaan", fontsize=10)
    ax.set_ylabel("Avg")

    ax.grid(axis="y", linestyle="--", alpha=0.3)

    st.pyplot(fig)

with col2:
    st.info(generate_workingday_insight(main_df))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Submission Dicoding - Ezra Angelita 🚀")
