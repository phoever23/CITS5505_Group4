from selenium.webdriver.common.by import By
import time
import random

class SharePage:
    def __init__(self, driver):
        self.driver=driver
        self.dateRange_field=(By.ID, "dateRange")
        self.dateRange_options=(By.XPATH, "//select[@id='dateRange']/option")
        self.shareWith_field=(By.ID, "shareWith")
        self.search_results=(By.XPATH, "//div[@id='searchResults']/div")
        self.share_button=(By.ID, "shareDataBtn")
        self.success_message=(By.XPATH, "//div[@class='success-message']")
        self.sharedBy_names=(By.XPATH, "//div[@class='shared-data-info']/h3")
        self.sharedBy_dateRange=(By.XPATH, "//div[@class='shared-data-info']/div/p")

    
    def open_page(self, url):
        self.driver.get(url+"/share")
    
    def enter_dateRange(self):
        self.driver.find_element(*self.dateRange_field).click()
        time.sleep(1)
        options = (self.driver.find_elements(*self.dateRange_options))
        date_selection=random.choice(options)
        date_selection.click()
        return date_selection.text

    def enter_username(self, user):
        self.driver.find_element(*self.shareWith_field).send_keys(user)
        firstResult = self.driver.find_element(*self.search_results)
        firstResult.click()
        time.sleep(1)

    def click_share(self):
        self.driver.find_element(*self.share_button).click()
    
    def get_successMessage(self):
        return self.driver.find_element(*self.success_message).text
    
    def get_firstSharedName(self):
        return self.driver.find_element(*self.sharedBy_names).text
    
    def get_firstSharedDateRange(self):
        return self.driver.find_element(*self.sharedBy_dateRange).text
