import os, sys
from dotenv import load_dotenv
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://demoqa.com")

                   
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def browser_name():
    return os.getenv("BROWSER", "chrome").lower()

@pytest.fixture(scope="session")
def headless():
    return os.getenv("HEADLESS", "true").lower() == "true"

@pytest.fixture(scope="session")
def driver(browser_name, headless):
    if browser_name != "chrome":
        raise RuntimeError("Somente Chrome configurado.")
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1600,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = ChromeService(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    yield d
    d.quit()
