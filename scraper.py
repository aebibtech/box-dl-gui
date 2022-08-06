# Box.com PDF Downloader
# Copyright (C) 2018 lfasmpao
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import platform
import re
import sys
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def url_checker(url):
    """
       This checks the url format
       :param url Unified Resource Locator
       :rtype: bool
       :return boolean
    """
    url_check_regex = re.compile(r"https:\/\/(.*).box.com\/(.*)")  # url check regex
    if re.match(url_check_regex, url) is not None:
        # return "box.com" in url  # really?
        return True


class Scraper:
    def __init__(self, url, driver_location=None, use_x11=False, wait_time=None):
        """
        This starts a selenium session
        :param url box.com url
        :type url string
        :param driver_location chrome driver path
        :type driver_location string
        """

        chrome_options = Options()
        if use_x11:
            # use x11 to hide chrome session
            if platform.system() == "Linux":
                self.display = Display(visible=0, size=(800, 600))
                self.display.start()  # start new virtual display
            if platform.system() == "Darwin":  # for OSX which I am using
                from easyprocess import EasyProcessCheckInstalledError # only darwin
                try:
                    self.display = Display(visible=0, size=(800, 600))
                    self.display.start()  # start new virtual display
                except EasyProcessCheckInstalledError:
                    print("Install XQuartz from here http://xQuartz.org and try again")
                    sys.exit(-1)
        else:
            # hide session using chrome headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1280x800")

        self.wait_load_time = wait_time
        self.use_x11 = use_x11
        self.driver_location = driver_location or "/usr/local/bin/chromedriver"
        self.url = url
        self.driver_obj = webdriver.Chrome(self.driver_location, chrome_options=chrome_options)

    def load_url(self):
        """
        This will load the url on the selenium driver
        """
        driver = self.driver_obj
        url = self.url
        driver.get(url)  # load selenium
        # TODO: This is a bad, maybe we should change this to selenium WebDriverWait
        time.sleep(self.wait_load_time)  # wait load time, implicit wait doesnt work well?

    def get_download_title(self):
        """
        This parses box.com title
        :rtype: string
        :return download title
        """
        driver = self.driver_obj
        title = str(driver.title).split("|")[0][:-1]
        return str(title.split(".")[:-1][0])  # split and remove extra white space

    def get_download_url(self):
        """
        This parses box.com url into PDF downloadable file
        :rtype string
        :returns box.com download_url else return None
        """
        driver = self.driver_obj  # get driver
        # Load network requests
        network_requests = list(driver.execute_script("return window.performance.getEntries();"))
        download_url = None  # default or error
        for i in network_requests:
            # this will scrap the pdf file in the word
            if (("public.boxcloud.com/api/2.0/files" in i["name"]) or 
            ("dl.boxcloud.com/api/2.0/files" in i["name"])) and "content?preview=true" in i["name"]: # new method
                download_url = i["name"]
            elif ("internal_files" in i["name"]) and ("pdf" in i["name"]):  # check for a pdf file
                download_url = i["name"]
        return download_url

    def clean(self):
        """
        This will close the current selenium session
        """
        self.driver_obj.quit()
        if self.use_x11 is True:
            self.display.stop()
