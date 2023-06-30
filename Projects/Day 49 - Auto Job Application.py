from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

EMAIL = "YOUR LOGIN EMAIL"
PASSWORD = "YOUR LOGIN PASSWORD"
PHONE = "YOUR PHONE NUMBER"

# Set up the Chrome WebDriver and open the LinkedIn job search page
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=marketing%20intern&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0")

# Find and click the "Sign in" button
time.sleep(5)
sign_in_button = driver.find_element(By.LINK_TEXT, "Sign in")
sign_in_button.click()

# Fill in the email and password fields and press Enter to sign in
time.sleep(5)
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(EMAIL)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(PASSWORD)  
password_field.send_keys(Keys.ENTER)

# Find all the job applications on the page
time.sleep(5)
job_applications = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in job_applications:
    driver.execute_script("arguments[0].click();", listing)
    time.sleep(5)
    try:
        # Find and click the "Apply" button
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        driver.execute_script("arguments[0].click();", apply_button)

        # Fill in the phone number field if it is empty
        time.sleep(5)
        phone = driver.find_element(By.CLASS_NAME, "fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE)

        # Submit the application
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button")
        if submit_button.get_attribute("aria-label") == "Continue to next step":
            # Close applications with multiple steps
            close_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
            close_button.click()
            time.sleep(5)
            discard_button = driver.find_element(By.XPATH, '//button[@data-control-name="discard_application_confirm_btn"]')
            discard_button.click()
            continue
        else:
            submit_button.click()

        # Close the pop-up after application is completed
        time.sleep(5)
        close_button = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
        close_button.click()

    except NoSuchElementException:
        continue

driver.quit()
