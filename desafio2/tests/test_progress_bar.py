import pytest
from pages.progress_bar_page import ProgressBarPage

pytestmark = pytest.mark.e2e

def test_progress_bar_stop_before_25_and_reset(driver):
    p = ProgressBarPage(driver)
    p.open()

 
    val = p.stop_near(target=25, tolerance=7)  
    assert val <= 25, f"Progress bar parou em {val}%, deveria ser <= 25%"

    p.start()
    p.wait_until_100()
    assert p.get_value() == 100

    p.reset()
    p.wait_until_zero()
    assert p.get_value() == 0

