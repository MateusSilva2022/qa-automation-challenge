import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AlertsPage:
    URL = "https://demoqa.com/alerts"
    TIMEOUT = 25  

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self):
        self.driver.get(self.URL)
        self._hide_ads()

    def _hide_ads(self):
        self.driver.execute_script("""
            for (let id of ['fixedban','adplus-anchor']) {
                const el = document.getElementById(id);
                if (el) el.remove();
            }
            const foot = document.querySelector('footer');
            if (foot) foot.remove();
        """)

   
    def _safe_click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        try:
            el.click()
        except Exception:
            
            self.driver.execute_script("arguments[0].click();", el)

    def wait_for_alert(self):
      
        try:
            return self.wait.until(EC.alert_is_present())
        except TimeoutException:
            try:
                self._safe_click((By.ID, "promtButton"))
            except Exception:
                pass
            return WebDriverWait(self.driver, 5).until(EC.alert_is_present())

    def accept_alert(self):
        self.wait_for_alert().accept()

    def dismiss_alert(self):
        self.wait_for_alert().dismiss()

    def send_text_to_prompt_and_accept(self, text):
        alert = self.wait_for_alert()
        alert.send_keys(text)
        alert.accept()

   
    def click_simple_alert(self):
        self._safe_click((By.ID, "alertButton"))

    def click_timer_alert(self):
        self._safe_click((By.ID, "timerAlertButton"))

    def click_confirm(self):
        self._safe_click((By.ID, "confirmButton"))

    def confirm_result_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "confirmResult"))).text.strip()

    def click_prompt(self):
        self._safe_click((By.ID, "promtButton"))

    def prompt_result_text(self):
        return self.wait.until(EC.visibility_of_element_located((By.ID, "promptResult"))).text.strip()
