import csv
import pandas as pd
import matplotlib.pyplot as plt

# Clean the "sets.csv" dataset by deleting the last column (img_url)
with open(
    'data/sets.csv',
    'r',
    encoding='utf-8'
) as input_file:
    reader = csv.reader(input_file)
    modified_rows = []
    for row in reader:
        row = row[:-1]
        modified_rows.append(row)
with open(
    'data/sets_fixed.csv',
    'w',
    encoding='utf-8',
    newline=''
) as output_file:
    writer = csv.writer(output_file)
    writer.writerows(modified_rows)

# LEGO database
# Source: https://rebrickable.com/downloads/
colors = pd.read_csv('data/colors.csv')
sets = pd.read_csv('data/sets_fixed.csv')
themes = pd.read_csv('data/themes.csv')

# Number of unique colors
nr_colors = colors['name'].nunique()
# print(nr_colors)

# Number of transparent and non-transparent colors
trans_colors = colors.is_trans.value_counts()
# print(trans_colors)

# Group number of sets by year
sets_by_year = sets.groupby('year').count()

# Create a line graph of sets by year
# Exclude last year for data uniformity (full years)
plt.plot(sets_by_year.index[:-1], sets_by_year.set_num[:-1])
plt.show()

# Group the sets by year and count the unique theme_ids for each year
themes_by_year = sets.groupby('year').agg({'theme_id': pd.Series.nunique})
# Rename the column 'theme_id' to 'nr_themes'
themes_by_year.rename(columns={'theme_id': 'nr_themes'}, inplace=True)

# Create a plot with two y-axes
ax1 = plt.gca()
ax2 = ax1.twinx()
# Plot the number of sets per year on the first y-axis
ax1.plot(sets_by_year.index[:-1], sets_by_year.set_num[:-1], 'g')
# Plot the number of themes per year on the second y-axis
ax2.plot(themes_by_year.index[:-1], themes_by_year.nr_themes[:-1], 'b')
# Labels
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Sets', color='green')
ax2.set_ylabel('Number of Themes', color='blue')
plt.show()


# Group the sets by year and calculate the
# mean number of parts per set for each year
parts_per_set = sets.groupby('year').agg({'num_parts': pd.Series.mean})
# Create a scatter plot
# Exclude last year for data uniformity (full years)
plt.scatter(parts_per_set.index[:-1], parts_per_set.num_parts[:-1])
plt.show()

# Count the number of sets for each theme
set_theme_count = sets['theme_id'].value_counts()

# Convert the Series to a DataFrame
set_theme_count = pd.DataFrame(
    {
        'id': set_theme_count.index,
        'set_count': set_theme_count.values
    }
)

# Merge the set_theme_count DataFrame with
# the themes DataFrame on the 'id' column
merged_df = pd.merge(set_theme_count, themes, on='id')

# Create a bar plot of the number of sets for the top 10 themes
plt.figure(figsize=(14, 8))
plt.xticks(fontsize=14, rotation=75)
plt.yticks(fontsize=14)
plt.ylabel('Nr of Sets', fontsize=14)
plt.xlabel('Theme Name', fontsize=14)
plt.bar(merged_df.name[:10], merged_df.set_count[:10])
plt.show()
