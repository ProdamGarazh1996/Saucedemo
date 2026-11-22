import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открытие URL-адреса: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Найти элемент используя локатор: {locator}")
    def find_element(self, locator: tuple):
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент "
                    f"с локатором {locator} за отведенное время"
        )

    @allure.step("Найти все элементы используя локатор: {locator}")
    def find_elements(self, locator: tuple):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти хоть один элемент "
                    f"с локатором {locator} за отведенное время"
        )

    def wait_until_document_loaded(self):
        WebDriverWait(self.driver, 60).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete")
