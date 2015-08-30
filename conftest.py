import pytest
from allauth.socialaccount.models import SocialApp
from socialee.utils.urls import is_absolute_url


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
        help="run slow tests")

def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")

@pytest.fixture
def socialauth():
    "Create (fake) SocialApp account for Facebook (dev)"
    # Use env vars for this, once it needs to be a real app/account.
    sapp, created = SocialApp.objects.get_or_create(provider=u'facebook',
        name='fb1', client_id='CLIENT_ID',
        secret='SECRET')
    sapp.save()
    sapp.sites.add(1)

@pytest.yield_fixture
def browser(browser, request, live_server, socialauth):
    """
    Provide a browser fixture via pytest-splinter's browser.

    It injects my_base_url (via --liveserveroverride) into its visit method.

    :type browser: Browser
    """
    b = browser
    b._live_server = live_server

    # Inject live_server.my_base_url into `visit`.
    _visit = b.visit

    def visit(url):
        if not is_absolute_url(url):
            url = live_server.url + url
        return _visit(url)
    b.visit = visit


    # Source:
    # http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html#comment-1998325550
    import contextlib
    # from selenium.webdriver import Remote
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.expected_conditions import staleness_of

    @contextlib.contextmanager
    def wait_for_page_load(timeout=30):
        old_page = b.driver.find_element_by_tag_name('html')

        yield

        class JavascriptError(Exception):
            pass

        def staleness_of_old_page_or_js_error(driver):
            # typeof("window.JSErrors") !== undefined and
            js_errors = b.evaluate_script('window.JSErrors')
            if js_errors:
                raise JavascriptError(
                    "A JavaScript error occurred at {}: {}".format(
                        driver.current_url, js_errors)
                )
                # pytest.fail()
            return staleness_of(old_page)

        WebDriverWait(b.driver, timeout).until(
            staleness_of_old_page_or_js_error)
    b.wait_for_page_load = wait_for_page_load

    yield b
