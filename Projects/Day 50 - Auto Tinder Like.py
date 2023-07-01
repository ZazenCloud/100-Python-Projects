from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import time

FB_EMAIL = "YOUR FACEBOOK LOGIN EMAIL"
FB_PASSWORD = "YOUR FACEBOOK PASSWORD"

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://tinder.com/app/recs")

# Click on the "Log in" button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, 'Log in'))
    )
login_button.click()

# Click on the "Continue with Facebook" button
FB_sign_in = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="q2069402257"]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button')
        )
    )
FB_sign_in.click()

# Switch to the Facebook login window
driver.switch_to.window(driver.window_handles[1])

# Enter Facebook credentials
email_input = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="email"]')
        )
    )
email_input.send_keys("YOUR EMAIL")
password_input = driver.find_element(By.XPATH, '//*[@id="pass"]')
password_input.send_keys("YOUR PASSWORD")
password_input.send_keys(Keys.ENTER)

# Switch back to the Tinder window
driver.switch_to.window(driver.window_handles[1])

time.sleep(5)

# Click on the location access button
location = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="q2069402257"]/main/div/div/div/div[3]/button[1]')
        )
    )
location.click()

time.sleep(5)

# Click on the "Not interested" button
not_interested = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="q2069402257"]/main/div/div/div/div[3]/button[2]')
        )
    )
not_interested.click()

time.sleep(5)

# Click on the "I Decline" button
i_decline = WebDriverWait(driver, 20).until(
EC.element_to_be_clickable((By.XPATH, '//*[@id="q-497183963"]/div/div[2]/div/div/div[1]/div[2]/button'))
)
i_decline.click()

time.sleep(5)

# Find the "Like" button
like_button = driver.find_element(
    By.XPATH, '//*[@id="q-497183963"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button')

# 100 likes
for i in range(100):
    time.sleep(5)
    try:
        like_button.click()

    except ElementClickInterceptedException:
        # Handle the case when a match popup appears
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsMatch a")
            match_popup.click()
        except NoSuchElementException:
            time.sleep(2)
            
driver.quit()