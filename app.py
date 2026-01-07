
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="DC Bike Rentals Dashboard", layout="wide")

st.title("🚲 Washington D.C. Bike Rentals Dashboard")
st.markdown("Analysis of bike-sharing demand based on weather and time factors.")

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season'] = df['season'].map(season_map)

    def day_period(hour):
        if 0 <= hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'

    df['day_period'] = df['hour'].apply(day_period)

    return df

df = load_data()

st.sidebar.header("🔎 Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    options=df['year'].unique(),
    default=df['year'].unique()
)

season_filter = st.sidebar.multiselect(
    "Select Season",
    options=df['season'].unique(),
    default=df['season'].unique()
)

workingday_filter = st.sidebar.radio(
    "Working Day",
    options=[0, 1],
    format_func=lambda x: "Non-working day" if x == 0 else "Working day"
)

filtered_df = df[
    (df['year'].isin(year_filter)) &
    (df['season'].isin(season_filter)) &
    (df['workingday'] == workingday_filter)
]

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", int(filtered_df['count'].sum()))
col2.metric("Avg Hourly Rentals", round(filtered_df['count'].mean(), 1))
col3.metric("Max Hourly Rentals", int(filtered_df['count'].max()))

st.subheader("🕒 Mean Hourly Rentals")

fig1, ax1 = plt.subplots()
sns.lineplot(data=filtered_df, x='hour', y='count', estimator=np.mean, ax=ax1)
ax1.set_ylabel("Mean Rentals")
st.pyplot(fig1)

st.subheader("📅 Mean Rentals by Month")

fig2, ax2 = plt.subplots()
sns.barplot(data=filtered_df, x='month', y='count', estimator=np.mean, ax=ax2)
st.pyplot(fig2)

st.subheader("🍂 Mean Rentals by Season")

fig3, ax3 = plt.subplots()
sns.barplot(data=filtered_df, x='season', y='count', estimator=np.mean, ax=ax3)
st.pyplot(fig3)

st.subheader("🌦️ Rentals by Weather Category")

fig4, ax4 = plt.subplots()
sns.barplot(data=filtered_df, x='weather', y='count', ci=95, ax=ax4)
st.pyplot(fig4)

st.subheader("🌅 Rentals by Period of Day")

fig5, ax5 = plt.subplots()
sns.barplot(
    data=filtered_df,
    x='day_period',
    y='count',
    estimator=np.mean,
    ax=ax5
)
st.pyplot(fig5)

st.markdown("""
### 📌 Key Insights
- Bike demand peaks during **commuting hours**
- **Working days** show higher registered usage
- **Clear weather and warmer seasons** lead to higher rentals
""")
