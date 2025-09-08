import os, sys, pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    headless = os.getenv("HEADLESS", "1") != "0"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")   
    else:
        options.add_argument("--start-maximized")         

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

  
    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)

    if not headless:
        try:
            d.maximize_window()  
        except Exception:
            pass

    yield d
    d.quit()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "driver" in item.fixturenames:
        driver = item.funcargs["driver"]
        os.makedirs("reports/screenshots", exist_ok=True)
        fname = os.path.join("reports", "screenshots", f"{item.name}.png")
        try:
            driver.save_screenshot(fname)
            print(f"\n[Screenshot salvo] {fname}")
        except Exception as e:
            print(f"\n[WARN] Não foi possível salvar screenshot: {e}")

