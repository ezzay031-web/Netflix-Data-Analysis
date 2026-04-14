import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
#  PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =========================
#  NETFLIX THEME CSS (Dark + Red Accents)
# =========================
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #141414;
        color: #ffffff;
        font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Headers & titles - improved visibility */
    h1, h2, h3, .stSubheader, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #e50914 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        text-shadow: 1px 1px 0px #00000080;
    }

    /* Make subheaders inside markdown also red & bold */
    .stSubheader {
        color: #e50914 !important;
        font-size: 1.8rem !important;
        border-left: 4px solid #e50914;
        padding-left: 15px;
        margin-top: 20px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #1f1f1f;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
        border-left: 4px solid #e50914;
    }
    [data-testid="stMetric"] label {
        color: #e5e5e5 !important;   /* brighter than before */
        font-weight: 600;
        font-size: 1rem;
    }
    [data-testid="stMetric"] .stMetricValue {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 800;
    }

    /* Sidebar (if used) */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #0b0b0b;
    }

    /* Select boxes, text inputs, buttons */
    .stSelectbox, .stTextInput, .stFileUploader {
        background-color: #2a2a2a;
        border-radius: 8px;
        border: 1px solid #333333;
        color: white;
    }
    .st-bw, .st-bx {
        background-color: #2a2a2a;
        color: white;
    }
    .stButton > button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #f40612;
        box-shadow: 0 0 8px #e50914;
        transform: scale(1.02);
    }

    /* Divider */
    hr {
        border-top: 1px solid #333333;
    }

    /* Sample titles section */
    .sample-card {
        background-color: #1f1f1f;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 8px;
        border-left: 3px solid #e50914;
    }

    /* Info & success boxes */
    .stAlert {
        background-color: #1f1f1f;
        border-left: 4px solid #e50914;
        color: #e5e5e5;
    }
    .stSuccess {
        background-color: #1a2a1a;
        border-left-color: #00e5a0;
    }

    /* Dataframe / tables (if any) */
    .dataframe {
        background-color: #1f1f1f !important;
        color: #e5e5e5 !important;
        border-collapse: collapse;
    }
    .dataframe th {
        background-color: #2a2a2a !important;
        color: #e50914 !important;
    }
    .dataframe td {
        border-color: #333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
#  HEADER (Netflix Logo Style)
# =========================
st.markdown("<h1 style='text-align:center;'>🎬 Netflix Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#b3b3b3;'>Explore Netflix movies & TV shows like a pro dashboard</p>", unsafe_allow_html=True)

# =========================
#  UPLOAD DATA
# =========================
file = st.file_uploader("Upload Netflix CSV file", type=["csv"])

if file:

    df = pd.read_csv(file)
    df = df.dropna()

    # =========================
    #  SEARCH BAR (NETFLIX STYLE)
    # =========================
    search = st.text_input("🔍 Search Movies or TV Shows")

    if search:
        df = df[df['title'].str.contains(search, case=False, na=False)]

    # =========================
    #  FILTERS
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
    #  KPI METRICS
    # =========================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", len(df))
    col2.metric("Movies", len(df[df["type"] == "Movie"]))
    col3.metric("TV Shows", len(df[df["type"] == "TV Show"]))

    st.divider()

    # =========================
    #  TYPE DISTRIBUTION (INTERACTIVE) - NOW BARS ARE RED
    # =========================
    fig1 = px.histogram(
        df, x="type", color="type",
        title="Content Type Distribution",
        color_discrete_sequence=["#e50914"]  # <-- Force all bars red
    )
    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#1f1f1f",
        font=dict(color="#e5e5e5"),
        title_font=dict(color="#e50914", size=20),
        legend_title_font=dict(color="#e50914"),
        showlegend=False  # not needed if only one color
    )
    st.plotly_chart(fig1, use_container_width=True)

    # =========================
    #  TOP COUNTRIES - BARS RED
    # =========================
    top_country = df["country"].value_counts().head(10).reset_index()
    top_country.columns = ["country", "count"]

    fig2 = px.bar(
        top_country, x="country", y="count",
        title="Top 10 Countries",
        color_discrete_sequence=["#e50914"]  # <-- Red bars
    )
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#1f1f1f",
        font=dict(color="#e5e5e5"),
        title_font=dict(color="#e50914"),
        xaxis=dict(title="Country", color="#b3b3b3"),
        yaxis=dict(title="Number of Titles", color="#b3b3b3")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # RELEASE YEAR TREND - line chart (no bars)
    # =========================
    year_data = df["release_year"].value_counts().sort_index().reset_index()
    year_data.columns = ["year", "count"]

    fig3 = px.line(year_data, x="year", y="count", title="Content Over Years")
    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="#141414",
        plot_bgcolor="#1f1f1f",
        font=dict(color="#e5e5e5"),
        title_font=dict(color="#e50914"),
        xaxis=dict(title="Release Year", color="#b3b3b3"),
        yaxis=dict(title="Count", color="#b3b3b3")
    )
    fig3.update_traces(line=dict(color="#e50914", width=3))  # red line
    st.plotly_chart(fig3, use_container_width=True)

    # =========================
    #  MOVIE POSTER THUMBNAILS (SIMULATED) - NETFLIX ROW STYLE
    # =========================
    st.subheader("🎬 Sample Titles")
    st.markdown("---")

    for i in range(min(10, len(df))):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("🎞️")
        with col2:
            st.markdown(
                f"<div class='sample-card'><strong>{df.iloc[i]['title']}</strong><br>{df.iloc[i]['type']} | {df.iloc[i]['release_year']} | {df.iloc[i]['country']}</div>",
                unsafe_allow_html=True
            )

    st.success("Netflix Dashboard Loaded Successfully 🍿")

else:
    st.info("📂 Upload Netflix dataset to start analysis")
