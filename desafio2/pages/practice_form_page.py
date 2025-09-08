from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class PracticeFormPage:
    URL = "https://demoqa.com/automation-practice-form"
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

    def type_first_name(self, text): self._type((By.ID, "firstName"), text)
    def type_last_name(self, text): self._type((By.ID, "lastName"), text)
    def type_email(self, text): self._type((By.ID, "userEmail"), text)
    def choose_gender(self, label):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[contains(@for,'gender') and text()='{label}']"))).click()
    def type_mobile(self, text): self._type((By.ID, "userNumber"), text)

    def set_birthdate(self, day: int, month_idx: int, year: int):
        self.wait.until(EC.element_to_be_clickable((By.ID, "dateOfBirthInput"))).click()
        Select(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__month-select")))).select_by_index(month_idx)
        Select(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__year-select")))).select_by_value(str(year))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'react-datepicker__day') and not(contains(@class,'outside-month')) and text()='{day}']"))).click()

    def add_subjects(self, subjects):
        inp = self.wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
        for s in subjects:
            inp.send_keys(s)
            inp.send_keys(Keys.ENTER)

    def choose_hobbies(self, hobbies):
        for h in hobbies:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[contains(@for,'hobbies') and text()='{h}']"))).click()

    def upload_file(self, path: str):
        self.wait.until(EC.presence_of_element_located((By.ID, "uploadPicture"))).send_keys(path)

    def type_address(self, text): self._type((By.ID, "currentAddress"), text)

    def choose_state_city(self, state: str, city: str):
        self.wait.until(EC.element_to_be_clickable((By.ID, "state"))).click()
        si = self.wait.until(EC.presence_of_element_located((By.ID, "react-select-3-input")))
        si.send_keys(state); si.send_keys(Keys.ENTER)
        self.wait.until(EC.element_to_be_clickable((By.ID, "city"))).click()
        ci = self.wait.until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
        ci.send_keys(city); ci.send_keys(Keys.ENTER)

    def submit(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()

    def assert_modal_open(self):
        title = self.wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
        assert "Thanks for submitting the form" in title.text

    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "closeLargeModal"))).click()

    def get_modal_rows(self):
        return self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".modal-content table tbody tr")
        ))

    def get_modal_dict(self):
        data = {}
        for r in self.get_modal_rows():
            cols = r.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 2:
                label = cols[0].text.strip()
                value = cols[1].text.strip()
                data[label] = value
        return data

