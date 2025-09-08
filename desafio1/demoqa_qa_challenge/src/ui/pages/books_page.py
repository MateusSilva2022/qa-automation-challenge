from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from .base_page import BasePage

class BooksPage(BasePage):
    URL = "https://demoqa.com/books"
    SEARCH = (By.ID, "searchBox")
    ROWS = (By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
    TITLE_LINKS = (By.CSS_SELECTOR, "div.action-buttons a")

    def open(self):
        self.visit(self.URL)
        self.remove_ads()

    def search(self, text: str):
        self.wait_visible(*self.SEARCH)
        self.find(*self.SEARCH).clear()
        self.find(*self.SEARCH).send_keys(text)

    def get_rows(self):
        return self.finds(*self.ROWS)

    def open_first_book(self):
        self.wait_visible(*self.ROWS)
        link = self.finds(*self.TITLE_LINKS)[0]
        self.scroll_into_view(link)
        try:
            self.wait_clickable(*self.TITLE_LINKS)
            link.click()
        except ElementClickInterceptedException:
            try:
                self.js_click(link)
            except Exception:
                href = link.get_attribute("href")
                self.driver.get(href)
