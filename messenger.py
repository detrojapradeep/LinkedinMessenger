import time
import traceback

from fake_useragent import UserAgent

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
            self.driver.implicitly_wait(6)

            time.sleep(1)

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

    def click_to_unread(self):
        if not self.driver:
            return
        
        link = "https://www.linkedin.com/messaging/"
        self.driver.get(link)
        self.driver.implicitly_wait(5)

        button_unread = self.driver.find_element(By.XPATH, '//button[text()="Unread"]')
        button_unread.click()
        first_message_processed = 1     
        # $('.msg-conversation-card.msg-conversations-container__pillar a').click()
   
        while True:
            try:
                # Refresh the page
                self.driver.implicitly_wait(10)

                # # Only for the first message so it doesn't get skipped
                # if(first_message_processed):
                #     first_message_processed = 0
                #     # Fetch the details of the person
                #     person = WebDriverWait(self.driver, 10).until(
                #         EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-conversation-card.msg-conversations-container__pillar a .msg-conversation-card__participant-names'))
                #     )
                #     person_name = person.get_attribute('innerText')
                #     print("THE PERSON NAME IS : " + person_name + '!!!!!!!')

                #     first_message = WebDriverWait(self.driver, 10).until(
                #         EC.presence_of_element_located((By.CLASS_NAME, '.msg-conversation-card.msg-conversations-container__pillar a'))
                #     )

                #     first_message.click()
                #     try:
                #         # Locate the first quick reply button
                #         first_quickreply_button = WebDriverWait(self.driver, 3).until(
                #             EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-s-message-list__quick-replies-container button'))
                #         )
                #         # Fetch the reply to be sent
                #         reply = WebDriverWait(self.driver, 3).until(
                #             EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-s-message-list__quick-replies-container button .conversations-quick-replies__reply-content'))
                #         )
                #         reply_text = reply.get_attribute('innerText')
                #         print("Reply Given IS : " + reply_text + '!!!!!\n')
                #         # Send the quick reply
                #         first_quickreply_button.click()
                #     except Exception as e:
                #         print(f"No Quick Reply options found: ")
                #         continue
                   

                # Wait until the messaging page is loaded
                # UL containing all the unread messages
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'msg-conversations-container__conversations-list'))
                )
                
                # Locate the first unread message by its class name
                first_unread_message = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-conversation-card__convo-item-container--unread a'))
                )

                # Fetch the details of the person
                person = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.msg-conversation-card__convo-item-container--unread a .msg-conversation-card__participant-names'))
                )
                person_name = person.get_attribute('innerText')
                print("THE PERSON NAME IS : " + person_name + '!!!!!!!')

                # Click the first unread message
                first_unread_message.click()
                time.sleep(5)


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
                    print("Reply Given IS : " + reply_text + '!!!!!\n')

                    # Send the quick reply
                    first_quickreply_button.click()
                    
                except Exception as e:
                    print(f"No Quick Reply options found: ")
                    continue

            # Working! Name from the UL of unread messages- the first unread message person name
            # $('.msg-conversation-card__convo-item-container--unread a .msg-conversation-card__participant-names').innerText

            # Working, content of the first quick reply!
            # $('.msg-s-message-list__quick-replies-container button .conversations-quick-replies__reply-content').innerText

            except (NoSuchElementException, TimeoutException) as e:
                print(f"No more unread messages found or timeout occurred:")
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
