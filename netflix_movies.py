'''
Import libraries
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("Netflix Data Explorer")

# Load Google Sheet
sheet_id = '1UTFc0NPiAAYVuY3F6TJ_IyYcfH-K6zxE2TBbSVaWu-Y'
sheet_name = 'Sheet1'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

netflix_df = load_data(url)

st.subheader("Dataset Preview")
st.dataframe(netflix_df)

# ───────────────────────────────────────────
# HISTOGRAM 1: Duration (raw)
# ───────────────────────────────────────────
st.subheader("Histogram – Duration (all movies & TV shows)")

plt.figure(figsize=(10, 5))
plt.hist(netflix_df.iloc[:, 8], bins=30)
plt.xlabel("Duration")
plt.ylabel("Number of Movies")
plt.title("Most Frequent Duration")
st.pyplot(plt)

# ───────────────────────────────────────────
# FILTERING
# ───────────────────────────────────────────
movies_only = netflix_df[netflix_df['type'] == 'Movie']

movies90 = movies_only[
    (movies_only['release_year'] >= 1990) &
    (movies_only['release_year'] < 2000)
].copy()

movies90['duration_minutes'] = (
    movies90['duration']
    .astype(str)
    .str.extract(r'(\d+)')
    .astype(float)
)

duration = int(movies90['duration_minutes'].mode()[0])

st.subheader("Most Frequent Duration (1990–1999 movies)")
st.write(duration)

action_movies = movies90[movies90['genre'] == 'Action']

short_movie_count = int(
    action_movies[action_movies['duration_minutes'] < 90].shape[0]
)

st.subheader("Number of Action Movies < 90 min (90s)")
st.write(short_movie_count)

# ───────────────────────────────────────────
# HISTOGRAM 2: 90s movie durations
# ───────────────────────────────────────────
st.subheader("Histogram – Duration of 90s Movies")

plt.figure(figsize=(10, 6))
plt.hist(
    movies90['duration_minutes'],
    bins=range(28, 196),
    edgecolor='black',
    align='left'
)
plt.title("Duration of Movies Released per Year (1990–1999)")
plt.xlabel("Duration")
plt.ylabel("Number of Movies")
plt.xticks(range(28, 195, 10))
st.pyplot(plt)

