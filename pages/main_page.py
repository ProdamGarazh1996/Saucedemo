import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    _SHOPPING_CART_LINK = (By.XPATH, "//a[@data-test='shopping-cart-link']")

    @allure.step("Добавить в корзину товар {item_name}")
    def add_item_to_cart(self, item_name: str):
        locator = (f"//div[contains(text(), '{item_name}')]"
                   f"/ancestor::div[@data-test='inventory-item-description']"
                   f"//button[text()='Add to cart']")
        self.find_element((By.XPATH, locator)).click()

    @allure.step("Нажать на иконку корзины")
    def click_on_shopping_cart_link(self):
        self.find_element(self._SHOPPING_CART_LINK).click()
