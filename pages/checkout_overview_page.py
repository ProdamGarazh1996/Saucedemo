import allure

from models.models import OrderSummary, Product, parse_price
from pages.authorized_page import AuthorizedPage
from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage(AuthorizedPage):
    PATH = "/checkout-step-two.html"
    _PAGE_MARKER = AuthorizedPage._title_marker("Checkout: Overview")

    _ITEM_TOTAL_LABEL = ("css selector", "[data-test='subtotal-label']")
    _TAX_LABEL = ("css selector", "[data-test='tax-label']")
    _TOTAL_LABEL = ("css selector", "[data-test='total-label']")
    _FINISH_BUTTON = ("id", "finish")

    @allure.step("Получить список товаров в заказе")
    def get_items(self) -> list[Product]:
        return self._read_products()

    @allure.step("Получить итоги заказа")
    def get_summary(self) -> OrderSummary:
        return OrderSummary(
            item_total=parse_price(self.get_text(self._ITEM_TOTAL_LABEL)),
            tax=parse_price(self.get_text(self._TAX_LABEL)),
            total=parse_price(self.get_text(self._TOTAL_LABEL)),
        )

    @allure.step("Нажать кнопку 'Finish'")
    def finish(self) -> CheckoutCompletePage:
        self.click(self._FINISH_BUTTON)
        return CheckoutCompletePage(self.driver).wait_until_loaded()
