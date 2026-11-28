from typing import TYPE_CHECKING, Self

import allure
from selenium.webdriver.common.by import By

from models.models import Product, parse_price
from pages.base_page import BasePage

if TYPE_CHECKING:
    from pages.cart_page import CartPage
    from pages.login_page import LoginPage


class AuthorizedPage(BasePage):
    _CART_LINK = ("css selector", "[data-test='shopping-cart-link']")
    _CART_BADGE = ("css selector", "[data-test='shopping-cart-badge']")
    _TITLE = ("css selector", "[data-test='title']")

    _MENU_BUTTON = ("id", "react-burger-menu-btn")
    _MENU_OPENED = ("css selector", ".bm-menu-wrap[aria-hidden='false']")
    _LOGOUT_LINK = ("id", "logout_sidebar_link")

    _ITEM_CARD = (By.XPATH, "//div[@data-test='inventory-item']")
    _ITEM_NAME = (By.XPATH, ".//div[@data-test='inventory-item-name']")
    _ITEM_DESC = (By.XPATH, ".//div[@data-test='inventory-item-desc']")
    _ITEM_PRICE = (By.XPATH, ".//div[@data-test='inventory-item-price']")

    @staticmethod
    def _title_marker(title: str) -> tuple[str, str]:
        return (By.XPATH, f"//span[@data-test='title' and text()='{title}']")

    @staticmethod
    def _item_card_locator(item_name: str) -> tuple[str, str]:
        return (By.XPATH,
                f"//div[@data-test='inventory-item']"
                f"[.//div[@data-test='inventory-item-name' "
                f"and text()='{item_name}']]")

    @allure.step("Получить заголовок страницы")
    def get_title(self) -> str:
        return self.get_text(self._TITLE)

    @allure.step("Получить счетчик товаров на иконке корзины")
    def get_cart_badge_count(self) -> int:
        if not self.is_element_visible(self._CART_BADGE):
            return 0
        return int(self.get_text(self._CART_BADGE))

    @allure.step("Нажать на иконку корзины")
    def open_cart(self) -> "CartPage":
        from pages.cart_page import CartPage

        self.click(self._CART_LINK)
        return CartPage(self.driver).wait_until_loaded()

    @allure.step("Открыть боковое меню")
    def open_menu(self) -> Self:
        self.click(self._MENU_BUTTON)
        self.find_element(self._MENU_OPENED)
        return self

    @allure.step("Выйти из системы")
    def logout(self) -> "LoginPage":
        from pages.login_page import LoginPage

        self.open_menu()
        self.click(self._LOGOUT_LINK)
        return LoginPage(self.driver).wait_until_loaded()

    def _read_products(self) -> list[Product]:
        products = []
        for card in self.driver.find_elements(*self._ITEM_CARD):
            products.append(Product(
                name=card.find_element(*self._ITEM_NAME).text,
                description=card.find_element(*self._ITEM_DESC).text,
                price=parse_price(card.find_element(*self._ITEM_PRICE).text),
            ))
        return products
