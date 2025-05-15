import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.signup_page import SignupPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()

def test_signup(driver):
    signup_page = SignupPage(driver)
    signup_page.open_page("http://127.0.0.1:5000/signup")
    time.sleep(5)
    signup_page.enter_username("test11")
    time.sleep(3)
    signup_page.enter_password("test098")
    time.sleep(3)
    signup_page.confirm_password("test098")
    time.sleep(3)
    signup_page.click_signup()
    time.sleep(3)
    url = driver.current_url
    assert(url.endswith('/login'))