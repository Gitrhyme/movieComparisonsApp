import streamlit as st
import pandas as pd
import plotly.express as px

#Dataset Filter System
def loadData(chosenYear, chosenMonth, chosenLang):
  url = "https://raw.githubusercontent.com/samgitmaster/CSC310/main/mymoviedb.csv"
  df = pd.read_csv(url, lineterminator='\n')
  df['Year'] = pd.DatetimeIndex(df['Release_Date']).year
  df['Month'] = pd.DatetimeIndex(df['Release_Date']).month
  df = df.drop(columns = ['Poster_Url'])
  df2 = df[df['Year'] == chosenYear]
  df3 = df2[df2['Month'] == chosenMonth]
  df4 = df3[df3['Original_Language'] == chosenLang]
  return df4

st.title('Movie Comparison')

st.subheader("This app allows you to filter a movie dataset by year, month, and language.")
st.subheader("It then displays movie ratings by vote average. The 43 most common movie languages have been provided.")
st.markdown("**For best results, use en(English) or ja(Japanese)**")

st.sidebar.header('Movies Filter')

chosenYear = st.sidebar.selectbox('Year', list(reversed(range(1970, 2023))))
chosenMonth = st.sidebar.selectbox('Month', list(range(1, 13)))
uniqueLang = ['en', 'ja', 'fr', 'hi', 'es', 'ru', 'de', 'th', 'ko', 'tr', 'cn',
       'zh', 'it', 'pt', 'ml', 'pl', 'fi', 'no', 'da', 'id', 'sv', 'nl',
       'te', 'sr', 'is', 'ro', 'tl', 'fa', 'uk', 'nb', 'eu', 'lv', 'ar',
       'el', 'cs', 'ms', 'bn', 'ca', 'la', 'ta', 'hu', 'he', 'et']
chosenLang = st.sidebar.selectbox('Language', uniqueLang)

df = loadData(chosenYear, chosenMonth, chosenLang)

st.dataframe(df)

moviesByAverage = (
    df.groupby(by=['Title']).sum()[['Vote_Average']].sort_values('Vote_Average', ascending=True)
)

figVoteAvg = px.bar(
    moviesByAverage,
    x="Vote_Average",
    y=moviesByAverage.index,
    orientation = "h",
    title = "<b>Movies By Vote Average Score</b>",
    color_discrete_sequence = ["#0083B8"] * len(moviesByAverage),
    template = "plotly_white",
)

st.plotly_chart(figVoteAvg)
