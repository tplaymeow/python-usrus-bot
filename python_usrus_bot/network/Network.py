from urllib.parse import urlencode
import requests
from selenium import webdriver
from python_usrus_bot.network.HTMLQueryBuilder import HTMLQueryBuilder


class NetworkManager:
    @staticmethod
    def build_url(base_url, path, params=None):
        return base_url + path + "?" + urlencode(params)

    @staticmethod
    async def get_html(url) -> HTMLQueryBuilder:
        driver = webdriver.Chrome()
        try:
            # Send a GET request using the requests library
            driver.get(url)
            return HTMLQueryBuilder(driver)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
