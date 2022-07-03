# selenium config for chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType


class Selenium:
    def __init__(self):
        self.driver = None
        self.options = Options()


    def get_driver(self):
        self.driver = webdriver.Chrome("chromedriver", options=self.options)
        return self.driver



    def get_page(self, url):
        self.driver.get(url)
        return self.driver

    def get_page_with_proxy(self, url, proxy):
        self.driver.get(url)
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)
        self.driver.set_window_size(1920, 1080)
        self.driver.set_window_position(0, 0)
        self.driver.set_proxy(proxy)
        return self.driver


url_of_all_new_personal_home_in_tehran = 'https://divar.ir/s/tehran/real-estate?user_type=personal'

# open the url_of_all_new_personal_home_in_tehran
selenium = Selenium()
driver = selenium.get_driver()
driver = selenium.get_page(url_of_all_new_personal_home_in_tehran)

# get all elements with xpath
cards = driver.find_elements(
    By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "kt-post-card--has-action", " " ))]')

for card in cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, '.kt-post-card__title').text
    except:
        title = ''

    try:
        price = card.find_element(By.CSS_SELECTOR, '.kt-post-card__description').text
    except:
        price = ''

    try:
        address = card.find_element(By.CSS_SELECTOR, '.kt-post-card__bottom-description').text.split(' ')[-1]
    except:
        address = ''

    try:
        link = card.find_element(
            By.XPATH, '//*[@id="app"]/div[1]/main/div[2]/div/div/div[1]/div/a').get_attribute('href')
    except:
        link = ''

    print( link)

















# close the browser
driver.quit()