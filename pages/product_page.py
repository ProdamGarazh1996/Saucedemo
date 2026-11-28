from typing import Self

import allure

from models.models import Product
from pages.authorized_page import AuthorizedPage
from pages.main_page import MainPage


class ProductPage(AuthorizedPage):
    PATH = "/inventory-item.html"
    _PAGE_MARKER = ("id", "inventory_item_container")

    _ADD_TO_CART_BUTTON = ("css selector", "[data-test='add-to-cart']")
    _REMOVE_BUTTON = ("css selector", "[data-test='remove']")
    _BACK_TO_PRODUCTS_BUTTON = ("id", "back-to-products")

    @allure.step("Получить данные товара")
    def get_product(self) -> Product:
        self.find_element(self._ITEM_CARD)
        return self._read_products()[0]

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> Self:
        self.click(self._ADD_TO_CART_BUTTON)
        self.find_element(self._REMOVE_BUTTON)
        return self

    @allure.step("Вернуться к списку товаров")
    def back_to_products(self) -> MainPage:
        self.click(self._BACK_TO_PRODUCTS_BUTTON)
        return MainPage(self.driver).wait_until_loaded()
