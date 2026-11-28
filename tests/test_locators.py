import allure
import pytest
from selenium.webdriver.common.by import By

from data.test_data import Users
from pages.login_page import LoginPage


@allure.epic("SauceDemo")
@allure.feature("Локаторы")
@allure.title("Тестирование локаторов")
@allure.description("Тестирование локаторов")
@pytest.mark.smoke
def test_locators(browser):
    LoginPage(browser).open().login_as(Users.STANDARD)

    with allure.step("Поиск с помощью основных локаторов"):
        browser.find_element(By.ID, "item_4_img_link")
        browser.find_element(By.NAME, "add-to-cart-sauce-labs-fleece-jacket")
        browser.find_element(By.CLASS_NAME, "title")
        browser.find_element(By.TAG_NAME, "div")
        browser.find_element(By.LINK_TEXT, "Sauce Labs Bolt T-Shirt")
        browser.find_element(By.PARTIAL_LINK_TEXT, " Labs Bolt")

    with allure.step("Поиск с помощью XPath"):
        browser.find_element(By.XPATH, "//a[@id='logout_sidebar_link']")

        browser.find_element(By.XPATH, "//a[text()='Logout']")

        browser.find_element(By.XPATH, "//a[contains(@data-test, 'logou')]")

        browser.find_element(By.XPATH, "//a[contains(text(), 'Log')]")

        browser.find_element(By.XPATH,
                             "//a[contains(text(), 'Log') and @role='button']")

    with allure.step("Поиск по осям XPath"):
        browser.find_element(By.XPATH, "//a[text()='Logout']//ancestor::nav")

        browser.find_element(By.XPATH, "//nav//descendant::a")

        browser.find_element(By.XPATH, "//nav//following::ul")

        browser.find_element(By.XPATH, "//a[text()='Logout']/parent::nav")

        browser.find_element(By.XPATH, "//a[text()='Logout']/preceding::a")

    with allure.step("Поиск с помощью CSS-селекторов"):
        browser.find_element(By.CSS_SELECTOR, ".page_wrapper")

        browser.find_element(By.CSS_SELECTOR, ".btn.btn_primary")

        browser.find_element(By.CSS_SELECTOR,
                             ".inventory_item_description "
                             ".inventory_item_label")

        browser.find_element(By.CSS_SELECTOR, "#logout_sidebar_link")

        browser.find_element(By.CSS_SELECTOR, "footer")

        browser.find_element(By.CSS_SELECTOR, "button.btn")

        browser.find_element(By.CSS_SELECTOR,
                             "[data-test=add-to-cart-sauce-labs-backpack]")

        browser.find_element(By.CSS_SELECTOR,
                             "[data-test~=add-to-cart-sauce-labs-backpack]")

        browser.find_element(By.CSS_SELECTOR,
                             "[data-test|=add-to-cart-sauce-labs-backpack]")

        browser.find_element(By.CSS_SELECTOR, "[data-test^=add-to-cart]")

        browser.find_element(By.CSS_SELECTOR, "[data-test$=labs-backpack]")

        browser.find_element(By.CSS_SELECTOR, "[data-test*=cart-sauce]")
