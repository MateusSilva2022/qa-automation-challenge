from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserWindowsPage:
    URL = "https://demoqa.com/browser-windows"
    TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)
        self._main_handle = None

    def open(self):
        self.driver.get(self.URL)
        self._hide_ads()

    def _hide_ads(self):
        # remove banners/ads que atrapalham cliques no DemoQA
        self.driver.execute_script("""
            for (let id of ['fixedban','adplus-anchor']) {
                const el = document.getElementById(id);
                if (el) el.remove();
            }
            const foot = document.querySelector('footer');
            if (foot) foot.remove();
        """)

    # --- ações ---
    def click_new_window(self):
        self._main_handle = self.driver.current_window_handle
        self.wait.until(EC.element_to_be_clickable((By.ID, "windowButton"))).click()

    def switch_to_new_window(self):
        # espera até existir uma segunda janela/aba
        self.wait.until(EC.number_of_windows_to_be(2))
        for h in self.driver.window_handles:
            if h != self._main_handle:
                self.driver.switch_to.window(h)
                return h
        raise RuntimeError("Nova janela não encontrada")

    def get_sample_heading_text(self):
        # na página https://demoqa.com/sample o ID é 'sampleHeading'
        el = self.wait.until(EC.visibility_of_element_located((By.ID, "sampleHeading")))
        return el.text.strip()

    def close_current_and_back(self):
        self.driver.close()
        self.driver.switch_to.window(self._main_handle)
