import pandas as pd
import matplotlib.pyplot as plt
# Download QueryResults.csv (located on this repository)
# and move it to same folder of this file
# Source: https://data.stackexchange.com/stackoverflow/query/675441/popular-programming-languages-per-over-time-eversql-com

# Read data from CSV file and create a DataFrame
df = pd.read_csv("query_results.csv", names=['DATE', 'TAG', 'POSTS'], header=0)

# Convert the 'DATE' column to datetime format
df['DATE'] = pd.to_datetime(df['DATE'])

# Pivot the 'TAG' column to become column headers (programming languages)
reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')

# Fill NaN (missing values) with 0
reshaped_df.fillna(0, inplace=True)

# Check if there are any NaN values in the reshaped DataFrame
# reshaped_df.isna().values.any()

# Drop columns for specific programming languages
new_df = reshaped_df.drop(['assembly', 'delphi', 'perl', 'go', 'ruby'], axis=1)

# Calculate the rolling mean over a window of 3 periods for each tag
roll_df = new_df.rolling(window=3).mean()

# Plotting the data
plt.figure(figsize=(16, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=16)
plt.ylabel('Number of Posts', fontsize=16)
plt.ylim(0, 30000)

for column in roll_df.columns:
    plt.plot(
        roll_df.index,  # Dates
        roll_df[column],  # Programming Language
        linewidth=3,
        label=roll_df[column].name
    )

# Add a legend to the plot
plt.legend(fontsize=16)
# Show the plot
plt.show()
