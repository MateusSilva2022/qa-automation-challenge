import pytest
from pages.web_tables_page import WebTablesPage

pytestmark = pytest.mark.e2e

def test_create_edit_delete_single_record(driver):
    page = WebTablesPage(driver)
    page.open()

    rec = WebTablesPage.random_record()
    page.create_record(rec)
    assert page.row_exists_by_email(rec.email), "registro não apareceu na tabela"

    edited = WebTablesPage.random_record()
    edited.first_name, edited.last_name, edited.email = rec.first_name, rec.last_name, rec.email
    edited.department = "Tech"
    edited.salary = 9999
    page.edit_record_by_email(rec.email, edited)

    row = page.get_row_dict_by_email(rec.email)
    assert row.get("department") == "Tech"
    assert row.get("salary") == "9999"

    page.delete_record_by_email(rec.email)
    assert not page.row_exists_by_email(rec.email)

def test_bulk_create_12_and_delete_them(driver):
    page = WebTablesPage(driver)
    page.open()

    emails = []
    for _ in range(12):
        rec = WebTablesPage.random_record()
        emails.append(rec.email)
        page.create_record(rec)

    assert all(page.row_exists_by_email(e) for e in emails)

    for e in emails:
        page.delete_record_by_email(e)

    assert all(not page.row_exists_by_email(e) for e in emails)
