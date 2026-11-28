from collections.abc import Iterable

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from models.models import CheckoutInfo, Product
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_overview_page import CheckoutOverviewPage
from steps.cart_steps import CartSteps


class CheckoutSteps:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.cart_steps = CartSteps(driver)

    def proceed_to_overview(self, products: Iterable[Product],
                            info: CheckoutInfo) -> CheckoutOverviewPage:
        with allure.step("Перейти к подтверждению заказа"):
            return (self.cart_steps.open_cart_with(products)
                    .checkout()
                    .fill_form(info)
                    .continue_checkout())

    def place_order(self, products: Iterable[Product],
                    info: CheckoutInfo) -> CheckoutCompletePage:
        with allure.step("Оформить заказ"):
            return self.proceed_to_overview(products, info).finish()
