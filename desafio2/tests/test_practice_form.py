import os, pytest
from pages.practice_form_page import PracticeFormPage
from utils.data import random_person

pytestmark = pytest.mark.e2e

def test_fill_and_submit_practice_form(driver):
    person = random_person()
    page = PracticeFormPage(driver)
    page.open()

    page.type_first_name(person.first_name)
    page.type_last_name(person.last_name)
    page.type_email(person.email)
    page.choose_gender(person.gender)
    page.type_mobile(person.mobile)

    page.set_birthdate(person.birth_day, person.birth_month_idx, person.birth_year)
    page.add_subjects(person.subjects)
    page.choose_hobbies(person.hobbies)

    upload_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "upload.txt"))
    page.upload_file(upload_path)

    page.type_address(person.address)
    page.choose_state_city(person.state, person.city)

    page.submit()
    page.assert_modal_open()

    modal = page.get_modal_dict()
    assert modal["Student Name"] == f"{person.first_name} {person.last_name}"
    assert modal["Student Email"] == person.email
    assert modal["Gender"] == person.gender
    assert modal["Mobile"] == person.mobile
    for s in person.subjects: assert s in modal["Subjects"]
    for h in person.hobbies: assert h in modal["Hobbies"]
    assert person.address in modal["Address"]
    assert f"{person.state} {person.city}" in modal["State and City"]

    page.close_modal()

