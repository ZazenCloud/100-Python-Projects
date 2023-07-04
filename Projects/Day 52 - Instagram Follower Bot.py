from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time

INSTAGRAM_ACCOUNT = ""
INSTAGRAM_PASSWORD = ""
TARGET = ""  # Instagram account (to use the followers list)
CYCLES = 4  # Number of times to load more followers
# Keep in mind that Instagram may limit your account if "CYCLES" > 5


class InstaFollower():

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=15, poll_frequency=1)

    def login(self):
        # Open the Instagram login page
        self.driver.get("https://www.instagram.com/accounts/login/")
        # Find the username field and enter the Instagram account username
        username = self.wait.until(EC.element_to_be_clickable((By.NAME, "username")))
        username.click()
        username.send_keys(INSTAGRAM_ACCOUNT)
        # Find the password field and enter the Instagram account password
        password = self.driver.find_element(By.NAME, "password")
        password.click()
        password.send_keys(INSTAGRAM_PASSWORD)
        # Find the submit button and click it to log in
        submit = self.driver.find_element(By.CSS_SELECTOR, "button[type*='submit']")
        submit.click()
        try:
            # Check if the "Turn On Notifications" dialog is displayed, close it if found
            notifications_off = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "._a9--._a9_1")))
            notifications_off.click()
        except NoSuchElementException:
            pass
        time.sleep(1)

    def find_followers(self):
        # Open the target user's Instagram profile
        self.driver.get(f"https://www.instagram.com/{TARGET}/")
        time.sleep(2)
        # Find and click on the followers list
        followers_list = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"a[href*='/{TARGET}/followers/']")))
        followers_list.click()
        time.sleep(2)

    def follow(self):
        # Find the "Followers" window
        people_to_follow = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "._acan._acap._acas._aj1-")))
        followers_window = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe")))
        self.driver.execute_script("arguments[0].click();", followers_window)

        for _ in range(1, CYCLES):
            # Find the list of people to follow
            people_to_follow = self.driver.find_elements(By.CSS_SELECTOR, "._acan._acap._acas._aj1-")
            for people in people_to_follow:
                if people.text == "Follow":
                    # Click the "Follow" button to follow the person
                    self.driver.execute_script("arguments[0].click();", people)
                    time.sleep(0.5)
                    scroll_origin = ScrollOrigin.from_element(followers_window)
                # Scroll the followers window to view more people to follow
                ActionChains(self.driver)\
                    .scroll_from_origin(scroll_origin, 0, 35)\
                    .perform()
                time.sleep(0.2)


instabot = InstaFollower()

instabot.login()
instabot.find_followers()
instabot.follow()

instabot.driver(quit)
