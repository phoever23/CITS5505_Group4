from selenium.webdriver.common.by import By

class DashboardPage:
    def __init__(self, driver):
        self.driver=driver
        self.home_button=(By.XPATH, "//a[@href='/' and @class='nav-link ']")
        self.upload_button=(By.XPATH, "//a[@href='/upload' and @class='nav-link ']")
        self.share_button=(By.XPATH, "//a[@href='/share' and @class='nav-link ']")
        self.welcome_banner=(By.XPATH, "//span[@class='user-welcome']")
        self.logout_button=(By.XPATH, "//a[@href='/logout' and @class='login-btn']")
    
    def open_page(self, url):
        self.driver.get(url)

    def click_home(self):
        self.driver.find_element(*self.home_button).click()

    def click_upload(self):
        self.driver.find_element(*self.upload_button).click()

    def click_dashboard(self):
        self.driver.find_element(*self.dashboard_button).click()

    def click_share(self):
        self.driver.find_element(*self.share_button).click()
    
    def click_logout(self):
        self.driver.find_element(*self.logout_button).click()
    
    def get_banner(self):
        return self.driver.find_element(*self.welcome_banner).text
