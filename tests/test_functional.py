from django.core.urlresolvers import reverse

from selenium.webdriver.support.ui import WebDriverWait
from socialee.models import UserEntry


def test_signup_on_home(browser, live_server, socialauth, settings):
    browser.visit(reverse("home"))
    submit_text = "ab die Post!"
    browser.click_link_by_text(submit_text)

    email_errorlist = browser.find_by_xpath("//input[@id='id_email']"
                                            "/following-sibling::ul[@class='errorlist']")
    assert len(email_errorlist) == 1
    assert email_errorlist[0].text == "Dieses Feld ist zwingend erforderlich."

    browser.fill("email", "user@example.com")
    browser.click_link_by_text(submit_text)
    assert "Bestätige deine E-Mail-Adresse" in browser.html

    assert UserEntry.objects.get(email="user@example.com")


def test_signup_on_home_complete(browser, live_server, socialauth, settings):
    browser.visit(reverse("home"))
    submit_text = "ab die Post!"

    next_button = browser.find_by_id("questionnavright")
    def click_and_is_scrolled_off(x, name):
        next_button.click()
        return not x.find_element_by_name(name).is_displayed()

    def fill_and_click_to_next(name, text):
        browser.fill(name, text)
        WebDriverWait(browser.driver, 10).until(
            lambda x: click_and_is_scrolled_off(x, name))

    fill_and_click_to_next("output_title", "Output")
    fill_and_click_to_next("input_title", "Input")
    browser.fill("project_title", "Projekt")

    browser.fill("email", "user@example.com")
    browser.click_link_by_text(submit_text)
    assert "Bestätige deine E-Mail-Adresse" in browser.html

    user = UserEntry.objects.get(email="user@example.com")
    profile = user.profile

    assert profile.project_set.count() == 1
    assert profile.project_set.first().title == "Projekt"

    assert profile.input_set.count() == 1
    assert profile.input_set.first().title == "Input"

    assert profile.output_set.count() == 1
    assert profile.output_set.first().title == "Output"
