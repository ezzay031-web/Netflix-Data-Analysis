import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 🎯 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# 🎨 PROFESSIONAL STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}

h1, h2, h3 {
    color: #e50914;
}

.block-container {
    padding: 2rem 3rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🎬 HEADER
# =========================
st.title("🎬 Netflix Analytics Dashboard (Portfolio Project)")
st.write("Built with Streamlit, Pandas, and Plotly")

# =========================
# 📂 LOAD DATA
# =========================
file = st.file_uploader("Upload Netflix CSV File", type=["csv"])

if file:

    df = pd.read_csv(file)
    df.dropna(inplace=True)

    # =========================
    # 📌 SIDEBAR FILTERS
    # =========================
    st.sidebar.header("🔎 Filters")

    content_type = st.sidebar.selectbox("Type", ["All"] + list(df["type"].unique()))
    year = st.sidebar.selectbox("Release Year", ["All"] + sorted(df["release_year"].unique(), reverse=True))

    if content_type != "All":
        df = df[df["type"] == content_type]

    if year != "All":
        df = df[df["release_year"] == year]

    # =========================
    # 📊 KPI DASHBOARD
    # =========================
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", len(df))
    col2.metric("Movies", (df["type"] == "Movie").sum())
    col3.metric("TV Shows", (df["type"] == "TV Show").sum())

    st.divider()

    # =========================
    # 📊 TYPE DISTRIBUTION
    # =========================
    st.subheader("🎭 Content Distribution")

    fig1 = px.histogram(df, x="type", color="type")
    st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # 🌍 TOP COUNTRIES
    # =========================
    st.subheader("🌍 Top 10 Countries")

    country_df = df["country"].value_counts().head(10).reset_index()
    country_df.columns = ["Country", "Count"]

    fig2 = px.bar(country_df, x="Country", y="Count")
    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # 📅 YEAR TREND
    # =========================
    st.subheader("📅 Content Over Time")

    year_df = df["release_year"].value_counts().sort_index().reset_index()
    year_df.columns = ["Year", "Count"]

    fig3 = px.line(year_df, x="Year", y="Count")
    st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # 📥 DOWNLOAD BUTTON
    # =========================
    st.subheader("📥 Export Data")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download Filtered Dataset",
        csv,
        "netflix_filtered_data.csv",
        "text/csv"
    )

    # =========================
    # 🎬 DATA PREVIEW
    # =========================
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    st.success("Dashboard Ready 🚀 Portfolio Project Completed")

else:
    st.info("Upload dataset to start analysis")

 else:
    st.info("Upload Netflix dataset to start analysis")
