from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver=driver
        self.username_textbox=(By.ID, "username")
        self.password_textbox=(By.ID, "password")
        self.login_button=(By.ID, "submit")
        self.success_alert=(By.XPATH, "//div[@role='alert']")

    def open_page(self, url):
        self.driver.get(url)
    
    def enter_username(self, username):
        self.driver.find_element(*self.username_textbox).send_keys(username)
    
    def enter_password(self, password):
        self.driver.find_element(*self.password_textbox).send_keys(password)
    
    def click_login(self):
        self.driver.find_element(*self.login_button).click()
    
    def get_alert(self):
        return self.driver.find_element(*self.success_alert).text