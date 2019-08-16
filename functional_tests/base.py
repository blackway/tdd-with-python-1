import sys
from contextlib import contextmanager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        # self.browser = webdriver.Chrome(
            # "C:/dev/works/django/TDD-with-python2/tdd-with-python-1/utils/chromedriver_win32/chromedriver.exe"
        # )
        # fp = webdriver.FirefoxProfile
        executable_path = "C:/dev/works/django/TDD-with-python2/tdd-with-python-1/utils/geckodriver-v0.24.0-win64/geckodriver.exe"
        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')        
        self.browser = webdriver.Firefox(executable_path=executable_path)
        # self.browser = webdriver.Firefox(executable_path=executable_path)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
