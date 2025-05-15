import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.signup_page import SignupPage
from pages.login_page import LoginPage

class Signup(unittest.TestCase):
    def setUp(self):
        # Setup Webdriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def tearDown(self):
        # Cleanup WebDriver
        self.driver.quit()
            
    def test_signup(self):
        signup_page = SignupPage(self.driver)
        login_page = LoginPage(self.driver)
        signup_page.open_page("http://127.0.0.1:5000/signup")
        time.sleep(5)
        signup_page.enter_username("test4")
        time.sleep(3)
        signup_page.enter_password("test098")
        time.sleep(3)
        signup_page.confirm_password("test098")
        time.sleep(3)
        signup_page.click_signup()
        time.sleep(3)
        url = self.driver.current_url
        alert=login_page.get_alert()
        self.assertTrue(url.endswith('/login'), msg="Failed to redirect to the login page")
        self.assertTrue(alert == "Account created successfully! Please login",msg="Success alert not found")

if __name__ == "__main__":
    unittest.main()