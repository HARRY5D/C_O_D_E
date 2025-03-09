# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Load data
# @st.cache_data
# def load_data():
#     file_path = "Shark Tank US dataset.csv"
#     df = pd.read_csv(file_path)
#     return df

# df = load_data()

# st.title("Startup Investment Tracker")

# # Industry-wise funding trends
# st.subheader("Industry-wise Funding Trends")
# industry_funding = df.groupby("Industry")['Total Deal Amount'].sum().sort_values(ascending=False).head(10)
# fig, ax = plt.subplots()
# sns.barplot(x=industry_funding.values, y=industry_funding.index, ax=ax)
# ax.set_xlabel("Total Investment (in $)")
# st.pyplot(fig)

# # Investment trends per season
# st.subheader("Investment Trends per Season")
# season_funding = df.groupby("Season Number")['Total Deal Amount'].sum()
# fig, ax = plt.subplots()
# ax.plot(season_funding.index, season_funding.values, marker='o', linestyle='-')
# ax.set_xlabel("Season Number")
# ax.set_ylabel("Total Investment (in $)")
# st.pyplot(fig)

# # Top-funded startups
# st.subheader("Top 10 Funded Startups")
# top_startups = df[['Startup Name', 'Total Deal Amount']].sort_values(by='Total Deal Amount', ascending=False).head(10)
# st.table(top_startups)

# Import only required components
from streamlit import title, subheader, pyplot, table, cache_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and cache data
@cache_data
def load_data():
    return pd.read_csv("Shark Tank US dataset.csv")

df = load_data()

# Dashboard title
title("Startup Investment Tracker")

# Industry funding visualization
subheader("Industry-wise Funding Trends")
industry_data = df.groupby("Industry")['Total Deal Amount'].sum()
top_industries = industry_data.nlargest(10)

fig_industry, ax_industry = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_industries.values, y=top_industries.index, ax=ax_industry)
ax_industry.set_xlabel("Total Investment ($)")
pyplot(fig_industry)
plt.close(fig_industry)

# Season trends visualization
subheader("Investment Trends per Season")
season_data = df.groupby("Season Number")['Total Deal Amount'].sum()

fig_season, ax_season = plt.subplots(figsize=(10, 4))
ax_season.plot(season_data.index, season_data.values, 'o-')
ax_season.set_xlabel("Season")
ax_season.set_ylabel("Total Investment ($)")
pyplot(fig_season)
plt.close(fig_season)

# Top startups table
subheader("Top 10 Funded Startups")
top_deals = df.nlargest(10, 'Total Deal Amount')[['Startup Name', 'Total Deal Amount']]
table(top_deals)