import pandas as pd
import plotly.express as px

# Show numeric output in decimal format (e.g. 2.15)
pd.options.display.float_format = '{:,.2f}'.format

# Read the CSV file into a DataFrame
df_apps = pd.read_csv('data/apps.csv')

# Drop 'Last_Updated' and 'Android_Ver' columns from the DataFrame
df_apps.drop(['Last_Updated', 'Android_Ver'], axis=1, inplace=True)

# Create a new DataFrame by dropping rows with missing values
df_apps_clean = df_apps.dropna()

# Drop duplicate rows based on 'App' and 'Price' columns
df_apps_clean.drop_duplicates(subset=['App', 'Price'], inplace=True)

# Count the occurrences of each value in the 'Content_Rating' column
ratings = df_apps_clean.Content_Rating.value_counts()

# Create a pie chart for ratings
pie = px.pie(
    labels=ratings.index,
    values=ratings.values,
    title="Content Rating",
    names=ratings.index,
)
pie.update_traces(textposition='outside', textinfo='percent+label')
pie.show()

# Create a donut chart for ratings
donut = px.pie(
    labels=ratings.index,
    values=ratings.values,
    title="Content Rating",
    names=ratings.index,
    hole=0.6,
)
donut.update_traces(
    textposition='inside',
    textfont_size=15,
    textinfo='percent'
)
donut.show()

# Convert 'Installs' and 'Price' columns to numeric
df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(
    ',', ""
)
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)

# Filter DataFrame to apps with price <= $250
df_apps_clean = df_apps_clean.loc[df_apps_clean['Price'] <= 250]

# Calculate 'Revenue_Estimate' column by multiplying 'Installs' and 'Price'
df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(
    df_apps_clean.Price
)

# Calculate Top 10 categories
top10_category = df_apps_clean.Category.value_counts()[:10]

# Create a bar chart for Top 10 categories
bar = px.bar(
    x=top10_category.index,
    y=top10_category.values
)
bar.show()

# Calculate total installs per category
category_installs = df_apps_clean.groupby('Category').agg(
    {'Installs': pd.Series.sum}
)
category_installs.sort_values('Installs', ascending=True, inplace=True)

# Create a horizontal bar chart for category popularity
h_bar = px.bar(
    x=category_installs.Installs,
    y=category_installs.index,
    orientation='h',
    title='Category Popularity'
)
h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
h_bar.show()

# Calculate app count per category
category_concentration = df_apps_clean.groupby('Category').agg(
    {'App': pd.Series.count}
)

# Merge app count and total installs DataFrames
category_merged_df = pd.merge(
    category_concentration,
    category_installs,
    on='Category',
    how="inner"
)

# Create a scatter plot for category concentration
scatter = px.scatter(
    category_merged_df,
    x="App",
    y="Installs",
    title='Category Concentration',
    color="Installs",
    size="App",
    hover_name=category_merged_df.index
)
scatter.update_layout(
    yaxis=dict(type='log'),
    xaxis_title='Number of Apps (Lower = More Concentrated)'
)
scatter.show()

# Split the nested data in the 'Genres' column
stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
# Calculate the count of genres
num_genres = stack.value_counts()

# Create a colored bar chart for Top 15 genres
colored_bar = px.bar(
    x=num_genres.index[:15],
    y=num_genres.values[:15],
    title='Top Genres',
    hover_name=num_genres.index[:15],
    color=num_genres.values[:15],
    color_continuous_scale='Agsunset'
)
colored_bar.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Apps',
    coloraxis_showscale=False
)
colored_bar.show()

# Group apps by category and type
df_free_vs_paid = df_apps_clean.groupby(
    ["Category", "Type"],
    as_index=False
).agg({'App': pd.Series.count})

# Create a grouped bar chart for free/paid apps by category
group_bar = px.bar(
    df_free_vs_paid,
    x='Category',
    y='App',
    title='Free vs Paid Apps by Category',
    color='Type',
    barmode='group'
)
group_bar.update_layout(
    xaxis_title='Category',
    yaxis_title='Number of Apps',
    xaxis={'categoryorder': 'total descending'},
    yaxis=dict(type='log')
)
group_bar.show()

# Create a box plot to analyze downloads of free and paid apps
box = px.box(
    df_apps_clean,
    y='Installs',
    x='Type',
    color='Type',
    notched=True,
    points='all',
    title='How Many Downloads are Paid Apps Giving Up?'
)
box.update_layout(yaxis=dict(type='log'))
box.show()

# Filter DataFrame for paid apps
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']

# Create a box plot for revenue estimates
revenue_box = px.box(
    df_paid_apps,
    x='Category',
    y='Revenue_Estimate',
    title='How Much Can Paid Apps Earn?'
)
revenue_box.update_layout(
    xaxis_title='Category',
    yaxis_title='Paid App Ballpark Revenue',
    xaxis={'categoryorder': 'min ascending'},
    yaxis=dict(type='log')
)
revenue_box.show()

# Create a box plot to analyze price distribution among paid apps
price_box = px.box(
    df_paid_apps,
    x='Category',
    y="Price",
    title='Price per Category'
)
price_box.update_layout(
    xaxis_title='Category',
    yaxis_title='Paid App Price',
    xaxis={'categoryorder': 'max descending'},
    yaxis=dict(type='log')
)
price_box.show()
