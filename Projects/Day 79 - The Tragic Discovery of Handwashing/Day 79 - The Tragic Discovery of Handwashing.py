import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats
from pandas.plotting import register_matplotlib_converters

# Set the display format for floating-point numbers
pd.options.display.float_format = '{:,.2f}'.format

# Register converters for matplotlib to handle dates
register_matplotlib_converters()

# Read the CSV files into DataFrames
df_yearly = pd.read_csv('data/annual_deaths_by_clinic.csv')
# parse_dates converts the column into a DateTime object
df_monthly = pd.read_csv('data/monthly_deaths.csv', parse_dates=['date'])

# Explore the Data
print(df_yearly.shape)
print(df_monthly.shape)
print(df_yearly.columns)
print(df_monthly.columns)
print(df_yearly.year.min())
print(df_yearly.year.max())
print(df_monthly.date.min())
print(df_monthly.date.max())
print(df_yearly.isna().any())
print(df_yearly.duplicated().values.any())
print(df_monthly.isna().any())
print(df_monthly.duplicated().values.any())
print(df_monthly.describe())

# Percentage of women giving birth who died
# throughout the 1840s at the hospital
print(round((df_yearly.deaths.sum() / df_yearly.births.sum() * 100), 2))

# Create locators for ticks on the Time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

# Plot Chart: Total Number of Monthly Births and Deaths
plt.figure(figsize=(14, 8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)

# Use Locators
ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.grid(color='grey', linestyle='--')

ax1.plot(
    df_monthly.date,
    df_monthly.births,
    color='skyblue',
    linewidth=3
)
ax2.plot(
    df_monthly.date,
    df_monthly.deaths,
    color='crimson',
    linewidth=2,
    linestyle='--'
)
plt.show()

# Line Chart: Total Yearly Births by Clinic
births_years_line = px.line(
    df_yearly,
    x='year',
    y='births',
    color='clinic',
    title='Total Yearly Births by Clinic'
)
births_years_line.show()

# Line Chart: Total Yearly Deaths by Clinic
death_years_line = px.line(
    df_yearly,
    x='year',
    y='deaths',
    color='clinic',
    title='Total Yearly Deaths by Clinic'
)
death_years_line.show()

# Create a new row for percentage of deaths in the yearly DataFrame
df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births * 100

# Average maternal death rate for Clinic 1
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_clinic_1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100
print(f'{avg_clinic_1:.2f}')

# Average maternal death rate for Clinic 2
clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_clinic_2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
print(f'{avg_clinic_2:.2f}')

# Line Chart: Proportion of Yearly Deaths by Clinic
clinic_deaths_line = px.line(
    df_yearly,
    x='year',
    y='pct_deaths',
    color='clinic',
    title='Proportion of Yearly Deaths by Clinic'
)
clinic_deaths_line.show()

# Date when handwashing was made mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Create a new row for percentage of deaths in the monthly DataFrame
df_monthly['pct_deaths'] = df_monthly.deaths / df_monthly.births

# Subset for before handwashing was implemented
before_handwashing = df_monthly[df_monthly.date < handwashing_start]

# Subset for after handwashing was implemented
after_handwashing = df_monthly[df_monthly.date >= handwashing_start]

# Average death rate prior to handwashing
before_hw_rate = (
    before_handwashing.deaths.sum() / before_handwashing.births.sum() * 100
)
print(f'{before_hw_rate:.2f}')

# Average death rate after handwashing
after_hw_rate = (
    after_handwashing.deaths.sum() / after_handwashing.births.sum() * 100
)
print(f'{after_hw_rate:.2f}')

# DataFrame with 6 month rolling average
# death rate prior to mandatory handwashing
roll_df = before_handwashing.set_index('date')
roll_df = roll_df.rolling(window=6).mean()


# Line Chart: Percentage of Monthly Deaths over Time
plt.figure(figsize=(14, 8), dpi=200)
plt.title('Percentage of Monthly Deaths over Time', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

plt.ylabel('Percentage of Deaths', color='crimson', fontsize=18)

ax = plt.gca()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])

plt.grid(color='grey', linestyle='--')

ma_line, = plt.plot(
    roll_df.index,
    roll_df.pct_deaths,
    color='crimson',
    linewidth=3,
    linestyle='--',
    label='6m Moving Average'
)
bw_line, = plt.plot(
    before_handwashing.date,
    before_handwashing.pct_deaths,
    color='black',
    linewidth=1,
    linestyle='--',
    label='Before Handwashing'
)
aw_line, = plt.plot(
    after_handwashing.date,
    after_handwashing.pct_deaths,
    color='skyblue',
    linewidth=3,
    marker='o',
    label='After Handwashing'
)
plt.legend(
    handles=[ma_line, bw_line, aw_line],
    fontsize=18
)
plt.show()

# Average percentage of monthly deaths before handwashing
before_hw_mean = before_handwashing.pct_deaths.mean() * 100
# Average percentage of monthly deaths after handwashing
after_hw_mean = after_handwashing.pct_deaths.mean() * 100
# Difference in averages before and after handwashing
hw_mean_difference = before_hw_mean - after_hw_mean
print(f'{hw_mean_difference:.2f}')
# Improvement factor after handwashing
hw_improvement = before_hw_mean / after_hw_mean
print(f'{hw_improvement:.2f}')

# Add a column to the monthly DataFrame that shows if a
# particular date was before or after the start of handwashing
df_monthly['washing_hands'] = np.where(
    df_monthly.date < handwashing_start, 'No', 'Yes'
)

# Box Chart: How Have the Stats Changed with Handwashing?
box = px.box(
    df_monthly,
    x='washing_hands',
    y='pct_deaths',
    color='washing_hands',
    title='How Have the Stats Changed with Handwashing?'
)
box.update_layout(
    xaxis_title='Washing Hands?',
    yaxis_title='Percentage of Monthly Deaths'
)
box.show()

# Histogram Chart: Monthly Percentage of Deaths
hist = px.histogram(
    df_monthly,
    x='pct_deaths',
    color='washing_hands',
    nbins=30,
    opacity=0.6,
    barmode='overlay',
    histnorm='percent',
    marginal='box'
)
hist.update_layout(
    xaxis_title='Proportion of Monthly Deaths',
    yaxis_title='Count'
)
hist.show()


# Kernel Density Estimate (KDE) Chart:
# Est. Distribution of Monthly Death Rate Before and After Handwashing
plt.figure(dpi=200)
sns.kdeplot(before_handwashing.pct_deaths, shade=True)
sns.kdeplot(after_handwashing.pct_deaths, shade=True)
plt.title(
    'Est. Distribution of Monthly Death Rate Before and After Handwashing'
)
plt.xlim(0, 0.4)
plt.show()

# T-Test and P-Value
t_stat, p_value = stats.ttest_ind(
    a=before_handwashing.pct_deaths,
    b=after_handwashing.pct_deaths
)
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')
