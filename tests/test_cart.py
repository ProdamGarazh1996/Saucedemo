from operator import attrgetter

import allure
import pytest

from data.test_data import Products
from models.models import Product
from pages.main_page import MainPage
from steps.cart_steps import CartSteps


@allure.epic("SauceDemo")
@allure.feature("Корзина")
class TestCart:

    @allure.story("Добавление товара")
    @allure.title("Добавление в корзину товара {product.name}")
    @allure.description("Добавленный из каталога товар появляется в корзине "
                        "с теми же названием, описанием и ценой")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.parametrize("product", [
        Products.BACKPACK,
        Products.BIKE_LIGHT,
        Products.ONESIE,
    ], ids=attrgetter("name"))
    def test_add_product_to_cart(self, main_page: MainPage, product: Product):
        main_page = main_page.add_item_to_cart(product.name)

        assert main_page.get_cart_badge_count() == 1, \
            "Счетчик корзины не равен 1"

        cart_page = main_page.open_cart()

        assert cart_page.get_items() == [product], \
            "Товар в корзине не соответствует добавленному"

    @allure.story("Удаление товара")
    @allure.title("Удаление товара на странице корзины")
    @allure.description("Удалённый товар пропадает из корзины, остальные "
                        "товары остаются, счетчик уменьшается")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_remove_product_in_cart(self, main_page: MainPage,
                                    cart_steps: CartSteps):
        cart_page = (cart_steps
                     .open_cart_with([Products.BACKPACK, Products.BIKE_LIGHT])
                     .remove_item(Products.BACKPACK.name))

        assert cart_page.get_items() == [Products.BIKE_LIGHT], \
            "После удаления в корзине неверный набор товаров"
        assert cart_page.get_cart_badge_count() == 1, \
            "Счетчик корзины не уменьшился после удаления товара"
