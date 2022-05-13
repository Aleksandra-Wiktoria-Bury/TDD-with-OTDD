from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#! standard library with common tests - class unittest.TestCase:
import unittest

class NewVisitorTest (unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # user checks the homepage
        self.browser.get('http://localhost:8000')
        
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
        #! explicit wait:
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy new carpet', [row.text for row in rows])
        self.assertIn('2: Mount the lamp', [row.text for row in rows])


        # input form for adding a new task is still present, user enters another task

        # upon page update, 2 tasks are displayed

        # will the results be stored? There should be a custom generated URL

        # user visits that URL - her to-do list is still there.
        self.fail('Finish the test!')
        # all achieved!
if __name__ == '__main__':  
    unittest.main()