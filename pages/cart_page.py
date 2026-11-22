import allure
from selenium.webdriver.common.by import By

from models.models import CartItemData
from pages.base_page import BasePage


class CartPage(BasePage):
    _INVENTORY_ITEM = (By.XPATH, "//div[@data-test='inventory-item']")
    _INVENTORY_ITEM_NAME = (By.XPATH,
                            ".//div[@data-test='inventory-item-name']")
    _INVENTORY_ITEM_DESC = (By.XPATH,
                            ".//div[@data-test='inventory-item-desc']")
    _INVENTORY_ITEM_PRICE = (By.XPATH,
                             ".//div[@data-test='inventory-item-price']")

    @allure.step("Проверить товар в корзине")
    def check_cart_item(self, expected_item: CartItemData,
                        actual_item_index: int):
        cart_items = self.find_elements(self._INVENTORY_ITEM)
        actual_item_name = (cart_items[actual_item_index]
                            .find_element(*self._INVENTORY_ITEM_NAME).text)

        actual_item_desc = (cart_items[actual_item_index]
                            .find_element(*self._INVENTORY_ITEM_DESC).text)

        actual_item_price = (cart_items[actual_item_index]
                             .find_element(*self._INVENTORY_ITEM_PRICE).text)

        assert actual_item_name == expected_item.name, \
            ("Ожидаемое значение имени в карточке товара не соответствует "
             "фактической")

        assert actual_item_desc == expected_item.description, \
            ("Ожидаемое значение описания в карточке товара не соответствует "
             "фактической")
        assert actual_item_price == expected_item.price, \
            ("Ожидаемое значение цены в карточке товара не соответствует "
             "фактической")
