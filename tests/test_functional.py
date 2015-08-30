from django.core.urlresolvers import reverse


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
