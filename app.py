import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 🎬 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
# 🎨 NETFLIX STYLE UI
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }

    h1, h2, h3 {
        color: #e50914;
        font-weight: bold;
    }

    .card {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 🎬 HEADER (Netflix Logo Style)
# =========================
st.markdown("<h1 style='text-align:center;'>🎬 Netflix Analytics Dashboard</h1>", unsafe_allow_html=True)
st.write("Explore Netflix movies & TV shows like a pro dashboard")

# =========================
# 📂 UPLOAD DATA
# =========================
file = st.file_uploader("Upload Netflix CSV file", type=["csv"])

if file:

    df = pd.read_csv(file)
    df = df.dropna()

    # =========================
    # 🔎 SEARCH BAR (NETFLIX STYLE)
    # =========================
    search = st.text_input("🔎 Search Movies or TV Shows")

    if search:
        df = df[df['title'].str.contains(search, case=False, na=False)]

    # =========================
    # 🎯 FILTERS
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        type_filter = st.selectbox("Type", ["All"] + list(df["type"].unique()))

    with col2:
        year_filter = st.selectbox("Release Year", ["All"] + sorted(df["release_year"].unique(), reverse=True))

    with col3:
        country_filter = st.selectbox("Country", ["All"] + list(df["country"].dropna().unique())[:50])

    # Apply filters
    if type_filter != "All":
        df = df[df["type"] == type_filter]

    if year_filter != "All":
        df = df[df["release_year"] == year_filter]

    if country_filter != "All":
        df = df[df["country"] == country_filter]

    # =========================
    # 📊 KPI METRICS
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", len(df))
    col2.metric("Movies", len(df[df["type"] == "Movie"]))
    col3.metric("TV Shows", len(df[df["type"] == "TV Show"]))

    st.divider()

    # =========================
    # 🎭 TYPE DISTRIBUTION (INTERACTIVE)
    # =========================
    fig1 = px.histogram(df, x="type", color="type", title="Content Type Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    # =========================
    # 🌍 TOP COUNTRIES
    # =========================
    top_country = df["country"].value_counts().head(10).reset_index()
    top_country.columns = ["country", "count"]

    fig2 = px.bar(top_country, x="country", y="count", title="Top 10 Countries")
    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # 📅 RELEASE YEAR TREND
    # =========================
    year_data = df["release_year"].value_counts().sort_index().reset_index()
    year_data.columns = ["year", "count"]

    fig3 = px.line(year_data, x="year", y="count", title="Content Over Years")
    st.plotly_chart(fig3, use_container_width=True)

    # =========================
    # 🎬 MOVIE POSTER THUMBNAILS (SIMULATED)
    # =========================
    st.subheader("🎬 Sample Titles")

    for i in range(min(10, len(df))):
        col1, col2 = st.columns([1, 4])

        with col1:
            st.markdown("🎬")

        with col2:
            st.write(f"**{df.iloc[i]['title']}**")
            st.write(f"{df.iloc[i]['type']} | {df.iloc[i]['release_year']} | {df.iloc[i]['country']}")

        st.divider()

    # =========================
    # 🎉 SUCCESS
    # =========================
    st.success("Netflix Dashboard Loaded Successfully 🎬")

else:
    st.info("Upload Netflix dataset to start analysis")
