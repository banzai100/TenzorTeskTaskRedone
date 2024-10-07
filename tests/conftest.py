import pytest
from selenium import webdriver
from utils.logger import log_info


@pytest.fixture
def driver():
    log_info("Инициализация веб-драйвера")
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    log_info("Закрытие веб-драйвера")
    driver.quit()
