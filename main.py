from enum import Enum
from urllib.parse import quote # to replace spaces and special characters in the URL
import json # for cookies
import time
import os
# from dotenv import load_dotenv
from dotenv import main
import sys
# Add the parent directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))

from messenger import LinkedinMessenger
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import random
from auth import check_cookies_and_login

from selenium.webdriver.support.ui import WebDriverWait
os.system("cls")  # clear screen from previous sessions

main.load_dotenv()

scraper = LinkedinMessenger()
driver = scraper.driver

RECIPIENT = "Deeksha Daga"
MESSAGE = """
Hello John,
I am sending you this message through LinkedIn.
Best Regards.
"""    
def main():
    check_cookies_and_login(driver)
    time.sleep(3)
    # scraper.send_message(recipient=RECIPIENT, message=MESSAGE)
    # scraper.reply_to_unread_messages()
    scraper.click_to_unread()
    scraper.logout()


if __name__ == "__main__":
    main()
