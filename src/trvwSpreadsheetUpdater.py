import argparse
import sys
from datetime import datetime

import configparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from fileManager import FileManager
from trvwCSVdownloader import TradingviewBot


class SpreadsheetUpdater():
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        self.client = gspread.authorize(creds)

        self.sheet = self.client.open('cryptoscreener')

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    # one line method...
    def openNewSheet(self):
        return self.client.open("tradehistory of cryptoscreener").sheet1

    def searchAndCopy(self, newSheet):
        print('now inserting all the found values')
        sheet = self.sheet.sheet1
        data = sheet.findall(self.pair)

        print(data)

        i = 0
        for cell in data:
            newSheet.insert_row([FileManager.getTimeSlot(cell.row)
                                ] + sheet.row_values(cell.row), 2)
            i = i + 1

        # Insert current date and time to spreadsheet.
        if data:
            newSheet.insert_row([str(datetime.now())], 2)

    # from the files that are downloaded, get them and put them in google sheets
    # assumption: the .csv files are deleted after inserted into google sheets.
    def putFilesInGoogleSheets(self):
        content = FileManager.mergeCSVFiles().read()

        sheet = self.client.open('cryptoscreener')
        print(sheet)
        self.client.import_csv(sheet.id, content)


bot = TradingviewBot()
print(bot.args['pair'])
sUpdater = SpreadsheetUpdater()
# bot.signIn()
# bot.downloadAll()
#
# sUpdater.putFilesInGoogleSheets()
# newSheet = sUpdater.openNewSheet()
# sUpdater.searchAndCopy(newSheet)
print(bot.args['no_delete'])
if bot.args['no_delete']:
    FileManager.removeOldFiles(None)

