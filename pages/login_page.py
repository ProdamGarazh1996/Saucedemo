import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    _USERNAME_INPUT = ("id", "user-name")
    _PASSWORD_INPUT = ("id", "password")
    _LOGIN_BUTTON = ("id", "login-button")

    @allure.step("Ввести логин: {username}")
    def enter_username(self, username: str):
        element = self.find_element(self._USERNAME_INPUT)
        element.clear()
        element.send_keys(username)

    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password: str):
        element = self.find_element(self._PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)

    @allure.step("Нажать на кнопку логина")
    def click_login_button(self):
        self.find_element(self._LOGIN_BUTTON).click()

    @allure.step("Залогиниться на сайт под пользователем: {username}")
    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
