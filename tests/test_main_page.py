from pages.sbis_page import SbisPage
from pages.tensor_page import TensorPage

KAMCHATSKIJ_KRAJ_ENG = "kamchatskij-kraj"
KAMCHATSKIJ_KRAJ_RUS = "Камчатский край"
SBIS_URL = "https://sbis.ru/"
SVERDLOVSKAYA_OBL_RUS = "Свердловская обл."


def test_first_case(driver):
    sbis_page = SbisPage(driver)

    sbis_page.go_to(SBIS_URL)
    sbis_page.click_element(sbis_page.CONTACTS_BUTTON)
    sbis_page.click_element(sbis_page.TENSOR_BANNER)

    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])

    tensor_page = TensorPage(driver)

    assert tensor_page.find_element(tensor_page.POWER_IN_PEOPLE), "Element 'Strength in People' not found"

    tensor_page.click_element(tensor_page.DETAILS)
    assert tensor_page.find_and_compare_images(), "The sizes of the photos do not match"


def test_second_case(driver):
    sbis_page = SbisPage(driver)

    sbis_page.go_to(SBIS_URL)
    sbis_page.click_element(sbis_page.CONTACTS_BUTTON)

    region_chooser = sbis_page.find_element(sbis_page.REGION_CHOOSER)
    assert region_chooser.text.strip() == SVERDLOVSKAYA_OBL_RUS, "The automatically selected region is incorrect."
    sverdl_obl_partners = sbis_page.get_contacts_names()

    sbis_page.click_element(sbis_page.REGION_CHOOSER)
    sbis_page.click_element(sbis_page.KAMCHATKA_KRAI)

    sbis_page.wait_for_text_change(sverdl_obl_partners)

    kamchatka_kraj_partners = sbis_page.get_contacts_names()
    assert sverdl_obl_partners != kamchatka_kraj_partners, "Partners list do not change"
    assert KAMCHATSKIJ_KRAJ_ENG in sbis_page.wrapper.driver.current_url, "The current region in the URL is incorrect."
    assert KAMCHATSKIJ_KRAJ_RUS in sbis_page.find_element(sbis_page.REGION_CHOOSER).text, "Current region do not change"


def test_third_case(driver):
    sbis_page = SbisPage(driver)
    sbis_page.go_to(SBIS_URL)
    sbis_page.click_element(sbis_page.FOOTER_DOWNLOAD)
    assert sbis_page.download_web_installer(), "File not available or size incorrect"
