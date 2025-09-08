from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def visit(self, url: str):
        self.driver.get(url)

    def find(self, by, locator):
        return self.driver.find_element(by, locator)

    def finds(self, by, locator):
        return self.driver.find_elements(by, locator)

    def wait_visible(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def scroll_into_view(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def js_click(self, el):
        self.driver.execute_script("arguments[0].click();", el)

    def remove_ads(self):
        self.driver.execute_script("""
            const sels = ['#fixedban', '#adplus-anchor', '.Advertisement',
                          '[id^="google_ads"]', 'iframe[id^="google_ads"]',
                          'iframe[aria-label="Advertisement"]'];
            for (const s of sels) document.querySelectorAll(s).forEach(e => { try{ e.remove(); }catch(e){} });
        """)

    def safe_click(self, el):
        try:
            self.scroll_into_view(el)
            el.click()
        except ElementClickInterceptedException:
            self.remove_ads()
            self.scroll_into_view(el)
            try:
                el.click()
            except ElementClickInterceptedException:
                self.js_click(el)
