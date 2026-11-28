from collections.abc import Iterable

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from models.models import Product
from pages.cart_page import CartPage
from pages.main_page import MainPage


class CartSteps:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def add_products(self, products: Iterable[Product]) -> MainPage:
        products = list(products)
        names = ", ".join(product.name for product in products)
        with allure.step(f"Добавить в корзину товары: {names}"):
            main_page = MainPage(self.driver).open()
            for product in products:
                main_page.add_item_to_cart(product.name)
            return main_page

    def open_cart_with(self, products: Iterable[Product]) -> CartPage:
        with allure.step("Открыть корзину с выбранными товарами"):
            return self.add_products(products).open_cart()
