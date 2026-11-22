import allure
import pytest

from models.models import CartItemData
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.title("Тестирование товара в корзине")
@allure.description("Тестирование товара в корзине")
@pytest.mark.regression
def test_cart(browser):
    login_page = LoginPage(browser)
    main_page = MainPage(browser)
    cart_page = CartPage(browser)
    login_page.open("https://www.saucedemo.com/")
    login_page.login("standard_user", "secret_sauce")
    login_page.wait_until_document_loaded()
    first_item = main_page.find_element(cart_page._INVENTORY_ITEM)
    cart_item_data = CartItemData(
        name=first_item.find_element(*cart_page._INVENTORY_ITEM_NAME).text,
        description=first_item.find_element(
            *cart_page._INVENTORY_ITEM_DESC).text,
        price=first_item.find_element(*cart_page._INVENTORY_ITEM_PRICE).text
    )

    main_page.add_item_to_cart("Sauce Labs Backpack")
    main_page.click_on_shopping_cart_link()
    cart_page.check_cart_item(cart_item_data, 0)
