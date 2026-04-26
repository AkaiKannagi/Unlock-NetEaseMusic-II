# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00125159799AECA991C73963FA670ED2D109350656D44AAB53AA3B17382DCE57DE6381548E4F64102E607F361E405F14AA8FCC15AD77E83976BA303A70BA087B8945789C82FF3DF7D1A1E784C6BAD4E7180504E4FC4A1804571EF777C6075BDA361BDF1501A0F6C3BB93D7E82B3E329F36D6E03D209860977B774257444850FEAEC0118B008F855D40626F4ADB551DB73D76462024568CEB3BC06CC5E03A0A0BA520BF19672CE67EE5D84AB9D4179BBFF10755A9D0442E03CD011EABDF8FC7E37696E25253EC2C9983D16E66D6B1F966C6B5F426A321E9B96F25BCD01F0E488230677573A52ADDB3670162713B78EF56CD8B3CF75011F5330206B161C41042494819B166E572F2706D1E9F28C08D922FE13E4E2D5E150F63B24F1977509B97B0D2F3802740C61243ACA7C6BCA6D83C8B12AEF867AEF88B27066733E5B904AB25F77DE8ABEBDECA86C2D5A3B04D5E71013F351E8119E7F45C97C95B2A6138518DFED121338D29ECF861E4B54C878DCAAB60D67E8B8B7E4ECF3B6C162F0E738D99337D8950390152270B409A1F062D84DA72"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
