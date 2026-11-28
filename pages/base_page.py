from typing import Self
from urllib.parse import urlparse

import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class BasePage:
    PATH: str = "/"
    _PAGE_MARKER: tuple[str, str]

    def __init__(self, driver: WebDriver, timeout: int = settings.timeout):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @property
    def url(self) -> str:
        return f"{settings.base_url}{self.PATH}"

    def load(self) -> None:
        with allure.step(f"Перейти по адресу: {self.url}"):
            self.driver.get(self.url)

    def is_loaded(self) -> bool:
        current_path = urlparse(self.driver.current_url).path
        expected_path = urlparse(self.url).path
        return (current_path == expected_path
                and self.is_element_visible(self._PAGE_MARKER))

    def wait_until_loaded(self) -> Self:
        with allure.step(f"Дождаться загрузки страницы "
                         f"{type(self).__name__}"):
            self.wait.until(
                lambda _: self.is_loaded(),
                message=f"Страница {type(self).__name__} ({self.PATH}) "
                        f"не загрузилась за отведенное время. "
                        f"Текущий URL: {self.driver.current_url}"
            )
        return self

    def open(self) -> Self:
        with allure.step(f"Открыть страницу {type(self).__name__}"):
            if not self.is_loaded():
                self.load()
            return self.wait_until_loaded()

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

    def click(self, locator: tuple) -> None:
        self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент с локатором {locator} не стал кликабельным "
                    f"за отведенное время"
        ).click()

    def type_text(self, locator: tuple, text: str) -> None:
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент с локатором {locator} не отобразился "
                    f"за отведенное время"
        ).text

    def is_element_visible(self, locator: tuple) -> bool:
        try:
            return any(element.is_displayed()
                       for element in self.driver.find_elements(*locator))
        except StaleElementReferenceException:
            return False

    def wait_until_invisible(self, locator: tuple) -> None:
        self.wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент с локатором {locator} не исчез "
                    f"за отведенное время"
        )

    def wait_until_document_loaded(self):
        WebDriverWait(self.driver, 60).until(
            lambda d: d.execute_script(
                "return document.readyState") == "complete")
