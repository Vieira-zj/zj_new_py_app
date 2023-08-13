# coding=utf-8
'''
Created on 2018-10-30
@author: zhengjin

Includes unit test and selenium web ui test demo by "unittest" module.
'''

import os
import threading
import time
import unittest

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as cond
from selenium.webdriver.support.ui import WebDriverWait

# --------------------------------------------------------------
# Unit Test
# --------------------------------------------------------------


class TestPy01(unittest.TestCase):
    '''
    unit test.
    '''

    def test_subprocess(self):

        def subprocess_main():
            for i in range(3):
                print('test and wait at %d' % i)
                time.sleep(1)

        t = threading.Thread(target=subprocess_main)
        t.start()
        print('in main thread and wait\n')
        t.join()

    def test_time_counter(self):
        now = time.perf_counter()
        time.sleep(3)
        during = time.perf_counter() - now
        print('during %.3f' % during)
        self.assertEqual(3, int(round(during)), 'test time counter')

    def test_reg_expr(self):
        import re
        test_str = 'list: device offline'
        self.assertTrue(re.search(
            'unknown|offline', test_str), 'search success')
        self.assertFalse(re.search(
            'unknown|online', test_str), 'search failed')


# --------------------------------------------------------------
# Webdriver Test
# --------------------------------------------------------------


class TestWebdriver01(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_gitlab_with_google_login(self):
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }
        browser = webdriver.Chrome(desired_capabilities=caps)
        browser.implicitly_wait(8)

        executor_url = browser.command_executor._url
        session_id = browser.session_id

        url = "https://git.xxxxx.com/project/service"
        browser.get(url)
        print("\nexecutor_url:", executor_url)
        print("session_id:", session_id)

        # select google login
        login_btn = browser.find_element_by_partial_link_text("Google")
        login_btn.click()

        # input email and next
        id_input = browser.find_element_by_css_selector("input#identifierId")
        id_input.send_keys("jin.zheng@xxxxx.com")
        id_next_btn = browser.find_element_by_css_selector(
            "#identifierNext button")
        id_next_btn.click()

        # reuse pre webdriver session
        # refer to: https://web.archive.org/web/20171129014322/http://tarunlalwani.com/post/reusing-existing-browser-session-selenium/
        browser2 = webdriver.Remote(
            command_executor=executor_url, desired_capabilities={})
        browser2.session_id = session_id
        print("current url:", browser2.current_url)

        # input password and next
        password_input = browser2.find_element_by_css_selector(
            "#password input")
        password_input.send_keys("xxxxx")
        pwd_next_btn = browser.find_element_by_css_selector(
            "#passwordNext button")
        print(pwd_next_btn.is_displayed())
        # pwd_next_btn.click()

        # TODO: input google dyn code
        time.sleep(3)
        browser2.quit()


class TestWebdriver02(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_wd_attach_to_existing_chrome(self):
        '''
        pre-conditions: start chrome with remote debug port

        $ cd /Applications/Google\\ Chrome.app/Contents/MacOS
        $ ./Google\\ Chrome --remote-debugging-port=17890
        '''

        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }

        br_options = ChromeOptions()
        br_options.add_experimental_option(
            "debuggerAddress", "localhost:17890")

        browser = webdriver.Chrome(
            desired_capabilities=caps, options=br_options)
        browser.implicitly_wait(8)
        print("attach to browser with debugger addr:",
              br_options.experimental_options)

        url = "https://confluence.xxxxxx.io/pages/viewpage.action?pageId=123456"
        browser.get(url)
        print("page title:", browser.title)
        print("cookies:", browser.get_cookies())

        try:
            login_btn = browser.find_element_by_partial_link_text("Google")
            print("google login display:", login_btn.is_displayed())
            login_btn.click()
        except Exception as e:
            print(e)
            print("login direct.")


# --------------------------------------------------------------
# Selenium Web UI Test
# --------------------------------------------------------------


class TestWebUI01(unittest.TestCase):
    '''
    selenium web ui test.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utils = TestUtils()
        self.ms_bing_page = MsBingPage()

    def test_selenium_chrome(self):
        '''
        selenium ui test with headless mode in local (chrome).

        pre-condition:
        pip3 install chromedriver-binary==84.0.4147.30.0
        '''
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }
        br_options = ChromeOptions()
        br_options.add_argument('--headless')
        br_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(
            desired_capabilities=caps, options=br_options)
        browser.implicitly_wait(8)

        print('\nbrowser: %s, version: %s' % (
            browser.capabilities['browserName'], browser.capabilities['browserVersion']))
        try:
            self.ms_bing_page.open_steps(self, browser)
        finally:
            browser.quit()

    def test_selenium_grid_headless_chrome(self):
        '''
        selenium ui test with headless mode by grid, and vnc record is disabled (chrome).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        br_options = ChromeOptions()
        br_options.add_argument('--headless')
        br_options.add_argument('--disable-gpu')

        caps = DesiredCapabilities.CHROME
        caps['platform'] = 'ANY'
        caps.update(br_options.to_capabilities())

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('browserName', 'null'), b_caps.get('version', 'null')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.utils.save_screenshot(browser, '/tmp/uitest_bing_home_01.png')
            self.ms_bing_page.search_steps(self, browser)
            self.utils.save_screenshot(
                browser, '/tmp/uitest_bing_search_01.png')
        finally:
            browser.quit()

    def test_selenium_grid_headless_firefox(self):
        '''
        selenium ui test with headless mode by grid, and vnc record is disabled (firefox).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        br_options = FirefoxOptions()
        br_options.headless = True

        caps = DesiredCapabilities.FIREFOX
        caps['platform'] = 'ANY'
        caps.update(br_options.to_capabilities())

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('browserName', 'unknown'), b_caps.get('version', 'unknown')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.utils.save_screenshot(browser, '/tmp/uitest_bing_home_02.png')
            self.ms_bing_page.search_steps(self, browser)
            self.utils.save_screenshot(
                browser, '/tmp/uitest_bing_search_02.png')
        finally:
            browser.quit()

    def test_selenium_grid_vnc_debug(self):
        '''
        selenium ui test by grid, and vnc record is enabled (chrome).

        pre-condition: selenium grid is running.
        check selenium hub: curl "http://localhost:4444/wd/hub/status" | jq .
        '''
        caps = DesiredCapabilities.CHROME
        caps['platform'] = 'ANY'

        hub_url = 'http://localhost:4444/wd/hub'
        browser = webdriver.Remote(
            command_executor=hub_url, desired_capabilities=caps)
        browser.implicitly_wait(8)

        b_caps = browser.capabilities
        print('\nbrowser: %s, version: %s' %
              (b_caps.get('version', 'unknown'), b_caps.get('browserName', 'unknown')))
        try:
            self.ms_bing_page.open_steps(self, browser)
            self.ms_bing_page.search_steps(self, browser)
        finally:
            browser.quit()


class TestWebUI02(unittest.TestCase):
    """
    去哪儿网首页 输入出发城市和日期
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_qunar_home_page_input(self):
        caps = {
            'browserName': 'chrome',
            'version': '',
            'platform': 'MAC',
            'javascriptEnabled': True,
        }
        browser = webdriver.Chrome(desired_capabilities=caps)
        browser.implicitly_wait(8)

        url = 'https://www.qunar.com/'
        browser.get(url)

        # 输入出发城市
        inputFromCity = browser.find_element_by_name('fromCity')
        inputFromCity.click()
        time.sleep(1)
        browser.find_element_by_css_selector('a[data-code=WUH]').click()

        # 输入出发日期
        inputFromDate = browser.find_element_by_name('fromDate')
        inputFromDate.click()
        time.sleep(1)
        inputFromDate.send_keys(Keys.COMMAND, 'a')
        inputFromDate.send_keys(Keys.DELETE)
        time.sleep(1)
        inputFromDate.send_keys('2020-12-11')
        inputFromDate.click()
        time.sleep(3)


# --------------------------------------------------------------
# UI Test Steps
# --------------------------------------------------------------


class MsBingPage(object):
    '''
    ms bing search home page.
    '''

    def open_steps(self, t, browser):
        open_url = 'https://cn.bing.com/'
        browser.get(open_url)
        print('page title:', browser.title)
        t.assertTrue('Bing' in browser.title, 'verify ms bing page title')

        en_tab = WebDriverWait(browser, 5, 0.5).until(
            cond.presence_of_element_located((By.ID, 'est_en')))
        print('en tab element text:', en_tab.text)
        t.assertTrue('国际版' in en_tab.text, 'verify en tab element text')
        en_tab.click()
        time.sleep(1)

    def search_steps(self, t, browser):
        input = browser.find_element_by_id('sb_form_q')
        t.assertIsNotNone(input, 'verify input element is exist')
        input.send_keys('docker selenium')
        input.submit()
        time.sleep(2)


class TestUtils(object):
    '''
    test utils.
    '''

    def __init__(self):
        self.is_screenshot = False

    def save_screenshot(self, browser, path):
        if not self.is_screenshot:
            return

        if os.path.exists(path):
            os.remove(path)
        browser.save_screenshot(path)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main(verbosity=2)

    tests = []
    # unit test
    # tests.append(TestPy01('test_subprocess'))
    # tests.append(TestPy01('test_time_counter'))
    # tests.append(TestPy01('test_reg_expr'))

    # webdriver test
    # tests.append(TestWebdriver01('test_gitlab_with_google_login'))
    # tests.append(TestWebdriver02('test_wd_attach_to_existing_chrome'))

    # web ui test
    # tests.append(TestWebUI01('test_selenium_chrome'))
    # tests.append(TestWebUI01('test_selenium_grid_headless_chrome'))
    # tests.append(TestWebUI01('test_selenium_grid_headless_firefox'))
    # tests.append(TestWebUI01('test_selenium_grid_vnc_debug'))

    tests.append(TestWebUI02('test_qunar_home_page_input'))

    suite = unittest.TestSuite()
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
