import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🎬 Netflix Style UI (CSS)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    h1, h2, h3 {
        color: #e50914;
        font-family: Arial;
    }

    .stFileUploader {
        background-color: #111111;
        border: 2px solid #e50914;
        padding: 10px;
        border-radius: 10px;
    }

    .stDataFrame {
        background-color: #111111;
    }

    div.stButton > button {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }

    div.stButton > button:hover {
        background-color: #b00610;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎬 Title
st.title("🎬 Netflix Data Analysis Dashboard")
st.write("Explore Netflix movies & TV shows like Netflix UI")

# Upload dataset
file = st.file_uploader("Upload your Netflix CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("📊 Data Preview")
    st.write(df.head())

    st.subheader("📌 Dataset Info")
    st.write(df.describe())

    # Missing values
    st.subheader("❌ Missing Values")
    st.write(df.isnull().sum())

    # Clean data
    df = df.dropna()

    # Type distribution
    st.subheader("🎭 Content Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x="type", data=df, ax=ax)
    ax.set_facecolor("#111111")
    st.pyplot(fig)

    # Top countries
    st.subheader("🌍 Top Content Countries")
    top_countries = df['country'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_countries.plot(kind='bar', ax=ax, color="#e50914")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Release year trend
    st.subheader("📅 Content Over Years")
    fig, ax = plt.subplots()
    df['release_year'].value_counts().sort_index().plot(ax=ax, color="#e50914")
    st.pyplot(fig)

    st.success("🎉 Analysis completed successfully!")

else:
    st.info("📂 Please upload Netflix dataset CSV file to start analysis")
    st.info("Please upload Netflix dataset CSV file to start analysis")
