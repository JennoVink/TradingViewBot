import os
import shutil
from abc import abstractmethod
from datetime import date
import argparse

# The filemanager copies files to other locations and is able to remove old files.
import configparser


class FileManager():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.amountOfLines = []
        for i in range(0, 7):
            # the first row in the csv doesn't have to be counted
            self.amountOfLines.append(-1)

    @abstractmethod
    def moveDownloadedFilesToFolder(self):
        filename = 'crypto_' + str(date.today())
        downlLocation = self.config['DEFAULT']['download_location'] + filename
        moveToLocation = self.config['COPY']['move_to_location']

        shutil.copyfile(downlLocation + str('.csv'), moveToLocation + self.config['COPY']['0'] + filename + str('.csv'))

        for i in range (1, 7):
            frm = downlLocation + ' (' + str(i) + ").csv"
            to = moveToLocation + self.config['COPY'][str(i)] + filename + ".csv"
            shutil.copyfile(frm, to)

    @abstractmethod
    def mergeCSVFiles(self):
        print('going to merge csv files...')
        filename = 'crypto_' + str(date.today())
        path = self.config['DEFAULT']['DOWNLOAD_LOCATION'] + filename

        # Clear out.csv:
        with open("out.csv", "w"):
            pass

        fout = open("out.csv", "a")

        # first file:
        for line in open(path + str('.csv')):
            fout.write(line)
            self.amountOfLines[0] = self.amountOfLines[0] + 1
        print((self.amountOfLines[0]))

        # now the rest:
        for num in range (1, 7):
            print(num)
            try:
                f = open(path + ' (' + str(num) + ").csv")
                next(f)  # skip the header
                fout.write('\n')
                for line in f:
                    fout.write(line)
                    self.amountOfLines[num] = self.amountOfLines[num] + 1
                f.close()  # not really needed
            except:
                print('file not found / other exception')
                print(path + ' (' + str(num) + ").csv")
                pass
        fout.close()

        print(self.amountOfLines)

        return open('out.csv', 'r')

    @abstractmethod
    def removeOldFiles(self):
        print('going to merge csv files...')
        filename = 'crypto_' + str(date.today())
        path = self.config['DEFAULT']['DOWNLOAD_LOCATION'] + filename

        os.remove(path + str('.csv'))

        # now the rest:
        for num in range(1, 7):
            print(num)
            try:
                os.remove(open(path + ' (' + str(num) + ").csv"))
            except:
                print('file not found - cannot remove or other exception')
                print(path + ' (' + str(num) + ").csv")
                pass


    #### helper function / leftover.......
    ###
    # Depending on the rownumber, the timeslot (in hours) is determined.
    ###
    def getTimeSlot(self, rowNumber):
        timeslots = [0.0833, 0.25, 1, 4, 24, 168, 720]

        i = 0
        while (rowNumber - self.amountOfLines[i] > 0):
            rowNumber = rowNumber - self.amountOfLines[i]
            i = i + 1

        return timeslots[i]




manager = FileManager()
manager.mergeCSVFiles()
# manager.moveDownloadedFilesToFolder()
