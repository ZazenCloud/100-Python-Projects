import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from pandas.plotting import register_matplotlib_converters

# Set the display format for floating-point numbers
pd.options.display.float_format = '{:,.2f}'.format

# Register converters for matplotlib to handle dates
register_matplotlib_converters()

# Read the CSV file into a DataFrame
df = pd.read_csv('data/cost_revenue_dirty.csv')

# Explore and Clean the Data
print(df.shape)
print(df.head())
print(df.isna().values.any())
print(df.duplicated().values.any())
print(df.info())

# List of characters to remove from the specified columns
chars_to_remove = ['$', ',']
# List of columns to process
columns = [
    'USD_Production_Budget',
    'USD_Worldwide_Gross',
    'USD_Domestic_Gross'
]

# Loop through each column and character to remove
for col in columns:
    for char in chars_to_remove:
        # Replace each character with an empty string
        df[col] = df[col].astype(str).str.replace(char, "")
    # Convert column to a numeric data type
    df[col] = pd.to_numeric(df[col])

# Convert the 'Release_Date' column to datetime format
df['Release_Date'] = pd.to_datetime(df['Release_Date'])

# Find the index of the film with the highest production budget
id_budget_max = df.USD_Production_Budget.idxmax()
# Find the index of the film with the lowest production budget
id_budget_min = df.USD_Production_Budget.idxmin()
print(df.loc[id_budget_max])
print(df.loc[id_budget_min])

# Investigating the Zero Revenue Films
# Print the number of films with zero domestic gross revenue
print(len(df[df.USD_Domestic_Gross == 0]))

# Display the top 10 films with zero domestic
# gross revenue, sorted by production budget
print(df[df.USD_Domestic_Gross == 0].sort_values(
    "USD_Production_Budget",
    ascending=False).head(10))

# Print the number of films with zero worldwide gross revenue
print(len(df[df.USD_Worldwide_Gross == 0]))

# Display the top 10 films with zero worldwide
# gross revenue, sorted by production budget
print(df[df.USD_Worldwide_Gross == 0].sort_values(
    "USD_Production_Budget", ascending=False
    ).head(10))

# Filter films with zero domestic gross but nonzero worldwide gross
international_releases = df.loc[
    (df.USD_Domestic_Gross == 0) &
    (df.USD_Worldwide_Gross != 0)
]
print(international_releases)
# OR
international_releases = df.query(
    'USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0'
)
print(international_releases)

# Date of Data Collection
scrape_date = pd.Timestamp('2018-5-1')
# Filter films with release dates after the data collection date
future_releases = df[df.Release_Date >= scrape_date]
# Create a new DataFrame by dropping future releases
df_clean = df.drop(future_releases.index)
# Display information about the cleaned DataFrame
print(df_clean.info())

# Query films that had a worldwide gross less than their production budget
lost_money = df_clean.query('USD_Worldwide_Gross < USD_Production_Budget')
# Calculate the percentage of films that lost money
print(round((len(lost_money) / len(df_clean) * 100), 2))

# Budget vs. Revenue Bubble Chart
# Set the figure size and dpi
plt.figure(figsize=(8, 4), dpi=200)
# Set the Seaborn styling for the plot
with sns.axes_style('dark'):
    # Create a scatter plot using Seaborn
    ax = sns.scatterplot(
        data=df_clean,
        x='USD_Production_Budget',
        y='USD_Worldwide_Gross',
        hue='USD_Worldwide_Gross',
        size='USD_Worldwide_Gross'
    )
    # Set plot limits and labels
    ax.set(
        ylim=(0, 3000000000),
        xlim=(0, 450000000),
        ylabel='Revenue in $ billions',
        xlabel='Budget in $100 millions'
    )

# Movie Releases over Time + Budget vs. Revenue Bubble Chart
# Set the figure size and dpi
plt.figure(figsize=(8, 4), dpi=200)
# Set the Seaborn styling for the plot
with sns.axes_style('darkgrid'):
    # Create a scatter plot using Seaborn
    ax = sns.scatterplot(
        data=df_clean,
        x='Release_Date',
        y='USD_Production_Budget',
        hue='USD_Worldwide_Gross',
        size='USD_Worldwide_Gross'
    )
    # Set plot limits and labels
    ax.set(
        ylim=(0, 450000000),
        xlim=(df_clean.Release_Date.min(), df_clean.Release_Date.max()),
        ylabel='Budget in $100 millions',
        xlabel='Year'
    )

# Create a datetime index from Release_Date
dt_index = pd.DatetimeIndex(df_clean.Release_Date)
years = dt_index.year
# Calculate decades based on the years
decades = (years // 10) * 10
# Create a new column with the values
df_clean['Decade'] = decades

# Filter films released before or in the 1960s
old_films = df_clean[df_clean.Decade <= 1960]
# Filter films released in the 1970s onwards
new_films = df_clean[df_clean.Decade > 1960]

# Display the film with the highest production budget among "old" films
print(old_films.sort_values('USD_Production_Budget', ascending=False).head(1))

# Seaborn Regression Plots
# Plot 1 (Old Films)
plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style("whitegrid"):
    sns.regplot(
        data=old_films,
        x='USD_Production_Budget',
        y='USD_Worldwide_Gross',
        scatter_kws={'alpha': 0.4},
        line_kws={'color': 'black'}
    )
# Plot 2 (New Films)
plt.figure(figsize=(8, 4), dpi=200)
with sns.axes_style("darkgrid"):
    ax = sns.regplot(
        data=new_films,
        x='USD_Production_Budget',
        y='USD_Worldwide_Gross',
        color='#2f4b7c',
        scatter_kws={'alpha': 0.25},
        line_kws={'color': '#ff7c43'}
    )
    ax.set(
        xlim=(0, 450000000),
        ylim=(0, 3000000000),
        xlabel='Budget in $100 millions',
        ylabel='Revenue in $ billions'
    )

# Create a LinearRegression model
regression = LinearRegression()

# Explanatory Variable(s) or Feature(s)
x = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
# Response Variable or Target
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])
# Fit the regression model
regression.fit(x, y)
# Display the intercept and coefficients
regression.intercept_
regression.coef_
# Calculate R-squared for the model
regression.score(x, y)

# Create another LinearRegression model
old_regression = LinearRegression()

# Explanatory Variable(s) or Feature(s)
x = pd.DataFrame(old_films, columns=['USD_Production_Budget'])
# Response Variable or Target
y = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])
# Fit the regression model
old_regression.fit(x, y)
# Display the intercept and coefficients
old_regression.intercept_
old_regression.coef_
# Calculate R-squared for the model
old_regression.score(x, y)

# Use the Model to Make a Prediction
budget = 350000000
revenue_estimate = regression.intercept_[0] + regression.coef_[0, 0]*budget
revenue_estimate = round(revenue_estimate, 2)
print(revenue_estimate)
