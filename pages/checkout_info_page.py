from typing import Self

import allure

from models.models import CheckoutInfo
from pages.authorized_page import AuthorizedPage
from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInfoPage(AuthorizedPage):
    PATH = "/checkout-step-one.html"
    _PAGE_MARKER = AuthorizedPage._title_marker("Checkout: Your Information")

    _FIRST_NAME_INPUT = ("id", "first-name")
    _LAST_NAME_INPUT = ("id", "last-name")
    _POSTAL_CODE_INPUT = ("id", "postal-code")
    _CONTINUE_BUTTON = ("id", "continue")
    _ERROR_MESSAGE = ("css selector", "[data-test='error']")

    @allure.step("Ввести имя: {first_name}")
    def enter_first_name(self, first_name: str) -> Self:
        self.type_text(self._FIRST_NAME_INPUT, first_name)
        return self

    @allure.step("Ввести фамилию: {last_name}")
    def enter_last_name(self, last_name: str) -> Self:
        self.type_text(self._LAST_NAME_INPUT, last_name)
        return self

    @allure.step("Ввести почтовый индекс: {postal_code}")
    def enter_postal_code(self, postal_code: str) -> Self:
        self.type_text(self._POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_form(self, info: CheckoutInfo) -> Self:
        with allure.step("Заполнить данные покупателя"):
            return (self.enter_first_name(info.first_name)
                        .enter_last_name(info.last_name)
                        .enter_postal_code(info.postal_code))

    @allure.step("Нажать кнопку 'Continue'")
    def continue_checkout(self) -> CheckoutOverviewPage:
        self.click(self._CONTINUE_BUTTON)
        return CheckoutOverviewPage(self.driver).wait_until_loaded()

    @allure.step("Нажать кнопку 'Continue' (ожидается ошибка)")
    def continue_expecting_error(self) -> Self:
        self.click(self._CONTINUE_BUTTON)
        self.get_error_message()
        return self

    @allure.step("Получить текст ошибки")
    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)
