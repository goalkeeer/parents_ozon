import time

from selenium.webdriver.chrome.options import Options
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class BrowserException(Exception):
    pass


class BrowserTradeLock:

    URL = 'https://www.tlock.ru'

    def __init__(self):
        service = Service(ChromeDriverManager().install())
        WINDOW_SIZE = "1920,600"
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=%s" % WINDOW_SIZE)
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.URL)
        self.driver.implicitly_wait(0.1)

    def get_login_button(self):
        return self.driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[1]/header/div/div[1]/div/div[1]/div/div[2]/div/div[1]/button')

    def get_search_input(self):
        return self.driver.find_element(by=By.ID, value='title-search-input')

    def check_authenticated(self):
        try:
            self.get_login_button()
            return False
        except NoSuchElementException:
            return True

    def make_search(self, text):
        search_input = self.get_search_input()
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.RETURN)

    def login(self, user, password):
        button = self.get_login_button()
        button.click()
        self.driver.implicitly_wait(5)
        user_input = self.driver.find_element(by=By.ID, value='em0')
        user_input.send_keys(user)
        user_input = self.driver.find_element(by=By.NAME, value='USER_PASSWORD')
        user_input.send_keys(password)
        auth_button = self.driver.find_element(by=By.ID, value='login_popup_sub')
        auth_button.click()
        time.sleep(1)

    def choose_item(self):
        fgrids = self.driver.find_elements(by=By.XPATH, value='//*[@id="view_1"]/div[2]/div')
        try:
            fgrid_first = fgrids[0]
        except IndexError:
            raise BrowserException('не найдено')

        items = fgrid_first.find_elements(by=By.CSS_SELECTOR, value='div.fgrid__item-i')
        if len(items) > 1:
            raise BrowserException('элементов больше 1')

        item = items[0]
        item_link = item.find_element(by=By.CSS_SELECTOR, value='a.prod__link')
        item_link.click()

    def get_count(self) -> str:
        count_input = self.driver.find_element(by=By.XPATH, value='//*[@id="big-price-info"]/tbody/tr/td[3]/div[1]/div[2]/form/div[1]/div/input')
        count_input.send_keys(1000000)
        count_div = self.driver.find_element(by=By.XPATH, value='//*[@id="big-price-info"]/tbody/tr/td[3]/div[1]/div[2]/form/div[2]/div[1]/div[2]/div[1]')
        return count_div.text

    def get_price(self) -> str:
        div_price = self.driver.find_element(by=By.XPATH, value='//*[@id="big-price-info"]/tbody/tr/td[3]/div[1]/div[1]/div[1]/div')
        price = div_price.text.split(' – ')[1].replace(' ', '').replace(',', '.')
        return price

    def quit(self):
        self.driver.quit()
