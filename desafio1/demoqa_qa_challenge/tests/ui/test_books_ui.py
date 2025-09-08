import pytest
from selenium.webdriver.support.ui import WebDriverWait
from src.ui.pages.books_page import BooksPage
from src.ui.pages.login_page import LoginPage

@pytest.mark.ui
def test_books_search_and_open(driver):
    page = BooksPage(driver)
    page.open()
    assert len(page.get_rows()) > 0
    page.search("JavaScript")
    assert len(page.get_rows()) >= 1
    page.open_first_book()
    WebDriverWait(driver, 10).until(lambda d: "/books?book=" in d.current_url)
    assert "/books?book=" in driver.current_url

@pytest.mark.ui
def test_login_negative_message(driver):
    lp = LoginPage(driver)
    lp.open()
    lp.login("usuario_invalido", "senha_errada")
    msg = lp.error_text(timeout=12)
    assert "/login" in driver.current_url
    assert "Invalid username or password!" in msg
