from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):

        self.executable_path_firefox = "C:/dev/works/django/TDD-with-python2/tdd-with-python-1/utils/geckodriver-v0.24.0-win64/geckodriver.exe"

        # Edith has heard about a cool new online to-do app.
        # She goes to check out its hompage.
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Input your items here'
        )

        # She types "Buy peacock feathers" into a text box.
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table("1: Buy peacock feathers")
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly".
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list.
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table("1: Buy peacock feathers")
            self.check_for_row_in_list_table(
                "2: Use peacock feathers to make a fly"
            )

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is comming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path=self.executable_path_firefox)

        # Francis visits the home page. There is no sign of Edith's list.
        self.browser.get(self.server_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(edith_list_url, francis_list_url)

        # Again, there is no trace of Edith's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.
