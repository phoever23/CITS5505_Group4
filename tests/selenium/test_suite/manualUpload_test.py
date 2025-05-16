import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.upload_page import UploadPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        upload_page = UploadPage(self.driver)

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

        dashboard_page.click_upload()
        time.sleep(3)
        date_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "entryDate"))
        )
        self.driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """, date_input, "2024-05-12")
        time.sleep(3)
        upload_page.enter_category()
        time.sleep(3)
        upload_page.enter_subcategory()
        time.sleep(3)
        upload_page.enter_amount()
        time.sleep(3)
        upload_page.enter_currency()
        time.sleep(3)
        upload_page.click_addExpense()
        time.sleep(0.5)

        toastMessage = upload_page.get_toastMessage()

        # Assert the conditions
        self.assertEqual(toastMessage, "Expenses added successfully")


if __name__ == "__main__":
    unittest.main()
