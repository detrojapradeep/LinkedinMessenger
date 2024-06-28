import os
import time
import traceback
from fake_useragent import UserAgent
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class LinkedinMessenger:
    def __init__(self) -> None:
        self.driver = self._get_driver()

    def _get_driver(self):
        ua = UserAgent()
        random_agent = ua.random
        fixed_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"""

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_argument(f"user-agent={fixed_agent}")
        # options.add_argument(f"user-agent={random_agent}")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.implicitly_wait(4)
        driver.maximize_window()
        return driver

    def login(self, email: str, password: str):
        if not self.driver:
            return

        link = "https://www.linkedin.com/login"
        try:
            # self.driver.get(link)
            self.driver.implicitly_wait(2)

            email_box = self.driver.find_element(By.XPATH, "//input[@id='username']")
            password_box = self.driver.find_element(By.XPATH, "//input[@id='password']")

            email_box.send_keys(email)
            time.sleep(1)
            password_box.send_keys(password)
            time.sleep(1)

            sign_in = self.driver.find_element(
                By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'
            )
            sign_in.click()
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())

    def send_message(self, recipient: str, message: str):
        if not self.driver:
            return

        link = "https://www.linkedin.com/messaging/thread/new/"
        try:
            self.driver.get(link)
            self.driver.implicitly_wait(6)

            time.sleep(3)

            search_name = self.driver.find_element(
                By.XPATH,
                '//input[contains(@class, "msg-connections-typeahead__search-field")]',
            )
            for name_part in recipient.split():
                search_name.send_keys(f"{name_part} ")
                time.sleep(1)
            time.sleep(2)

            search_name.send_keys(Keys.RETURN)
            message_box = self.driver.find_element(
                By.XPATH,
                '//form[contains(@class, "msg-form")]/div[3]/div/div[1]/div[1]/p',
            )
            message_box.send_keys(message)
            time.sleep(3)

            send_button = self.driver.find_element(
                By.XPATH,
                '//form[contains(@class, "msg-form")]/footer/div[2]/div[1]/button',
            )
            send_button.click()

            time.sleep(8)

        except Exception as e:
            print(traceback.format_exc())



    def check_and_create_excel_file(self, filename="REPLIES.csv"):
        if not os.path.exists(filename):
            df = pd.DataFrame(columns=["Person Name", "Quick Reply"])
            df.to_excel(filename, index=False)
            print(f"Created new file: {filename}")
        else:
            print(f"File {filename} already exists.")

    def update_excel_file(self, person_name, reply_text, filename="REPLIES.xlsx"):
        df = pd.read_excel(filename)
        new_entry = {"Person Name": person_name, "Quick Reply": reply_text}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_excel(filename, index=False)

    # $('.msg-conversation-card.msg-conversations-container__pillar a').click()
    def click_to_unread(self):
        if not self.driver:
            return
        self.check_and_create_excel_file()

        link = "https://www.linkedin.com/messaging/"
        self.driver.get(link)
        self.driver.implicitly_wait(5)

        try:
            button_unread = self.driver.find_element(By.XPATH, '//button[text()="Unread"]')
            button_unread.click()
        
        except (NoSuchElementException, TimeoutException):
            print("Unread button not found.")
            return

        while True:
            try:
                self.driver.implicitly_wait(10)
                
                # Wait for the conversations list to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'msg-conversations-container__conversations-list'))
                )

                # Locate the first unread message
                first_unread_message = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-conversation-card__convo-item-container--unread a'))
                )

                # Fetch the person's name
                person = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-conversation-card__convo-item-container--unread a .msg-conversation-card__participant-names'))
                )
                person_name = person.get_attribute('innerText')

                # Click the first unread message
                first_unread_message.click()
                # time.sleep(5)
                reply_text = "N/A"

                try:
                    # Locate the first quick reply button
                    first_quickreply_button = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-s-message-list__quick-replies-container button'))
                    )

                    # Fetch the reply to be sent
                    reply = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-s-message-list__quick-replies-container button .conversations-quick-replies__reply-content'))
                    )
                    reply_text = reply.get_attribute('innerText')

                    # Send the quick reply
                    first_quickreply_button.click()
                    time.sleep(5)

                except (NoSuchElementException, TimeoutException):
                    reply_text = "N/A"
                    print("No Quick Reply options found.")
                
                # Update the excel file with Person, Reply
                self.update_excel_file(person_name, reply_text)

            except (NoSuchElementException, TimeoutException):
                print("No more unread messages found or timeout occurred.")
                break

    def logout(self):
        if not self.driver:
            return

        link = "https://www.linkedin.com/m/logout"
        try:
            self.driver.get(link)
            self.driver.implicitly_wait(4)
            time.sleep(4)
        except Exception as e:
            print(traceback.format_exc())
