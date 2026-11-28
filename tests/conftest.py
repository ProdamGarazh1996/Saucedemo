import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from data.test_data import Users
from pages.login_page import LoginPage
from pages.main_page import MainPage
from steps.auth_steps import AuthSteps
from steps.cart_steps import CartSteps
from steps.checkout_steps import CheckoutSteps


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Браузер для запуска тестов",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера без окна",
    )


def _chrome_options(headless: bool) -> ChromeOptions:
    options = ChromeOptions()

    chrome_prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }

    options.add_experimental_option("prefs", chrome_prefs)

    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    return options


def _firefox_options(headless: bool) -> FirefoxOptions:
    options = FirefoxOptions()

    options.set_preference("signon.rememberSignons", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.disable_open_during_load", False)

    if headless:
        options.add_argument("-headless")
    return options


def _create_driver(browser_name: str, headless: bool) -> WebDriver:
    if browser_name == "firefox":
        return webdriver.Firefox(options=_firefox_options(headless))
    return webdriver.Chrome(options=_chrome_options(headless))


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    with allure.step(f"Запуск браузера {browser_name}"):
        driver = _create_driver(browser_name, headless)
        if headless:
            driver.set_window_size(*settings.window_size)
        else:
            driver.maximize_window()
    yield driver
    with allure.step("Закрытие браузера"):
        driver.quit()


@pytest.fixture
def login_page(browser) -> LoginPage:
    return LoginPage(browser).open()


@pytest.fixture
def main_page(auth_steps) -> MainPage:
    return auth_steps.login_as(Users.STANDARD)


@pytest.fixture
def auth_steps(browser) -> AuthSteps:
    return AuthSteps(browser)


@pytest.fixture
def cart_steps(browser) -> CartSteps:
    return CartSteps(browser)


@pytest.fixture
def checkout_steps(browser) -> CheckoutSteps:
    return CheckoutSteps(browser)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when in ("setup", "call") and report.failed:
        browser = item.funcargs.get("browser")
        if browser:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="screenshot on fail",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(
                browser.current_url,
                name="url on fail",
                attachment_type=allure.attachment_type.URI_LIST,
            )
            allure.attach(
                browser.page_source,
                name="page source on fail",
                attachment_type=allure.attachment_type.HTML,
            )
