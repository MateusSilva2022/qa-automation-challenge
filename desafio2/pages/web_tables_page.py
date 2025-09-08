from dataclasses import dataclass
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@dataclass
class WebRecord:
    first_name: str
    last_name: str
    email: str
    age: int
    salary: int
    department: str

class WebTablesPage:
    URL = "https://demoqa.com/webtables"
    TIMEOUT = 15

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

    def _type(self, locator, text):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.clear()
        el.send_keys(text)

    def click_add(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton"))).click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "registration-form-modal")))

    def fill_form(self, rec: WebRecord):
        self._type((By.ID, "firstName"), rec.first_name)
        self._type((By.ID, "lastName"), rec.last_name)
        self._type((By.ID, "userEmail"), rec.email)
        self._type((By.ID, "age"), str(rec.age))
        self._type((By.ID, "salary"), str(rec.salary))
        self._type((By.ID, "department"), rec.department)

    def submit_form(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()
        self.wait.until(EC.invisibility_of_element_located((By.ID, "registration-form-modal")))

    def create_record(self, rec: WebRecord):
        self.click_add()
        self.fill_form(rec)
        self.submit_form()

    def search(self, term: str):
        box = self.wait.until(EC.element_to_be_clickable((By.ID, "searchBox")))
        box.send_keys(Keys.CONTROL, "a")
        box.send_keys(Keys.DELETE)
        box.send_keys(term)

    def clear_search(self):
        self.search("")

    def _email_cell(self, email: str):
        xpath = f"//div[@class='rt-td' and normalize-space(text())='{email}']"
        return self.driver.find_elements(By.XPATH, xpath)

    def row_exists_by_email(self, email: str) -> bool:
        self.search(email)
        self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, ".rt-noData, .rt-td"))
        return len(self._email_cell(email)) > 0

    def get_row_dict_by_email(self, email: str):
        self.search(email)
        self.wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, ".rt-noData, .rt-td"))
        cells = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'rt-tr') and @role='row']/div[@class='rt-td']"
        )
        if not cells:
            return {}
        cols = ["first_name", "last_name", "age", "email", "salary", "department", "action"]
        values = [c.text.strip() for c in cells[:len(cols)]]
        return dict(zip(cols, values))

    def edit_record_by_email(self, email: str, new: WebRecord):
        self.search(email)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Edit']"))).click()
        self.fill_form(new)
        self.submit_form()

    def delete_record_by_email(self, email: str):
        self.search(email)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Delete']"))).click()
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "rt-noData")))

    @staticmethod
    def random_record():
        fn = random.choice(["Mateus","Ana","Bruno","Livia","Paula","Lucas","Beatriz","Joao","Carla","Renan"])
        ln = random.choice(["Silva","Souza","Oliveira","Almeida","Gomes","Lima","Ribeiro","Pereira","Costa","Carvalho"])
        email = f"{fn.lower()}.{ln.lower()}{random.randint(100,999)}@example.com"
        age = random.randint(18, 60)
        salary = random.randint(1500, 15000)
        dept = random.choice(["Legal","Compliance","Insurance","Tech","Sales","HR"])
        return WebRecord(fn, ln, email, age, salary, dept)
