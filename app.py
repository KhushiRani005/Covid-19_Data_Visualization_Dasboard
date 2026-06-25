import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("COVID-19 Dashboard")
st.write("Visualizing COVID-19 Cases Around the World")

# Load Data
df = pd.read_csv("covid_data.csv")

# Convert Date
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar
st.sidebar.title("Dashboard Controls")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df['Country/Region'].unique())
)

# Filter Data
country_data = df[df['Country/Region'] == country]

# Latest Data
latest = country_data.sort_values('Date').iloc[-1]

# Metrics
st.header("Latest Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Confirmed Cases", int(latest['Confirmed']))
    st.metric("Recovered Cases", int(latest['Recovered']))

with col2:
    st.metric("Deaths", int(latest['Deaths']))
    st.metric("Active Cases", int(latest['Active']))

# Line Chart
st.header("Confirmed Cases Trend")

fig1 = px.line(
    country_data,
    x='Date',
    y='Confirmed',
    title=f'Confirmed Cases in {country}'
)

st.plotly_chart(fig1)

# Active Cases Chart
st.header("Active Cases Trend")

fig2 = px.bar(
    country_data,
    x='Date',
    y='Active',
    title='Active Cases Over Time'
)

st.plotly_chart(fig2)

# Pie Chart
st.header("Case Distribution")

pie_data = pd.DataFrame({
    'Category': ['Active', 'Recovered', 'Deaths'],
    'Count': [
        latest['Active'],
        latest['Recovered'],
        latest['Deaths']
    ]
})

fig3 = px.pie(
    pie_data,
    values='Count',
    names='Category'
)

st.plotly_chart(fig3)

# WHO Region Analysis
st.header("WHO Region Analysis")

region_data = df.groupby('WHO Region')['Confirmed'].max().reset_index()

fig4 = px.bar(
    region_data,
    x='WHO Region',
    y='Confirmed',
    title='Confirmed Cases by WHO Region'
)

st.plotly_chart(fig4)

# Raw Data
st.header("Dataset Preview")
st.dataframe(country_data.tail(20))