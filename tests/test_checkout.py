import allure
import pytest

from data.test_data import CHECKOUT_INFO, TAX_RATE, Products
from models.models import CheckoutInfo, OrderSummary, Product
from pages.main_page import MainPage
from steps.cart_steps import CartSteps
from steps.checkout_steps import CheckoutSteps


@allure.epic("SauceDemo")
@allure.feature("Оформление заказа")
class TestCheckout:

    @allure.story("Успешный заказ")
    @allure.title("Оформление заказа от корзины до подтверждения")
    @allure.description("Пользователь оформляет заказ, видит сообщение "
                        "об успешном заказе, корзина очищается")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_successful_order(self, main_page: MainPage,
                              checkout_steps: CheckoutSteps):
        complete_page = checkout_steps.place_order(
            [Products.BACKPACK, Products.ONESIE], CHECKOUT_INFO)

        assert complete_page.get_complete_header() == \
            "Thank you for your order!", \
            "Неверный заголовок сообщения о заказе"
        assert complete_page.get_complete_text() == (
            "Your order has been dispatched, and will arrive just as fast "
            "as the pony can get there!"
        ), "Неверный текст сообщения о заказе"
        assert complete_page.get_cart_badge_count() == 0, \
            "После оформления заказа корзина не очистилась"

        main_page = complete_page.back_home()

        assert main_page.get_cart_badge_count() == 0, \
            "После возврата в каталог корзина не пуста"

    @allure.story("Подтверждение заказа")
    @allure.title("Итоги заказа: {case}")
    @allure.description("На шаге подтверждения отображаются выбранные "
                        "товары, сумма товаров, налог 8% и итоговая сумма")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("case, products", [
        ("один товар", [Products.BACKPACK]),
        ("два товара", [Products.BIKE_LIGHT, Products.BOLT_T_SHIRT]),
        ("все товары", list(Products.ALL)),
    ], ids=["one_product", "two_products", "all_products"])
    def test_order_summary(self, main_page: MainPage,
                           cart_steps: CartSteps, case: str,
                           products: list[Product]):
        overview_page = (cart_steps
                         .open_cart_with(products)
                         .checkout()
                         .fill_form(CHECKOUT_INFO)
                         .continue_checkout())

        assert overview_page.get_items() == products, \
            "Товары в заказе не соответствуют добавленным в корзину"
        assert overview_page.get_summary() == OrderSummary.calculate(
            products, TAX_RATE), \
            "Итоги заказа рассчитаны неверно"

    @allure.story("Данные покупателя")
    @allure.title("Валидация формы покупателя: {case}")
    @allure.description("Без обязательного поля нельзя перейти к "
                        "подтверждению заказа, отображается ошибка")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("case, info, expected_error", [
        ("не указано имя",
         CheckoutInfo("", "Ivanov", "123456"),
         "Error: First Name is required"),
        ("не указана фамилия",
         CheckoutInfo("Ivan", "", "123456"),
         "Error: Last Name is required"),
        ("не указан индекс",
         CheckoutInfo("Ivan", "Ivanov", ""),
         "Error: Postal Code is required"),
    ], ids=["empty_first_name", "empty_last_name", "empty_postal_code"])
    def test_checkout_form_validation(self, main_page: MainPage,
                                      cart_steps: CartSteps, case: str,
                                      info: CheckoutInfo,
                                      expected_error: str):

        info_page = (cart_steps
                     .open_cart_with([Products.BACKPACK])
                     .checkout()
                     .fill_form(info)
                     .continue_expecting_error())

        assert info_page.get_error_message() == expected_error, \
            "Текст ошибки валидации не соответствует ожидаемому"
        assert info_page.is_loaded(), \
            "Пользователь ушёл со страницы ввода данных"
