from selenium.webdriver.common.by import By

from .base_page import BasePage
from utils.logger import log_info


class TensorPage(BasePage):
    POWER_IN_PEOPLE = (By.XPATH, "//p[text()='Сила в людях']")
    DETAILS = (By.XPATH, "//a[@href='/about' and text()='Подробнее']")
    COOKIE_AGREEMENT = (
        By.XPATH, "//div[contains(@class, 'tensor_ru-CookieAgreement__close') and contains(@class, 'icon-Close')]")
    WORKING = (By.XPATH, "//h2[contains(text(), 'Работаем')]")

    def find_and_compare_images(self):
        # Find the header and parent block.
        header = self.find_element(self.WORKING)
        parent_block = header.find_element(By.XPATH, "../..")

        # Find all images in the parent block.
        images = parent_block.find_elements(By.TAG_NAME, "img")

        if not images:
            log_info("Images in the block were not found.")
            return False

        first_image_width = images[0].get_attribute("width")
        first_image_height = images[0].get_attribute("height")

        for img in images:
            width = img.get_attribute("width")
            height = img.get_attribute("height")

            if width != first_image_width or height != first_image_height:
                log_info("The dimensions of the images do not match.")
                return False
        log_info("All images have the same dimensions.")
        return True
