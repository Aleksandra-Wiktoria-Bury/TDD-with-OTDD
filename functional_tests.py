from selenium import webdriver

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
        
        #? an assertion is a predicate connected to a point in the program, that always should evaluate to true at that point in code execution
        # user checks for the page title & header - 'To-Do' 
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        # user can enter a to-do item straight away
        # # user types the task

        # after submitting with 'enter' a new task is displayed

        # input form for adding a new task is still present, user enters another task

        # upon page update, 2 tasks are displayed

        # will the results be stored? There should be a custom generated URL

        # user visits that URL - her to-do list is still there.

        # all achieved!
if __name__ == '__main__':  
    unittest.main()