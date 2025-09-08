import pytest
from pages.browser_windows_page import BrowserWindowsPage

pytestmark = pytest.mark.e2e

def test_new_window_has_sample_text_and_is_closed(driver):
    page = BrowserWindowsPage(driver)
    page.open()

    page.click_new_window()
    page.switch_to_new_window()

    assert page.get_sample_heading_text() == "This is a sample page"

    page.close_current_and_back()
