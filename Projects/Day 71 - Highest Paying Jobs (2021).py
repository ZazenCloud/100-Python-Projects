from bs4 import BeautifulSoup
import requests
import pandas as pd

full_list = []

# From the article "Highest Paying Jobs With a Bachelor’s Degree" (2021)
# By Payscale.com

# Loop through pages 1 to 34 to scrape data
for i in range(1, 35):
    response = requests.get(
        f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{i}"
    )
    payscale_webpage = response.text

    soup = BeautifulSoup(payscale_webpage, "html.parser")

    spans = soup.select("tr td span")

    # Extract the text from the spans and clean it
    data_list = [
        text.getText().replace("%", "").replace(",", "")
        .replace("$", "").replace("-", "0")
        for text in spans
    ]
    # Select every other element in the data_list to get the relevant data
    clean_list = data_list[1::2]

    # Add the cleaned data to the full_list
    full_list.extend(clean_list)

# Split the full_list into chunks of six elements each
chunked_list = [full_list[i:i+6] for i in range(0, len(full_list), 6)]

# Remove the unwanted elements (Rank, Degree Type)
for group in chunked_list:
    del group[2]
    del group[0]

# Column names for the DataFrame
columns = ["Major", "Early Career Pay", "Mid-Career Pay", "% High Meaning"]

df = pd.DataFrame(chunked_list, columns=columns)

# Convert columns to numeric (integer) data type
df['Early Career Pay'] = df['Early Career Pay'].astype(int)
df['Mid-Career Pay'] = df['Mid-Career Pay'].astype(int)
df['% High Meaning'] = df['% High Meaning'].astype(int)

print("Year of Research: 2021")
print(f"Number of Majors: {df.shape[0]}\n")

print("Top 20 Majors by Early Career Pay\n")
# Sort the DataFrame by 'Early Career Pay' column in descending order
best_20_early_career_pay = df.sort_values('Early Career Pay', ascending=False)
# Display the best 20 early career paying majors
print(best_20_early_career_pay[['Major', 'Early Career Pay']].head(20))

print("\n------------------------------------------------------------------\n")

print("Bottom 20 Majors by Early Career Pay\n")
# Sort the DataFrame by 'Early Career Pay' column in ascending order
worst_20_early_career_pay = df.sort_values('Early Career Pay')
# Display the worst 20 early career paying majors
print(worst_20_early_career_pay[['Major', 'Early Career Pay']].head(20))

print("\n------------------------------------------------------------------\n")

print("Top 20 Majors by Mid-Career Pay\n")
# Sort the DataFrame by 'Mid-Career Pay' column in descending order
best_20_mid_career_pay = df.sort_values('Mid-Career Pay', ascending=False)
# Display the best 20 mid-career paying majors
print(best_20_mid_career_pay[['Major', 'Mid-Career Pay']].head(20))

print("\n------------------------------------------------------------------\n")

print("Bottom 20 Majors by Mid-Career Pay\n")
# Sort the DataFrame by 'Mid-Career Pay' column in ascending order
worst_20_mid_career_pay = df.sort_values('Mid-Career Pay')
# Display the worst 20 mid-career paying majors
print(worst_20_mid_career_pay[['Major', 'Mid-Career Pay']].head(20))

print("\n------------------------------------------------------------------\n")

print("Top 20 Majors by % High Meaning\n")
# Sort the DataFrame by '% High Meaning' column in descending order
best_20_meaning = df.sort_values('% High Meaning', ascending=False)
# Display the best 20 high meaning majors
print(best_20_meaning[['Major', '% High Meaning']].head(20))

print("\n------------------------------------------------------------------\n")

print("Bottom 20 Majors by % High Meaning\n")
# Sort the DataFrame by '% High Meaning' column in ascending order
worst_20_meaning = df.sort_values('% High Meaning')
# Display the worst 20 high meaning majors
print(worst_20_meaning[['Major', '% High Meaning']].head(20))
