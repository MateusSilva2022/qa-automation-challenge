import pytest
from pages.sortable_page import SortablePage

pytestmark = pytest.mark.e2e

def test_sortable_list_ascending_with_drag_and_drop(driver):
    p = SortablePage(driver)
    p.open()

    p.move_item_to_index("Six", 0)
    assert p.get_order()[0] == "Six"

    final_order = p.sort_ascending()
    assert final_order == ["One", "Two", "Three", "Four", "Five", "Six"]
