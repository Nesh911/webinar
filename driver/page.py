import time

from selenium.common.exceptions import (ElementNotVisibleException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    """
    Base class for all Pages
    """
    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout

    @property
    def url(self):
        return self.driver.current_url

    def refresh(self):
        return self.driver.refresh()

    def wait_for_no_alert(self, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present(), message='No alert'
            )
            alert = self.driver.switch_to_alert()
            alert.accept()
            return False
        except TimeoutException:
            return True

    def get_element(self, locator):
        return self.driver.find_element(*locator)

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def get_select(self, locator):
        return Select(self.driver.find_element(*locator))

    def select_by_index(self, locator, index):
        index = int(index)

        select = Select(self.driver.find_element(*locator))

        select.select_by_index(index)

        return select

    def select_last_index(self, locator):
        select = Select(self.driver.find_element(*locator))

        select.select_by_index(len(select.options) - 1)

        return select

    def is_element_present(self, locator):
        self.driver.implicitly_wait(0)
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.driver.implicitly_wait(self.timeout)

    def is_element_visible(self, locator):
        self.driver.implicitly_wait(0)
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except (NoSuchElementException, ElementNotVisibleException, StaleElementReferenceException):
            return False
        finally:
            # set back to where you once belonged
            self.driver.implicitly_wait(self.timeout)

    def wait_for_element_visible(self, locator):
        """
        Waits for element will be visible for timings.default

        Args:
            locator: webdriver locator of the element
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator),
            message='Element %s %s either is not present or invisible' % locator)

    def wait_for_element_not_visible(self, locator):
        """
        Waits for element will be not visible for timings.default

        Args:
            locator: webdriver locator of the element
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located(locator),
            message='Element %s %s is visible' % locator)

    def wait_for_element_present(self, locator):
        """
        Waits for element will be present for timings.default

        Args:
            locator: webdriver locator of the element
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator),
            message='Element %s %s is not present in DOM' % locator)

    def wait_for_element_clickable(self, locator):
        """
        Waits for element will be clickable for timings.default

        Args:
            locator: webdriver locator of the element
        """
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator),
            message='Element %s %s is not clickable' % locator)

    def wait_ajax(self):
        """Awaiting ajax"""
        while self.driver.execute_script('return document.readyState') != 'complete':
            time.sleep(0.5)

    def wait_for_page_load_complete(self):
        WebDriverWait(self.driver, self.timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def wait_for_number_of_windows(self, value):
        """
        Waits until condition evaluate to value

        Args:
            value: value of the parameter
        """
        WebDriverWait(self.driver, self.timeout).until(lambda driver: len(driver.window_handles) == value,
                                                       message='{} is not equal to {}')

    def move_to_element(self, locator):
        """
        Scroll page to the element

        Args:
            locator: webdriver locator of the element
        """
        self.driver.execute_script('arguments[0].scrollIntoView(true);', self.get_element(locator))

    def move_to_element_up_scroll(self, locator):
        """
        Scroll page to the element

        Args:
            locator: webdriver locator of the element

        window.scrollBy(0, -200) is used to scroll page up to prevent overlaying element
        by sticked header
        """
        self.move_to_element(locator)
        self.driver.execute_script('window.scrollBy(0, -200);')

    def scroll_to_top(self):
        """
        Scroll page to the top of the page
        """
        self.driver.execute_script('window.scrollTo(0, 0)')

    def scroll_to_bottom(self):
        """
        Scroll page to the bottom of the page
        """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def get_scroll_top(self):
        """
        Scroll page to the bottom of the page
        """
        return self.driver.execute_script('return '
                                          'window.pageYOffset||document.documentElement.scrollTop||document.body'
                                          '.scrollTop||0')

    def set_border(self, locator):
        """
        Set 3px solid red border around element

        Args:
            locator: webdriver locator of the element
        """
        self.driver.execute_script("arguments[0].style.border='2px dashed red'", self.get_element(locator))

    def click(self, locator):
        self.wait_for_element_clickable(locator)
        element = self.get_element(locator)
        self.set_border(locator)
        self.click_on_element(element)

    def click_on_element(self, element):
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.click(element)
        action.perform()

    def set(self, locator, text):
        """
        Send keys to the input

        Args:
            locator: webdriver locator of the element
            text: text to set
        """
        element = self.get_element(locator)
        self.set_border(locator)
        element.send_keys(text)

    def js_click(self, locator):
        """
        Cheat, don't use in test if possible

        Args:
            locator: webdriver locator of the element
        """
        self.driver.execute_script('arguments[0].click();', self.get_element(locator))

    def get_xpath(self, locator):
        """
        Get element's XPATH
        Args:
            locator: webdriver locator of the element

        Returns:
            Element's xpath
        """
        return '//' + self.driver.execute_script('gPt=function(c){if(c===document.body){return c.tagName}var a=0;'
                                                 'var e=c.parentNode.childNodes;for(var b=0;b<e.length;b++){var d=e[b];'
                                                 "if(d===c){return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'}"
                                                 'if(d.nodeType===1&&d.tagName===c.tagName){a++}}};'
                                                 'return gPt(arguments[0]).toLowerCase();', self.get_element(locator))

    def get_domain(self):
        """Get protocol from config and domain and return url
        """
        return self.driver.execute_script('return location.protocol') + '//' + self.driver.execute_script('return location.hostname') + '/'
