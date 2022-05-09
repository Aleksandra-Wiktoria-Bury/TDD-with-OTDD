from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://localhost:8000')


# an assertion is a predicate connected to a point in the program, that always should evaluate to true at that point in code execution
# checks for the default Django "it worked" page
assert 'Django' in browser.title