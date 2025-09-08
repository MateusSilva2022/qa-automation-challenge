from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://demoqa.com/login"
    USER = (By.ID, "userName")
    PASS = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login")
    ERROR_ID = (By.ID, "name")
    ERROR_ALT = (By.XPATH, "//p[contains(@class,'text-danger') or contains(., 'Invalid username')]")
    ERROR_ANY = (By.XPATH, "//*[contains(text(),'Invalid username or password')]")

    def open(self):
        self.visit(self.URL)
        self.remove_ads()
        self.wait_visible(*self.USER)

    def login(self, user, pwd):
        self.find(*self.USER).clear()
        self.find(*self.USER).send_keys(user)
        self.find(*self.PASS).clear()
        self.find(*self.PASS).send_keys(pwd)
        self.safe_click(self.find(*self.LOGIN_BTN))

    def error_text(self, timeout: int = 12) -> str:
        for locator in (self.ERROR_ID, self.ERROR_ALT, self.ERROR_ANY):
            try:
                el = self.wait.until(EC.visibility_of_element_located(locator))
                if el and el.text:
                    return el.text.strip()
            except TimeoutException:
                continue
        return ""
