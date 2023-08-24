from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Set Chrome options to mute audio
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Open Cookie Clicker
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Set up a WebDriverWait instance with a timeout of 10 seconds
# and a polling frequency of 0.5 seconds
wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5)

# Wait for the "Got it!" element to be
# clickable and then click it to accept cookies
accept_cookies = wait.until(
    EC.element_to_be_clickable((By.LINK_TEXT, "Got it!"))
)
accept_cookies.click()

# Find the "English" language option element and click on it
language = driver.find_element(By.XPATH, '//*[@id="langSelect-EN"]')
language.click()

# Wait for the save pop-up element to be visible
# and then click on it to close the pop-up
close_popup = wait.until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".note.haspic .close"))
)
close_popup.click()

# Find the big cookie element
big_cookie = driver.find_element(By.ID, "bigCookie")

# Initialize variables
random_time = 5
start_time = time.time()


def get_buildings_info():
    '''Finds all elements of buildings available to purchase
    and returns 2 lists (IDs and prices).'''
    id_list = []
    price_list = []

    # Find all the unlocked building elements
    buildings = driver.find_elements(
        By.CSS_SELECTOR, ".product.unlocked.enabled"
    )

    for building in buildings:
        # Locate the <div> with the price and ID info
        building_element = building.find_element(
            By.CSS_SELECTOR, ".content .price"
        )
        # Get the building ID attribute
        building_id = building_element.get_attribute("id")
        # Append the building ID to the id_list
        id_list.append(building_id)
        # Get the building price text and convert it to an integer
        building_price = int(building_element.text.replace(",", ""))
        # Append the building price to the price_list
        price_list.append(building_price)

    return id_list, price_list


while True:
    # Track time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Click on the big cookie
    big_cookie.click()

    if elapsed_time >= random_time:
        # Click on available upgrades
        upgrades = driver.find_elements(
            By.CSS_SELECTOR, ".crate.upgrade.enabled"
        )
        for upgrade in upgrades:
            # to avoid a stale element
            upgrade_id = upgrade.get_attribute("id")
            upgrade_to_click = driver.find_element(By.ID, upgrade_id)
            upgrade_to_click.click()

        # Get current cookies amount
        cookies_info = driver.find_element(By.ID, "cookies").text
        cookies_amount = int(cookies_info.split(" ")[0].replace(",", ""))

        # Close achievements pop-ups
        driver.execute_script("Game.CloseNotes()")

        # Get building information
        id_list, price_list = get_buildings_info()

        # Purchase affordable buildings
        while price_list and cookies_amount > min(price_list):
            last_item = price_list[-1]
            last_id = id_list[-1]
            if last_item > cookies_amount:
                # If not affordable, remove building from lists
                del last_item
                del last_id
            else:
                # Click on the building to purchase
                buy = driver.find_element(By.ID, last_id)
                # JavaScript clicking method avoid interception errors
                driver.execute_script("arguments[0].click();", buy)
                # Update prices after purchase
                id_list, price_list = get_buildings_info()

        # Generate a new random time interval
        random_time = random.randint(5, 10)

        # Update the start time for the next loop
        start_time = time.time()

    else:
        continue
