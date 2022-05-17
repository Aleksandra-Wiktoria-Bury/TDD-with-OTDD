# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
class NewVisitorTest (StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # helper method:
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try: 
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # user checks the homepage
        self.browser.get(self.live_server_url)
        
        # user checks for the page title & header - 'To-Do' 
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # user can enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # user types the task: "Buy new carpet"
        inputbox.send_keys('Buy new carpet')

        # after submitting with 'enter' a new task is displayed
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy new carpet')

        # input form for adding a new task is still present, user enters another task
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Mount the lamp')
        inputbox.send_keys(Keys.ENTER)


        # upon page update, 2 tasks are displayed
        self.wait_for_row_in_list_table('1. Buy new carpet')
        self.wait_for_row_in_list_table('2. Mount the lamp')

    def test_multiple_users_can_start_lists_with_diff_URL(self):

        # userA starts a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy new carpet')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy new carpet')

        # will the results be stored? There should be a custom generated URL
        userA_list_URL = self.browser.current_url
        self.assertRegex(userA_list_URL, '/lists/.+')

        ##! new user visits - use new browser to make sure no info i.e. through cookies is present
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # userB visits page, there's no trace of userA list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new carpet', page_text)
        self.assertNotIn('Mount the lamp', page_text)

        # userB starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy milk')

        # userB gets own URL
        userB_list_URL = self.browser.current_url
        self.assertRegex(userB_list_URL, '/lists/.+')
        self.assertNotEqual(userA_list_URL, userB_list_URL)

        # again no trace of userA list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy new carpet', page_text)
        self.assertIn('Buy milk', page_text)

        # user visits that URL - her to-do list is still there.

        # all achieved!
    def test_layout_and_styling(self):

        # user goes to the webpage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width']/2, 512, delta = 5)

#if __name__ == '__main__':  
#    unittest.main()