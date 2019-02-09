import argparse
import sys
from datetime import datetime

import configparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from fileManager import FileManager
from trvwCSVdownloader import TradingviewBot


class SpreadsheetUpdater():
    def __init__(self, pair):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        self.client = gspread.authorize(creds)

        self.sheet = self.client.open('cryptoscreener')

        self.pair = pair

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    # one line method...
    def openNewSheet(self):
        return self.client.open("tradehistory of cryptoscreener").sheet1

    def searchAndCopy(self, newSheet, filemanager):
        print('now inserting all the found values')
        sheet = self.sheet.sheet1
        data = sheet.findall(self.pair)

        print('Found the following matches with ' + self.pair)
        print(data)

        i = 0
        for cell in data:
            newSheet.insert_row([filemanager.getTimeSlot(cell.row)
                                ] + sheet.row_values(cell.row), 2)
            i = i + 1

        # Insert current date and time to spreadsheet.
        if data:
            newSheet.insert_row([str(datetime.now())], 2)

    # from the files that are downloaded, get them and put them in google sheets
    # assumption: the .csv files are deleted after inserted into google sheets.
    def putFilesInGoogleSheets(self, filemanager):
        content = filemanager.mergeCSVFiles().read()

        sheet = self.client.open('cryptoscreener')
        print(sheet)
        self.client.import_csv(sheet.id, content)


bot = TradingviewBot()
manager = FileManager()
sUpdater = SpreadsheetUpdater(bot.args['pair'])

print(bot.args['pair'])
# bot.signIn()
# print('Sign in stage completed')
#
# bot.downloadAll()
# print('download stage completed')

sUpdater.putFilesInGoogleSheets(manager)
print('Files in google sheets stage completed')

newSheet = sUpdater.openNewSheet()
sUpdater.searchAndCopy(newSheet, manager)
print('Search and copy stage completed')

manager.moveDownloadedFilesToFolder()
print('Moved files into new folder')

print(bot.args['no_delete'])
if not bot.args['no_delete']:
    FileManager.removeOldFiles(manager)

# todo:
# what if a lot of alerts are going off in a short amount of time?