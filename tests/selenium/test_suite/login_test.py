import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogin(unittest.TestCase):
    def setUp(self):
        # Setup WebDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        # Cleanup WebDriver
        self.driver.quit()

    def test_login(self):
        # Create instances of page objects
        dashboard_page = DashboardPage(self.driver)
        login_page = LoginPage(self.driver)

        # Open login page
        login_page.open_page("http://127.0.0.1:5000/login")
        time.sleep(5)

        # Perform login actions
        login_page.enter_username("test")
        time.sleep(3)
        login_page.enter_password("qwerty")
        time.sleep(3)
        login_page.click_login()
        time.sleep(5)

        # Assert the conditionsq
        url = self.driver.current_url
        self.assertTrue(url.endswith('/dashboard'))
        self.assertTrue(dashboard_page.get_banner().endswith('test'))


if __name__ == "__main__":
    unittest.main()
