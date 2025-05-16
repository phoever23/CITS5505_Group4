import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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
        dashboard_page.click_logout()
        time.sleep(3)

        # Assert the conditions
        url = self.driver.current_url
        logout_message = login_page.get_alert()
        self.assertTrue(url.endswith('/login'), msg="Failed to redirect to the login page")
        self.assertEqual(logout_message, "You have been logged out", msg="Failed to display the logout message")


if __name__ == "__main__":
    unittest.main()
