import atexit

import structlog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options


class BrowserRunner:
    def __init__(self):
        self.browsers = {
            'chrome': webdriver.Chrome,
            'firefox': webdriver.Firefox
        }
        self.browser = None
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='webdriver')
        atexit.register(self.stop)

    def _start_local(self, browser_name, headless=False):
        browser_cap = self.browsers.get(browser_name)
        if not browser_cap:
            raise Exception(
                f'No capabilities found for {browser_name}. Please use one of {self.browsers.keys()}'
            )

        if browser_name == 'chrome':
            options = chrome_options()
            options.add_argument('--dns-prefetch-disable')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--ignore-certificate-errors')

            if headless:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')

            self.browser = browser_cap(options=options)

    def start(self, browser_name='chrome', headless=False):
        self.log.info('start browser')
        if self.is_running():
            return self.browser

        self._start_local(browser_name, headless)

    def open(self, host='', browser_name='chrome', headless=False):
        if not self.browser:
            self.log.info(f'open {host}')
            self.start(browser_name=browser_name, headless=headless)
            self.browser.get(host)

    def stop(self):
        if self.browser:
            self.log.info('quit browser')
            self.browser.quit()
            self.browser = None

    def is_running(self):
        return bool(self.browser)
