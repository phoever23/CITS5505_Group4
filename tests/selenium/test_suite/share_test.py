import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.share_page import SharePage
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
        # This test assumes two users in with username - alice and bob

        # Create instances of page objects
        share_page = SharePage(self.driver)
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)

        user1 = "alice"
        user2 = "bob"

        # Open login page
        login_page.open_page("http://127.0.0.1:5000/login")
        time.sleep(5)

        # Login as 'alice'
        login_page.enter_username(user1)
        time.sleep(3)
        login_page.enter_password("qwerty")
        time.sleep(3)
        login_page.click_login()
        time.sleep(5)

        # Navigate to share page and share expense data to user 'bob'
        dashboard_page.click_share()
        time.sleep(3)
        date_range = share_page.enter_dateRange()
        time.sleep(3)
        share_page.enter_username(user2)
        time.sleep(3)
        share_page.click_share()
        time.sleep(2)

        message = share_page.get_successMessage()

        self.assertEqual(message, "Data shared successfully!", msg="Sharing expense data failed")
        
        dashboard_page.click_logout()
        time.sleep(3)

        # Login as 'bob'
        login_page.enter_username(user2)
        time.sleep(3)
        login_page.enter_password("qwerty")
        time.sleep(3)
        login_page.click_login()
        time.sleep(5)

        # Navigate to share page and verify the shared data
        dashboard_page.click_share()
        time.sleep(3)

        # Capture the shared data
        sharedBy = share_page.get_firstSharedName()
        sharedDataRange= share_page.get_firstSharedDateRange()

        # Assert the conditions
        self.assertTrue(sharedBy.endswith(user1))
        self.assertTrue(sharedDataRange.endswith(date_range))



if __name__ == "__main__":
    unittest.main()
