from selenium.webdriver.common.by import By
import time
import random

class UploadPage:
    def __init__(self, driver):
        self.driver=driver
        self.date_field=(By.ID,"entryDate")
        self.category_field=(By.ID, "entryCategory")
        self.category_options=(By.XPATH, "//select[@id='entryCategory']/option[@value!='']")
        self.subcategory_field=(By.ID, "entrySubcategory")
        self.subcategory_options=(By.XPATH, "//select[@id='entrySubcategory']/option[@value!='']")
        self.amount_field=(By.ID, "entryAmount")
        self.currency_field=(By.ID, "entryCurrency")
        self.currency_options=(By.XPATH, "//select[@id='entryCurrency']/option")
        self.add_button=(By.XPATH, "//button[@class='submit-btn']")
        self.toast=(By.XPATH, "//div[contains(@class, 'toast')]")
    
    def open_page(self, url):
        self.driver.get(url+"/upload")
    
    def enter_date(self, date):
        self.driver.find_element(*self.date_field).send_keys(date)
    
    def enter_category(self):
        self.driver.find_element(*self.category_field).click()
        time.sleep(1)
        options = (self.driver.find_elements(*self.category_options))
        random.choice(options).click()
    
    def enter_subcategory(self):
        self.driver.find_element(*self.subcategory_field).click()
        time.sleep(1)
        options = (self.driver.find_elements(*self.subcategory_options))
        random.choice(options).click()
    
    def enter_amount(self):
        amount = random.randint(10, 100)
        self.driver.find_element(*self.amount_field).send_keys(amount)

    def enter_currency(self):
        self.driver.find_element(*self.currency_field).click()
        time.sleep(1)
        options = (self.driver.find_elements(*self.currency_options))
        random.choice(options).click()

    def click_addExpense(self):
        self.driver.find_element(*self.add_button).click()
    
    def get_toastMessage(self):
        return self.driver.find_element(*self.toast).text
        
