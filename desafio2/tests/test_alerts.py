import pytest
from pages.alerts_page import AlertsPage

pytestmark = pytest.mark.e2e

def test_simple_alert_accept(driver):
    page = AlertsPage(driver)
    page.open()
    page.click_simple_alert()
    page.accept_alert()  

def test_timer_alert_accept(driver):
    page = AlertsPage(driver)
    page.open()
    page.click_timer_alert()
    page.accept_alert()  

def test_confirm_alert_ok_and_cancel(driver):
    page = AlertsPage(driver)
    page.open()
    page.click_confirm()
    page.accept_alert()
    assert "You selected Ok" in page.confirm_result_text()

    page.click_confirm()
    page.dismiss_alert()
    assert "You selected Cancel" in page.confirm_result_text()

def test_prompt_alert_with_text(driver):
    page = AlertsPage(driver)
    page.open()
    name = "Mateus"
    page.click_prompt()
    page.send_text_to_prompt_and_accept(name)
    assert name in page.prompt_result_text()
