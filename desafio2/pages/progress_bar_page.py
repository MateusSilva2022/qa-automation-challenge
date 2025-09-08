import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProgressBarPage:
    URL = "https://demoqa.com/progress-bar"
    TIMEOUT = 30 

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def open(self):
        self.driver.get(self.URL)
        self._hide_ads()

    def _hide_ads(self):
        self.driver.execute_script("""
            for (let id of ['fixedban','adplus-anchor']) { const el = document.getElementById(id); if (el) el.remove(); }
            const foot = document.querySelector('footer'); if (foot) foot.remove();
        """)

   
    def _bar_el(self):
   
        return self.wait.until(EC.presence_of_element_located((By.ID, "progressBar")))

    def start_stop_btn(self):
        return self.wait.until(EC.element_to_be_clickable((By.ID, "startStopButton")))

    def reset_btn(self):
        return self.driver.find_element(By.ID, "resetButton")

   
    def get_value(self) -> int:
        el = self._bar_el()
      
        aria = el.get_attribute("aria-valuenow")
        if aria and aria.isdigit():
            return int(aria)
      
        style = el.get_attribute("style") or ""
        if "width:" in style and "%" in style:
            try:
                return int(style.split("width:")[1].split("%")[0].strip())
            except Exception:
                pass
      
        txt = (el.text or "").strip().replace("%", "")
        return int(txt) if txt.isdigit() else 0

    def start(self):
        self.start_stop_btn().click()

    def stop(self):
        self.start_stop_btn().click()

    def reset(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "resetButton"))).click()

    def wait_until_running(self):
        
        self.wait.until(lambda d: self.get_value() > 0)

    def wait_until_100(self):
        self.wait.until(lambda d: self.get_value() == 100)

    def wait_until_zero(self):
        self.wait.until(lambda d: self.get_value() == 0)

   
    def stop_near(self, target: int = 25, tolerance: int = 7) -> int:
        """
        Inicia (se ainda não), espera começar a andar e pára quando
        o valor atingir target - tolerance (ex.: 18%) para estabilizar <= target.
        Retorna o valor final após parar.
        """
      
        self.start()
        self.wait_until_running()

        lower_bound = max(1, target - tolerance)
        end = time.monotonic() + self.TIMEOUT
        last = 0
        while time.monotonic() < end:
            v = self.get_value()
          
            if v >= lower_bound:
                self.stop()
                time.sleep(0.15)  
                return self.get_value()
            last = v
            time.sleep(0.05)
       
        self.stop()
        time.sleep(0.15)
        return self.get_value()
