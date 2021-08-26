from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

class Elements():
    def __init__(self, driver, waitTime = 10):
        self.driver = driver.browser
        self.waitTime = waitTime

    def ByXpath(self, xpath):
        try:
            elements = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_all_elements_located((By.XPATH, xpath))
            )
            return elements
        except:
            return None

    def ByClassName(self, className):
        try:
            elements = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, className))
            )
            return elements
        except:
            return None

    def ByTagName(self, tagName):
        try:
            elements = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_all_elements_located((By.TAG_NAME, tagName))
            )
            return elements
        except:
            return None

class Element():
    def __init__(self, driver, waitTime = 10):
        self.driver = driver.browser
        self.waitTime = waitTime

    def ByXpath(self, xpath):
        try:
            element = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
            return ElementInteraction(element)
        except:
            return None

    def ByClassName(self, className):
        try:
            element = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_element_located((By.CLASS_NAME, className))
            )
            return ElementInteraction(element)
        except:
            return None

    def ByTagName(self, tagName):
        try:
            element = WebDriverWait(self.driver, self.waitTime).until(
                ec.presence_of_element_located((By.TAG_NAME, tagName))
            )
            return ElementInteraction(element)
        except:
            return None

class ElementInteraction():
    def __init__(self, element):
        self.element = element

    def find(self):
        return self.element

    def click(self):
        self.element.click()

    def double_click(self):
        self.element.click()
        self.element.click()

    def send_keys(self, key):
        self.element.send_keys(key)