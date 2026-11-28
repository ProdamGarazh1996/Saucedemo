from typing import Self

import allure
from selenium.webdriver.common.by import By

from models.models import Product
from pages.authorized_page import AuthorizedPage
from pages.checkout_info_page import CheckoutInfoPage


class CartPage(AuthorizedPage):
    PATH = "/cart.html"
    _PAGE_MARKER = AuthorizedPage._title_marker("Your Cart")

    _CHECKOUT_BUTTON = ("id", "checkout")

    @allure.step("Получить список товаров в корзине")
    def get_items(self) -> list[Product]:
        return self._read_products()

    @allure.step("Удалить из корзины товар {item_name}")
    def remove_item(self, item_name: str) -> Self:
        card = self._item_card_locator(item_name)
        self.click((By.XPATH, f"{card[1]}//button[text()='Remove']"))
        self.wait_until_invisible(card)
        return self

    @allure.step("Нажать кнопку 'Checkout'")
    def checkout(self) -> CheckoutInfoPage:
        self.click(self._CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver).wait_until_loaded()
