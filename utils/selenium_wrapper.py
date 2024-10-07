from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import log_info, log_error

PRELOAD_OVERLAY = "preload-overlay"


class SeleniumWrapper:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, timeout=10):
        log_info(f"Searching for element: {locator}")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, PRELOAD_OVERLAY))
            )
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            log_info(f"Element found: {locator}")

            return element
        except TimeoutException:
            log_error(f"Element not found: {locator}")
            return False

    def click_element(self, locator, timeout=10):
        element = self.find_element(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
        log_info(f"Clicking on element: {locator}")
        element.click()
