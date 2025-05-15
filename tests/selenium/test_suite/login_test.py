import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()

def test_login(driver):
    dashboard_page = DashboardPage(driver)
    login_page = LoginPage(driver)
    login_page.open_page("http://127.0.0.1:5000/login")
    time.sleep(5)
    login_page.enter_username("niranjan")
    time.sleep(3)
    login_page.enter_password("Niranjan9")
    time.sleep(3)
    login_page.click_login()
    time.sleep(5)
    url = driver.current_url
    assert(url.endswith('/dashboard') and dashboard_page.get_banner().endswith('niranjan'))


