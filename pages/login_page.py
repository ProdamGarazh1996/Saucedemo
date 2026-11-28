from typing import Self

import allure

from models.models import User
from pages.base_page import BasePage
from pages.main_page import MainPage


class LoginPage(BasePage):
    PATH = "/"

    _USERNAME_INPUT = ("id", "user-name")
    _PASSWORD_INPUT = ("id", "password")
    _LOGIN_BUTTON = ("id", "login-button")
    _ERROR_MESSAGE = ("css selector", "[data-test='error']")

    _PAGE_MARKER = _LOGIN_BUTTON

    @allure.step("Ввести логин: {username}")
    def enter_username(self, username: str) -> Self:
        self.type_text(self._USERNAME_INPUT, username)
        return self

    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password: str) -> Self:
        self.type_text(self._PASSWORD_INPUT, password)
        return self

    @allure.step("Нажать на кнопку логина")
    def click_login_button(self) -> None:
        self.click(self._LOGIN_BUTTON)

    @allure.step("Залогиниться на сайт под пользователем: {username}")
    def login(self, username: str, password: str) -> None:
        (self.enter_username(username)
             .enter_password(password)
             .click_login_button())

    def login_as(self, user: User) -> MainPage:
        self.login(user.username, user.password)
        return MainPage(self.driver).wait_until_loaded()

    def login_expecting_error(self, user: User) -> Self:
        self.login(user.username, user.password)
        self.get_error_message()
        return self

    @allure.step("Получить текст ошибки на странице логина")
    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)
