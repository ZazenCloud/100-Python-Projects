from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

# Create a new form at https://docs.google.com/forms/
# Create 3 questions (select "short answer" as the type)
# Q1 -> What's the address of the property?
# Q2 -> What's the price per month?
# Q3 -> What's the link to the property?
# Click "Send", then copy the link generated
# Paste the link as a string value to the FORM variable

FORM = "..."
CITY = "san-francisco-ca"
LINK = f"https://www.zillow.com/{CITY}/rentals/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.86451840366255%2C%22east%22%3A-122.28003589038086%2C%22south%22%3A37.61664273113711%2C%22west%22%3A-122.72566882495117%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

addresses_list = []
prices_list = []
url_list = []

response = requests.get(LINK, headers=header).content

soup = BeautifulSoup(response, 'html.parser')

# Zillow uses lazy loading to display the cards
# So, if we parse the raw HTML, we only get 9 cards
# But we can target a script element
# That holds the info of all the cards in that page (41 cards)
data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
    .contents[0]
    .strip("!<>-")
)

all_data = data['cat1']['searchResults']['listResults']

# Iterate over the data and populate the lists
for i in range(len(all_data)):
    try:
        # There are 2 different price display structures
        # This try/except block covers both
        prices_list.append(all_data[i]['units'][0]['price'])
    except KeyError:
        prices_list.append(all_data[i]['price'])

    address = addresses_list.append(all_data[i]['address'])

    link = all_data[i]['detailUrl']
    if 'http' not in link:
        # Some links don't have the "www.zillow.com" at the beginning
        # In this case, we add them
        url_list.append(f"https://www.zillow.com{link}")
    else:
        url_list.append(link)

driver = webdriver.Chrome()
wait = WebDriverWait(driver, timeout=15, poll_frequency=1)

# Open the Google Form page
driver.get(FORM)

# Iterate over the lists and fill in the form inputs
for address, price, url in zip(addresses_list, prices_list, url_list):
    i = 0
    temp_tuple = (address, price, url)
    # Wait for the "Submit" button to be visible
    submit = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".NPEfkd.RveJvd.snByac")
        )
    )
    inputs = driver.find_elements(By.CSS_SELECTOR, "input[type*='text']")
    for input in inputs:
        driver.execute_script("arguments[0].click();", input)
        time.sleep(0.1)
        input.send_keys(temp_tuple[i])
        i += 1
    submit.click()
    # Proceed to the next iteration
    another = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "a")))
    another.click()
