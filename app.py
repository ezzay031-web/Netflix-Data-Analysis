import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

st.title(" Netflix Data Analysis Dashboard")
st.write("This project explores Netflix movies and TV shows dataset.")

# Upload dataset
file = st.file_uploader("Upload your Netflix CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader(" Data Preview")
    st.write(df.head())

    st.subheader(" Dataset Info")
    st.write(df.describe())

    # Missing values
    st.subheader(" Missing Values")
    st.write(df.isnull().sum())

    # Cleaning
    df = df.dropna()

    # Show type distribution
    st.subheader(" Content Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x="type", data=df, ax=ax)
    st.pyplot(fig)

    # Top countries
    st.subheader(" Top Content Countries")
    top_countries = df['country'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_countries.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Release year trend
    st.subheader(" Content Over Years")
    fig, ax = plt.subplots()
    df['release_year'].value_counts().sort_index().plot(ax=ax)
    st.pyplot(fig)

    st.success("Analysis completed successfully ")

else:
    st.info("Please upload Netflix dataset CSV file to start analysis")
