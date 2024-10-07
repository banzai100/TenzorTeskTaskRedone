from utils.selenium_wrapper import SeleniumWrapper


class BasePage:
    def __init__(self, driver):
        self.wrapper = SeleniumWrapper(driver)

    def go_to(self, url):
        self.wrapper.driver.get(url)

    def find_element(self, locator, timeout=10):
        return self.wrapper.find_element(locator, timeout)

    def click_element(self, locator, timeout=10):
        self.wrapper.click_element(locator, timeout)
