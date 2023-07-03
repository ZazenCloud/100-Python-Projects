from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TWITTER_ACCOUNT = "YOUR TWITTER ACCOUNT/EMAIL"
TWITTER_PASSWORD = "YOUR TWITTER PASSWORD"
PROMISED_DOWNLOAD = 0  # Your contracted download speed
PROMISED_UPLOAD = 0  # Your contracted upload speed
COMPANY_ACCOUNT = "YOUR INTERNET PROVIDER TWITTER ACCOUNT"


class InternetSpeedTwitterBot():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.down = 0
        self.up = 0
        self.wait = WebDriverWait(self.driver, timeout=15, poll_frequency=1)

    def get_internet_speed(self):
        """Open 'speedtest.net' and measure your internet speed."""
        self.driver.get("https://www.speedtest.net/")
        time.sleep(1)
        accept_cookies = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-close-btn-container .banner-close-button")))
        accept_cookies.click()
        start_test = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "js-start-test")))
        start_test.click()
        # Wait for test to finish
        time.sleep(60)
        self.down = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".download-speed"))).text
        self.up = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "upload-speed"))).text

    def tweet_text_at_provider(self):
        """Log in Twitter and send a complain tweet to your internet provider."""
        self.driver.get("https://twitter.com/")
        login = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input")))
        login.click()
        login.send_keys(TWITTER_ACCOUNT)
        login.send_keys(Keys.ENTER)
        password = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete*='current-password']")))
        password.send_keys(TWITTER_PASSWORD)
        password.send_keys(Keys.ENTER)
        tweet_text = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".public-DraftStyleDefault-block")))
        tweet_text.send_keys(f"Hey, @{COMPANY_ACCOUNT}!\n" +
                             f"My internet speed is {self.down}/{self.up} (DL/UP) right now.\n" +
                             f"Can you please explain me why?\n" +
                             f"I pay for {PROMISED_DOWNLOAD}/{PROMISED_UPLOAD}!")
        tweet_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid*='tweetButtonInline']")))
        tweet_button.click()


bot = InternetSpeedTwitterBot()

# Get the current internet speed
bot.get_internet_speed()
# Check if the internet speed is below the promised speed
if float(bot.down) < 200 or float(bot.up) < 200:
    # Tweet a complaint to the provider
    bot.tweet_text_at_provider()
