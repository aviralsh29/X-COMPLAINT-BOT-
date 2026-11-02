
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


PROMISED_DOWN = 150
PROMISED_UP = 10

Y_EMAIL = os.getenv("Y_EMAIL")
Y_PASSWORD = os.getenv("Y_PASSWORD")

LOGIN_URL = "https://app.100daysofpython.dev/services/y/login"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.options)
        self.wait = WebDriverWait(self.driver, 5)

        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        """Get current internet download and upload speeds."""

        self.driver.get("https://www.speedtest.net/")
        time.sleep(3)

        go_button = self.driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button/h1'
        )
        go_button.click()

        time.sleep(60)

        self.down = self.driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/h3'
        ).text

        self.up = self.driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div/h3'
        ).text

        print("Download speed:", self.down)
        print("Upload speed:", self.up)

    def tweet_at_provider(self):
        """Log in and tweet a complaint about internet speed."""

        self.driver.get(LOGIN_URL)

        email_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/form/input[1]")
            )
        )
        email_button.send_keys(Y_EMAIL)

        password_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/form/input[2]")
            )
        )
        password_button.send_keys(Y_PASSWORD)

        login_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/form/button")
            )
        )
        login_button.click()

        post_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/nav/button")
            )
        )
        post_button.click()

        write = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/form/div[1]/div/div[2]")
            )
        )
        write.send_keys(
            f"Hey Internet Provider, why is my speed "
            f"{self.up} up / {self.down} down "
            f"when I pay for {PROMISED_UP} up / {PROMISED_DOWN} down?"
        )

        post = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/form/div[2]/button[2]")
            )
        )
        post.click()


bot = InternetSpeedTwitterBot()

try:
    bot.get_internet_speed()
    bot.tweet_at_provider()
finally:
    bot.driver.quit()
