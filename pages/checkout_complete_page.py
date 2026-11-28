import allure

from pages.authorized_page import AuthorizedPage
from pages.main_page import MainPage


class CheckoutCompletePage(AuthorizedPage):
    PATH = "/checkout-complete.html"
    _PAGE_MARKER = AuthorizedPage._title_marker("Checkout: Complete!")

    _COMPLETE_HEADER = ("css selector", "[data-test='complete-header']")
    _COMPLETE_TEXT = ("css selector", "[data-test='complete-text']")
    _BACK_HOME_BUTTON = ("id", "back-to-products")

    @allure.step("Получить заголовок сообщения о заказе")
    def get_complete_header(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)

    @allure.step("Получить текст сообщения о заказе")
    def get_complete_text(self) -> str:
        return self.get_text(self._COMPLETE_TEXT)

    @allure.step("Нажать кнопку 'Back Home'")
    def back_home(self) -> MainPage:
        self.click(self._BACK_HOME_BUTTON)
        return MainPage(self.driver).wait_until_loaded()
