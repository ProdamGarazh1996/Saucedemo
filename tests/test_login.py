import allure
import pytest

from data.test_data import Users
from models.models import User
from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.epic("SauceDemo")
@allure.feature("Авторизация")
class TestLogin:

    @allure.story("Успешный вход")
    @allure.title("Успешная авторизация пользователем {user.username}")
    @allure.description("Пользователь с валидными данными попадает "
                        "в каталог товаров, корзина пуста")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.parametrize("user", [
        Users.STANDARD,
        Users.PROBLEM,
        Users.PERFORMANCE_GLITCH,
        Users.ERROR,
        Users.VISUAL,
    ], ids=lambda user: user.username)
    def test_successful_login(self, login_page: LoginPage, user: User):
        main_page = login_page.login_as(user)

        assert main_page.get_title() == "Products", \
            "После логина не открылся каталог товаров"
        assert main_page.get_cart_badge_count() == 0, \
            "У нового пользователя корзина не пуста"

    @allure.story("Неуспешный вход")
    @allure.title("Ошибка авторизации: {case}")
    @allure.description("При невалидных данных пользователь остаётся "
                        "на странице логина и видит сообщение об ошибке")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("case, user, expected_error", [
        ("заблокированный пользователь", Users.LOCKED_OUT,
         "Epic sadface: Sorry, this user has been locked out."),
        ("неверный логин и пароль", Users.INVALID,
         "Epic sadface: Username and password do not match any user "
         "in this service"),
        ("пустой логин", User("", "secret_sauce"),
         "Epic sadface: Username is required"),
        ("пустой пароль", User("standard_user", ""),
         "Epic sadface: Password is required"),
    ], ids=["locked_out", "invalid_credentials", "empty_username",
            "empty_password"])
    def test_login_with_invalid_data(self, auth_steps, case: str,
                                     user: User, expected_error: str):
        login_page = auth_steps.try_to_login(user)

        assert login_page.get_error_message() == expected_error, \
            "Текст ошибки авторизации не соответствует ожидаемому"
        assert login_page.is_loaded(), \
            "Пользователь ушёл со страницы логина"

    @allure.story("Выход")
    @allure.title("Выход из системы через боковое меню")
    @allure.description("После выхода открывается страница логина, "
                        "а каталог снова требует авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_logout(self, browser, main_page: MainPage):
        login_page = main_page.logout()

        assert login_page.is_loaded(), "Не открылась страница логина"

        MainPage(browser).load()
        assert login_page.wait_until_loaded().get_error_message() == (
            "Epic sadface: You can only access '/inventory.html' "
            "when you are logged in."
        ), "После выхода каталог доступен без авторизации"
