import os
import urllib

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from utils.logger import log_info, log_error


class SbisPage(BasePage):
    CONTACTS_BUTTON = (By.XPATH, "//a[@href='/contacts' and contains(text(), 'Контакты')]")
    TENSOR_BANNER = (By.XPATH, "//img[@alt='Разработчик системы СБИС — компания «Тензор»']")
    REGION_CHOOSER = (By.XPATH, "//span[contains(@class, 'sbis_ru-Region-Chooser__text')]")
    PARTNER_ELEMENT = (By.CLASS_NAME, "sbisru-Contacts-List__name")
    KAMCHATKA_KRAI = (By.XPATH, "//span[text()='41 Камчатский край']")
    DIALOG_LOCATOR = (By.XPATH, "//div[@name='dialog' and contains(@class, 'sbis_ru-Region-Panel')]")
    FOOTER_DOWNLOAD = (By.XPATH, "//a[@href='/download' and text()='Скачать локальные версии']")
    WEB_DOWNLOAD = (By.XPATH,
                    "//h3[contains(text(),'Веб-установщик')]/following::a[@class='sbis_ru-DownloadNew-loadLink__link js-link']")

    def get_contacts_names(self):
        partners_elements = self.wrapper.driver.find_elements(*self.PARTNER_ELEMENT)
        partners_names = [element.text for element in partners_elements]
        return partners_names

    def wait_for_text_change(self, original_partners, timeout=5):
        WebDriverWait(self.wrapper.driver, 10).until(
            EC.invisibility_of_element_located(self.KAMCHATKA_KRAI)
        )

        def element_text_changed(driver):
            try:
                # Finding all partners
                elements = driver.find_elements(*self.PARTNER_ELEMENT)
                if not elements:
                    return False

                # Checking that the elements actually have text
                if [element.text for element in elements] == original_partners:
                    return False
                return True
            except Exception:
                # If we receive a StaleElementReferenceException, return False.
                return False

        # Wait until the elements have changed text or raise a stale element error.
        try:
            WebDriverWait(self.wrapper.driver, timeout).until(
                element_text_changed
            )
        except Exception:
            ...

    def download_web_installer(self):
        download_obj = self.find_element(self.WEB_DOWNLOAD)
        url = download_obj.get_attribute("href")
        target = url.split("/")[-1]
        save_path = os.path.join(os.getcwd(), 'resources', 'download', target)
        expected_size = float("".join([char for char in download_obj.text if char.isdigit() or char == "."]))
        log_info(f"Expected installer file size: {expected_size}")
        try:
            urllib.request.urlretrieve(url, save_path)
        except urllib.error.URLError:
            log_error("Web installer file not available")
            return False
        if os.path.exists(save_path):
            file_size = round(os.path.getsize(save_path) / (1024 * 1024), 2)
            if file_size == expected_size:
                log_info(f"Web installer file successfully download with size {file_size}")
            else:
                log_error(f"Web installer file size incorrect")
                return False
        return True
