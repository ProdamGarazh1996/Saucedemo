import allure
from selenium.webdriver.remote.webdriver import WebDriver

from models.models import User
from pages.login_page import LoginPage
from pages.main_page import MainPage


class AuthSteps:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def login_as(self, user: User) -> MainPage:
        with allure.step(f"Авторизоваться пользователем '{user.username}'"):
            return LoginPage(self.driver).open().login_as(user)

    def try_to_login(self, user: User) -> LoginPage:
        with allure.step(f"Попытаться авторизоваться пользователем "
                         f"'{user.username}'"):
            return LoginPage(self.driver).open().login_expecting_error(user)
