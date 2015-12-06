from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from tests.api import create_real_test_data
from tests.api import drop_all_product_lists, drop_all_products
from tests.base.rest_calls import PRODUCT_LISTS_API_ENDPOINT, PRODUCTS_API_ENDPOINT
from django.contrib.auth.models import User
import sys
import os


class FunctionalTest(StaticLiveServerTestCase):
    """
    Common functional test class which provides the ability to work against a remote server

    use attribute --liveserver=staging.ubuntu.local in with execution to test against a staging server
    """
    download_dir = ""

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split("=")[1]
                return
        # if no liveserver argument is given, a local test server is used
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.download_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "selenium_downloads")
        print("Selenium Download directory set to %s" % self.download_dir)

        for the_file in os.listdir(self.download_dir):
            file_path = os.path.join(self.download_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as ex:
                print("Failed to delete file, tests may also fail: %s" % ex)

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", self.download_dir)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


class DestructiveProductDbFunctionalTest(FunctionalTest):
    API_USERNAME = "api"
    API_PASSWORD = "api"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"

    def clean_db(self):
        """
        dropy any usage data form the system, use with care when testing again a live server
        :return:
        """
        drop_all_product_lists(server=self.server_url,
                           username=self.API_USERNAME,
                           password=self.API_PASSWORD)
        drop_all_products(server=self.server_url,
                       username=self.API_USERNAME,
                       password=self.API_PASSWORD)

    def create_test_data(self):
        base_path = os.path.join("tests", "data")
        test_data_paths = [
            os.path.join(base_path, "create_cisco_test_data.json"),
            os.path.join(base_path, "create_juniper_test_data.json"),
        ]

        create_real_test_data(server=self.server_url,
                              username=self.API_USERNAME,
                              password=self.API_PASSWORD,
                              test_data_paths=test_data_paths)

    def setUp(self):
        super().setUp()

        # create superuser
        u = User(username='admin')
        u.set_password('admin')
        u.is_superuser = True
        u.is_staff = True
        u.save()
        u = User(username='api')
        u.set_password('api')
        u.is_superuser = False
        u.is_staff = False
        u.save()

        self.clean_db()
        self.create_test_data()

        # set API endpoints
        self.PRODUCT_LIST_API_URL = self.server_url + PRODUCT_LISTS_API_ENDPOINT
        self.PRODUCT_LIST_BY_NAME_API_URL = self.server_url + PRODUCT_LISTS_API_ENDPOINT + "byname/"
        self.PRODUCT_API_URL = self.server_url + PRODUCTS_API_ENDPOINT
        self.PRODUCT_BY_NAME_API_URL = self.server_url + PRODUCTS_API_ENDPOINT + "byname/"

    def tearDown(self):
        super().tearDown()
