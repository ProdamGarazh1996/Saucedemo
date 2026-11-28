from typing import TYPE_CHECKING, Self

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from models.models import Product, SortOption
from pages.authorized_page import AuthorizedPage

if TYPE_CHECKING:
    from pages.product_page import ProductPage


class MainPage(AuthorizedPage):
    PATH = "/inventory.html"
    _PAGE_MARKER = AuthorizedPage._title_marker("Products")

    _SORT_SELECT = ("css selector", "[data-test='product-sort-container']")
    _ACTIVE_SORT_OPTION = ("css selector", "[data-test='active-option']")

    ADD_TO_CART_TEXT = "Add to cart"
    REMOVE_TEXT = "Remove"

    def _item_button_locator(self, item_name: str) -> tuple[str, str]:
        return (By.XPATH,
                f"{self._item_card_locator(item_name)[1]}//button")

    @allure.step("Получить список товаров в каталоге")
    def get_products(self) -> list[Product]:
        return self._read_products()

    def sort_by(self, option: SortOption) -> Self:
        with allure.step(f"Отсортировать товары: {option.label}"):
            Select(self.find_element(self._SORT_SELECT)).select_by_value(
                option.option_value)
            self.wait.until(
                EC.text_to_be_present_in_element(self._ACTIVE_SORT_OPTION,
                                                 option.label),
                message=f"Не применилась сортировка '{option.label}'"
            )
        return self

    @allure.step("Получить выбранный вариант сортировки")
    def get_active_sort_option(self) -> str:
        return self.get_text(self._ACTIVE_SORT_OPTION)

    @allure.step("Получить текст кнопки у товара {item_name}")
    def get_item_button_text(self, item_name: str) -> str:
        return self.get_text(self._item_button_locator(item_name))

    @allure.step("Добавить в корзину товар {item_name}")
    def add_item_to_cart(self, item_name: str) -> Self:
        button = self._item_button_locator(item_name)
        self.wait.until(
            EC.text_to_be_present_in_element(button, self.ADD_TO_CART_TEXT),
            message=f"У товара '{item_name}' нет кнопки "
                    f"'{self.ADD_TO_CART_TEXT}'"
        )
        self.click(button)
        self.wait.until(
            EC.text_to_be_present_in_element(button, self.REMOVE_TEXT),
            message=f"Кнопка у товара '{item_name}' не сменилась "
                    f"на '{self.REMOVE_TEXT}'"
        )
        return self

    @allure.step("Открыть карточку товара {item_name}")
    def open_product(self, item_name: str) -> "ProductPage":
        from pages.product_page import ProductPage

        self.click((By.XPATH,
                    f"{self._item_card_locator(item_name)[1]}"
                    f"//div[@data-test='inventory-item-name']"))
        return ProductPage(self.driver).wait_until_loaded()
