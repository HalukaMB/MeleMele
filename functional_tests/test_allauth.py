# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate


class TestGoogleLogin(StaticLiveServerTestCase):
    fixtures = ['allauth_fixture']
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        print("hey")
        activate('en')

    def tearDown(self):
        self.browser.quit()

    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.ID, element_id)))

    def get_element_by_tag(self, element_tag):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.TAG_NAME, element_tag)))

    def get_element_by_xpath(self, xpath):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.XPATH, xpath)))

    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                (By.ID, element_id)))

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def user_login(self):
        import json
        with open("taskbuster/fixtures/google_user.json") as f:
            credentials = json.loads(f.read())
        print("calling json")
        print(credentials["Email"])
        self.get_element_by_id("identifierId").send_keys(credentials["Email"])
        self.get_button_by_id("identifierNext").click()
        print(credentials["Passwd"])

        inputE = self.get_element_by_tag('input')
        print(inputE)
        #passwordE = self.get_element_by_tag('password')
        #print(passwordE)
        #self.get_element_by_tag('input').send_keys(credentials["Passwd"])

        #e=self.get_element_by_xpath('//*[@id="password"]/div/div/div')
        #print(e)
        inputE.send_keys(credentials["Passwd"])
        self.get_button_by_id("passwordNext").click()
        button = self.get_button_by_id("passwordNext")
        print(button)
        print("done?")
        #for btn in ["signIn", "submit_approve_access"]:
        #    self.get_button_by_id(btn).click()
        return

    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        google_login.click()
        self.user_login()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")
