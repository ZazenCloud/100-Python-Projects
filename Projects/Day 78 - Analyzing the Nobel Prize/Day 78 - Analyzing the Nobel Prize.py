import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Set the display format for floating-point numbers
pd.options.display.float_format = '{:,.2f}'.format

# Read the CSV file into a DataFrame
df_data = pd.read_csv('data/nobel_prize_data.csv')

# Explore the data
print(df_data.shape)
print(df_data.info())
print(df_data.columns)

# Sort DataFrame by year
years = df_data.year.sort_values(ascending=True)
# First Nobel Prize of the DataFrame
years.head(1)
# Last Nobel Prize of the DataFrame
years.tail(1)

# Check for duplicates and NaN values
print(df_data.duplicated().values.any())
print(df_data.isna().values.any())
print(df_data.isna().sum())

# Convert Year and Birth Date to Datetime
df_data.birth_date = pd.to_datetime(df_data.birth_date)

# Add a column with the Prize Share as a percentage
separated_values = df_data.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(separated_values[0])
denomenator = pd.to_numeric(separated_values[1])
df_data['share_pct'] = numerator / denomenator

# Donut Chart: Percentage of Male vs. Female laureates
sex = df_data.sex.value_counts()
fig = px.pie(
    labels=sex.index,
    values=sex.values,
    title="Percentage of Male vs. Female Winners",
    names=sex.index,
    hole=0.3
)
fig.update_traces(textposition='inside', textfont_size=16, textinfo='percent')
fig.show()

# First 3 female Nobel laureates
df_data[df_data.sex == 'Female'].sort_values('year', ascending=True)[:3]

# People that won multiple Nobel Prizes
is_winner = df_data.duplicated(subset=['full_name'])
multiple_winners = df_data[is_winner]
print(multiple_winners['full_name'])

# Number of categories in the Nobel Prize
df_data.category.nunique()

# Bar Chart: Number of Prizes per Category
prizes_per_category = df_data.category.value_counts()
category_bar = px.bar(
    x=prizes_per_category.index,
    y=prizes_per_category.values,
    color=prizes_per_category.values,
    color_continuous_scale='Aggrnyl',
    title='Number of Prizes Awarded per Category'
)
category_bar.update_layout(
    xaxis_title='Nobel Prize Category',
    coloraxis_showscale=False,
    yaxis_title='Number of Prizes'
)
category_bar.show()

# First Nobel Prize of Economics
df_data[df_data.category == 'Economics'].sort_values('year').head(1)

# Bar Chart: Male and Female Winners by Category
cat_men_women = df_data.groupby(
    ['category', 'sex'],
    as_index=False
).agg({'prize': pd.Series.count})
cat_men_women.sort_values('prize', ascending=False, inplace=True)

man_women_category_bar = px.bar(
    x=cat_men_women.category,
    y=cat_men_women.prize,
    color=cat_men_women.sex,
    title='Number of Prizes Awarded per Category split by Men and Women'
)
man_women_category_bar.update_layout(
    xaxis_title='Nobel Prize Category',
    yaxis_title='Number of Prizes'
)
man_women_category_bar.show()

# Number of Nobel Prizes per year
prize_per_year = df_data.groupby(by='year').count().prize
moving_average = prize_per_year.rolling(window=5).mean()

# Plot for number of prizes across the years
plt.figure(figsize=(16, 8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(
    ticks=np.arange(1900, 2021, step=5),
    fontsize=14,
    rotation=45
)
ax = plt.gca()
ax.set_xlim(1900, 2020)
ax.scatter(x=prize_per_year.index,
           y=prize_per_year.values,
           color='dodgerblue',
           alpha=0.7,
           s=100,)

ax.plot(prize_per_year.index,
        moving_average.values,
        color='crimson',
        linewidth=3,)
plt.show()

# Number of Nobel Prizes shares per year
yearly_avg_share = df_data.groupby(
    by='year'
).agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()

# Plot for number of prizes shares across the years
plt.figure(figsize=(16, 8), dpi=200)
plt.title('Number of Nobel Prizes Awarded per Year', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(
    ticks=np.arange(1900, 2021, step=5),
    fontsize=14,
    rotation=45
)
ax1 = plt.gca()
ax2 = ax1.twinx()
ax1.set_xlim(1900, 2020)
ax2.invert_yaxis()
ax1.scatter(
    x=prize_per_year.index,
    y=prize_per_year.values,
    color='dodgerblue',
    alpha=0.7,
    s=100
)
ax1.plot(
    prize_per_year.index,
    moving_average.values,
    color='crimson',
    linewidth=3
)
ax2.plot(
    prize_per_year.index,
    share_moving_average.values,
    color='grey',
    linewidth=3
)
plt.show()

# Top 20 countries with the most Nobel Prizes
top_countries = df_data.groupby(
    ['birth_country_current'],
    as_index=False
).agg({'prize': pd.Series.count})
top_countries.sort_values(by='prize', inplace=True)
top20_countries = top_countries[-20:]

# Bar Chart: Top 20 Countries by Number of Prizes
countries_most_bar = px.bar(
    x=top20_countries.prize,
    y=top20_countries.birth_country_current,
    orientation='h',
    color=top20_countries.prize,
    color_continuous_scale='Viridis',
    title='Top 20 Countries by Number of Prizes'
)
countries_most_bar.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Country',
    coloraxis_showscale=False
)
countries_most_bar.show()

# Grouping data by ISO (country code)
df_countries = df_data.groupby(
    ['birth_country_current', 'ISO'],
    as_index=False
).agg({'prize': pd.Series.count})
df_countries.sort_values('prize', ascending=False)

# Choropleth Map: Number of Prizes Won by Country
world_map = px.choropleth(
    df_countries,
    locations='ISO',
    color='prize',
    hover_name='birth_country_current',
    color_continuous_scale=px.colors.sequential.matter
)
world_map.update_layout(coloraxis_showscale=True)
world_map.show()

# Create a DataFrame that groups the number of prizes by country and category
cat_country = df_data.groupby(
    ['birth_country_current', 'category'],
    as_index=False
).agg({'prize': pd.Series.count})
# Sort the DataFrame by the number of prizes in descending order
cat_country.sort_values(by='prize', ascending=False, inplace=True)
# Merge DataFrames
merged_df = pd.merge(cat_country, top20_countries, on='birth_country_current')
# Rename the columns of the merged DataFrame
merged_df.columns = [
    'birth_country_current',
    'category',
    'cat_prize',
    'total_prize'
]
# Sort by the total number of prizes in ascending order
merged_df.sort_values(by='total_prize', inplace=True)

# Horizontal Bar Chart: Top 20 Countries by Number of Prizes and Category
category_cpuntry_bar = px.bar(
    x=merged_df.cat_prize,
    y=merged_df.birth_country_current,
    color=merged_df.category,
    orientation='h',
    title='Top 20 Countries by Number of Prizes and Category'
)
category_cpuntry_bar.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Country'
)
category_cpuntry_bar.show()

# Create a DataFrame that groups the number of prizes by country and year
prize_by_year = df_data.groupby(
    by=['birth_country_current', 'year'],
    as_index=False
).count()
# Sort by year and selects only the columns of interest
prize_by_year = prize_by_year.sort_values('year')[
    ['year', 'birth_country_current', 'prize']
]
# Creates a DataFrame that calculates the cumulative
# sum of prizes for each country over time
cumulative_prizes = prize_by_year.groupby(
    by=['birth_country_current', 'year']
).sum().groupby(level=[0]).cumsum()
# Reset the index of the DataFrame to make it easier to manipulate
cumulative_prizes.reset_index(inplace=True)

# Line Chart: Number of Prizes Won by Each Country Over Time
line_chart = px.line(
    cumulative_prizes,
    x='year',
    y='prize',
    color='birth_country_current',
    hover_name='birth_country_current'
)
line_chart.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Prizes'
)
line_chart.show()

# Top 20 organizations with the most Nobel Prizes
top20_orgs = df_data.organization_name.value_counts()[:20]
top20_orgs.sort_values(ascending=True, inplace=True)

# Horizontal Bar Chart: Top 20 Research Institutions by Number of Prizes
org_bar = px.bar(
    x=top20_orgs.values,
    y=top20_orgs.index,
    orientation='h',
    color=top20_orgs.values,
    color_continuous_scale=px.colors.sequential.haline,
    title='Top 20 Research Institutions by Number of Prizes'
)
org_bar.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='Institution',
    coloraxis_showscale=False
)
org_bar.show()

# Top 20 cities with the most researches
top20_org_cities = df_data.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)

# Horizontal Bar Chart: Which Cities Do the Most Research?
city_bar2 = px.bar(
    x=top20_org_cities.values,
    y=top20_org_cities.index,
    orientation='h',
    color=top20_org_cities.values,
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Which Cities Do the Most Research?'
)
city_bar2.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='City',
    coloraxis_showscale=False
)
city_bar2.show()

# Top 20 cities with the most Nobel Prizes laureates born there
top20_cities = df_data.birth_city.value_counts()[:20]
top20_cities.sort_values(ascending=True, inplace=True)

# Horizontal Bar Chart: Where were the Nobel Laureates Born?
city_bar = px.bar(
    x=top20_cities.values,
    y=top20_cities.index,
    orientation='h',
    color=top20_cities.values,
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Where were the Nobel Laureates Born?'
)
city_bar.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='City of Birth',
    coloraxis_showscale=False
)
city_bar.show()

# Create a DataFrame that groups the number of prizes by the country,
# city, and name of the organization where the laureates worked
country_city_org = df_data.groupby(
    by=[
        'organization_country',
        'organization_city',
        'organization_name'
    ],
    as_index=False
).agg({'prize': pd.Series.count})
# Sort by the number of prizes in descending order
country_city_org = country_city_org.sort_values('prize', ascending=False)

# Sunburst Chart: Where do Discoveries Take Place?
burst = px.sunburst(
    country_city_org,
    path=['organization_country', 'organization_city', 'organization_name'],
    values='prize',
    title='Where do Discoveries Take Place?',
)
burst.update_layout(
    xaxis_title='Number of Prizes',
    yaxis_title='City',
    coloraxis_showscale=False
)
burst.show()

# Extract the birth year of the laureates (from the datetime object)
birth_years = df_data.birth_date.dt.year
# Creates a new column called winning_age, which is the
# difference between the year of the prize and the birth year
df_data['winning_age'] = df_data.year - birth_years

# The oldest Nobel laureate
print(df_data.nlargest(n=1, columns='winning_age'))
# The youngest Nobel laureate
print(df_data.nsmallest(n=1, columns='winning_age'))

# Plot of distribution of age on receipt of a Nobel Prize
plt.figure(figsize=(8, 4), dpi=200)
sns.histplot(
    data=df_data,
    x=df_data.winning_age,
    bins=30
)
plt.xlabel('Age')
plt.title('Distribution of Age on Receipt of Prize')
plt.show()

# Histogram Chart: Distribution of laureates age across the years
plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(
        data=df_data,
        x='year',
        y='winning_age',
        lowess=True,
        scatter_kws={'alpha': 0.4},
        line_kws={'color': 'black'}
    )
plt.show()

# Box Chart: Winning Age Across the Nobel Prize Categories
plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.boxplot(data=df_data,
                x='category',
                y='winning_age')
plt.show()

# Regression Chart: Winning Age Across the Nobel Prize Categories and Years
with sns.axes_style("whitegrid"):
    sns.lmplot(
        data=df_data,
        x='year',
        y='winning_age',
        hue='category',
        lowess=True,
        aspect=2,
        scatter_kws={'alpha': 0.5},
        line_kws={'linewidth': 5}
    )
plt.show()
