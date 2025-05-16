from selenium.webdriver.common.by import By

class SignupPage:
    def __init__(self, driver):
        self.driver=driver
        self.username_textbox=(By.ID, "username")
        self.password_textbox=(By.ID, "password")
        self.confirm_textbox=(By.ID, "confirm_password")
        self.signup_button=(By.ID, "submit")
    
    def open_page(self, url):
        self.driver.get(url)
    
    def enter_username(self, username):
        self.driver.find_element(*self.username_textbox).send_keys(username)
    
    def enter_password(self, password):
        self.driver.find_element(*self.password_textbox).send_keys(password)
    
    def confirm_password(self, password):
        self.driver.find_element(*self.confirm_textbox).send_keys(password)

    def click_signup(self):
        self.driver.find_element(*self.signup_button).click()

    