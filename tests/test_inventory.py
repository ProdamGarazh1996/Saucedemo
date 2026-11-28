from operator import attrgetter

import allure
import pytest

from data.test_data import Products
from models.models import Product, SortOption
from pages.main_page import MainPage


@allure.epic("SauceDemo")
@allure.feature("Каталог товаров")
class TestInventory:

    @allure.story("Сортировка")
    @allure.title("Сортировка товаров: {option.label}")
    @allure.description("После выбора варианта сортировки товары "
                        "упорядочены по названию или цене")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("option, field, reverse", [
        (SortOption.NAME_ASC, "name", False),
        (SortOption.NAME_DESC, "name", True),
        (SortOption.PRICE_ASC, "price", False),
        (SortOption.PRICE_DESC, "price", True),
    ], ids=["name_asc", "name_desc", "price_asc", "price_desc"])
    def test_sort_products(self, main_page: MainPage, option: SortOption,
                           field: str, reverse: bool):
        products = main_page.sort_by(option).get_products()
        actual_values = [getattr(product, field) for product in products]

        assert main_page.get_active_sort_option() == option.label, \
            "На странице отображается другой вариант сортировки"
        assert len(products) == len(Products.ALL), \
            "После сортировки изменилось количество товаров"
        assert actual_values == sorted(actual_values, reverse=reverse), \
            f"Товары не отсортированы: {option.label}"

    @allure.story("Карточка товара")
    @allure.title("Карточка товара {product.name}")
    @allure.description("Карточка товара показывает те же данные, что и "
                        "каталог; из карточки можно добавить товар в "
                        "корзину и вернуться в каталог")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("product", [
        Products.BACKPACK,
        Products.FLEECE_JACKET,
        Products.RED_T_SHIRT,
    ], ids=attrgetter("name"))
    def test_product_details(self, main_page: MainPage, product: Product):
        product_page = main_page.open_product(product.name)

        assert product_page.get_product() == product, \
            "Данные в карточке товара не соответствуют ожидаемым"

        main_page = product_page.add_to_cart().back_to_products()

        assert main_page.get_cart_badge_count() == 1, \
            "Товар из карточки не добавился в корзину"
        assert main_page.get_item_button_text(product.name) == \
            MainPage.REMOVE_TEXT, \
            "В каталоге у добавленного товара нет кнопки 'Remove'"
