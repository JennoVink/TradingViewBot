# login to trading view
# download several timeframes
import argparse
import time

import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class TradingviewBot():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.email = self.config['LOGIN']['email']
        self.password = self.config['LOGIN']['password']

        self.SPEEDFACTOR = int(self.config['DEFAULT']['speed_factor'])

        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        # argument parser:
        parser = argparse.ArgumentParser()
        parser.add_argument('--pair', required=True)
        parser.add_argument('--no-delete', action='store_true')

        args = parser.parse_args()

        self.args = vars(args)

        print('Query string:', args)

    # Sign in to TradingView
    def signIn(self):
        self.browser.get('https://www.tradingview.com/#signin')

        time.sleep(0.5 * self.SPEEDFACTOR)

        print(self.browser.find_elements_by_css_selector('#signin-form input'))
        emailInput = self.browser.find_elements_by_css_selector('#signin-form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('#signin-form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(1 * self.SPEEDFACTOR)

    ###
    # Download the csv. The interval goes from 1 to 8.
    # interval : descr : value
    # 1        :  1m   : 1/60 0.01666667
    # 2        :  5m   : 5/60: 0.083333
    # 3        : 15m   : 0.25
    # 4        :  1h   : 1
    # 5        :  4h   : 4
    # 6        :  1d   : 24
    # 7        :  1w   : 168
    # 8        :  1m   : 720
    ###
    def download(self, intervalIndex, shouldRefresh):
        if shouldRefresh:
            self.browser.get('https://www.tradingview.com/crypto-screener/')
            time.sleep(2 * self.SPEEDFACTOR)

        intervalDropdown = self.browser.find_elements_by_xpath('//*[@id="js-screener-container"]/div[2]/div[7]/div[2]')[0]
        print(intervalDropdown)
        intervalDropdown.click()
        time.sleep(1 * self.SPEEDFACTOR)

        dropdownButton = self.browser.find_elements_by_xpath('//*[@id="js-screener-container"]/div[2]/div[7]/div[3]/div/div[1]/div[' + str(intervalIndex) + ']/div')[0]
        dropdownButton.click()
        time.sleep(2 * self.SPEEDFACTOR)

        exportButton = self.browser.find_element_by_css_selector('.tv-screener-toolbar__button--export.apply-common-tooltip.common-tooltip-fixed')
        exportButton.click()
        time.sleep(2 * self.SPEEDFACTOR)

    # Download all (except the 1m) csv data.
    def downloadAll(self):
        refreshFlag = True
        for i in range (2, 9):
            print(i)
            self.download(i, refreshFlag)
            refreshFlag = False


# bot = TradingviewBot()
# bot.signIn()
# bot.downloadAll()