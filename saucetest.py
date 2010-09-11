from django.utils.simplejson import dumps
from selenium import selenium
import settings
import unittest

class TestSauceWithAppEngine(unittest.TestCase):
    def setUp(self):
        self.browser = selenium(
            "saucelabs.com",
            4444,
            dumps({'username': settings.sauce_username,
                   'access-key': settings.sauce_accesskey,
                   'os': "Windows 2003",
                   'browser': "iexplore",
                   'browser-version': "7.",
                   'job-name': self.__class__.__name__,
                   'record-video': True}),
            'http://saucelabsdemo.appspot.com')
        self.browser.start()

    def test_login(self):
        browser = self.browser 
        browser.open('http://saucelabsdemo.appspot.com')
        browser.open('http://google.com')
        #self.assertEquals(1 == 1)
        #browser.wait_for_page_to_load(10000)
        #browser.type('q', 'Selenium Testing')
        #browser.click('btnG')

    def tearDown(self):
        self.browser.stop()
