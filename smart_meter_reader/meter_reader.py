
from datetime import datetime
import csv
import os
import asyncio
import time
import timeit


class MeterReader:
    def __init__(self, cfg):
        self.interval = cfg['interval']
        self.output_path = cfg['output_path']
        self.file_name = cfg['file_name']
        self.readers = []
        self.result_dict = {}
        self.now = datetime.now()
        self.new_file = False

    def add_reader(self, reader):
        self.readers.append(reader)

    def reader_meters(self):
        # method to read all input data
        self.now = datetime.now()
        print("now =", self.now)
        self.result_dict = {'date':self.now}
        # storing the result in csv file
        for reader in self.readers:
            self.result_dict.update(asyncio.run(reader.read_meter()))

    def write_to_file(self):
        # method to store the date which has been read to a csv file in the folder year/month/day.csv
        if not os.path.exists(self.output_path + str(self.now.year)):
            os.mkdir(self.output_path + str(self.now.year))
        if not os.path.exists(self.output_path + str(self.now.year) + '/' + str(self.now.month)):
            os.mkdir(self.output_path + str(self.now.year) + '/' + str(self.now.month))
        csv_file_name = self.output_path + str(self.now.year) + '/' + str(self.now.month) + '/' \
                        + str(self.now.day) + self.file_name
        if not os.path.isfile(csv_file_name):
            self.new_file = True
        fieldnames = [key for key in self.result_dict]
        with open(csv_file_name, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if self.new_file:
                writer.writeheader()
                self.new_file = False
            writer.writerow(self.result_dict)

    def start_reading(self):
        # method to start reading the data every time defined by the given interval
        while True:
            start = timeit.timeit()
            # reading the smart meter
            self.reader_meters()
            self.write_to_file()
            # determining time it took to perform all task and then hold to next interval
            end = timeit.timeit()
            duration = end - start
            time.sleep(self.interval - duration)