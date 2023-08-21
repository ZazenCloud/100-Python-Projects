import pandas as pd
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read data from CSV files and convert them into DataFrames
df_tesla = pd.read_csv('data/TESLA Search Trend vs Price.csv')
df_btc_search = pd.read_csv('data/Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('data/Daily Bitcoin Price.csv')
df_unemployment = pd.read_csv('data/UE Benefits Search vs UE Rate 2004-19.csv')
df_unempl_2020 = pd.read_csv("data/UE Benefits Search vs UE Rate 2004-20.csv")

# Get the maximum and minimum values for Tesla in Web Search
tesla_max_search = df_tesla.TSLA_WEB_SEARCH.max()
tesla_min_search = df_tesla.TSLA_WEB_SEARCH.min()
print(f'Largest value for Tesla in Web Search: {tesla_max_search}')
print(f'Smallest value for Tesla in Web Search: {tesla_min_search}')

# Get the statistical summary of the Tesla DataFrame
df_tesla.describe()

# Get the maximum value for "Unemployment Benefits" in Web Search
unemployment_max_search = df_unemployment.UE_BENEFITS_WEB_SEARCH.max()
print('Largest value for "Unemployemnt Benefits" '
      f'in Web Search: {unemployment_max_search}')

# Get the maximum BTC News Search value
max_bitcoin_search = df_btc_search.BTC_NEWS_SEARCH.max()
print(f'largest BTC News Search: {max_bitcoin_search}')

# Check for missing values in the DataFrames
print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
print(f'Missing values for BTC price?: {df_btc_price.isna().values.any()}')
print(f'Number of missing values: {df_btc_price.isna().values.sum()}')
df_btc_price[df_btc_price.CLOSE.isna()]

# Drop rows with missing values from BTC Price DataFrame
df_btc_price.dropna(inplace=True)

# Convert the 'MONTH' column to datetime format
# Print for checking
df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
print(type(df_tesla.MONTH[0]))
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
print(type(df_unemployment.MONTH[0]))
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
print(type(df_btc_search.MONTH[0]))
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)
print(type(df_btc_price.DATE[0]))
df_unempl_2020.MONTH = pd.to_datetime(df_unempl_2020.MONTH)
print(type(df_unempl_2020.MONTH[0]))

# Create a resampled DataFrame for Bitcoin price data
df_btc_monthly = df_btc_price.resample('M', on='DATE').last()

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

# Register date converters to avoid warning messages
register_matplotlib_converters()

# Plot TSLA Stock Price and TSLA Web Search
plt.figure(figsize=(14, 8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('TSLA Stock Price', color='#E52020', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E52020', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()

# Plot BTC Price and BTC Web Search
plt.figure(figsize=(14, 8), dpi=120)
plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('BTC Price', color='orange', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE,
         color='orange', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH,
         color='skyblue', linewidth=3, marker='o')

plt.show()

# Plot FRED U/E Rate and Unemployment Benefits Web Search
# Cut-off: 2019
plt.figure(figsize=(14, 8), dpi=120)
plt.title(
    'Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate',
    fontsize=18
)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])

ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE,
         color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3)

plt.show()

# Plot FRED U/E Rate and Unemployment Benefits Web Search
# Cut-off: 2020
plt.figure(figsize=(14, 8), dpi=120)
plt.title(
    'Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate',
    fontsize=18
)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.set_xlim([df_unempl_2020.MONTH.min(), df_unempl_2020.MONTH.max()])

ax1.plot(df_unempl_2020.MONTH, df_unempl_2020.UNRATE,
         color='purple', linewidth=3, linestyle='--')
ax2.plot(df_unempl_2020.MONTH, df_unempl_2020.UE_BENEFITS_WEB_SEARCH,
         color='skyblue', linewidth=3)

plt.show()
