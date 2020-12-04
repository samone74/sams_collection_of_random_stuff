# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from smeterd.meter import SmartMeter

from datetime import datetime
from datetime import date
from time import mktime, localtime
import time
import timeit
import csv
import os
def main():

    fieldnames = ['date', 'gas', 'low_consumed', 'high_consumed', 'current_consumed']
    interval = 60
    output_path = '/media/pi/MyPassport/'
    csv_file_name_end = 'smartmeter.csv'
    new_file = False
    while True:
        start = timeit.timeit()
        # reading the smart meter
        meter = SmartMeter('/dev/ttyUSB0')
        meter.serial.baudrate = 115200
        packet = meter.read_one_packet()
        meter.disconnect()
        now = datetime.now()
        print("now =", now)

        # storing the result in csv file
        result_dict = {'date': str(now), 'gas': packet['gas']['total'], 'low_consumed': packet['kwh']['low']['consumed'],
                       'high_consumed': packet['kwh']['high']['consumed'],
                       'current_consumed': packet['kwh']['current_consumed']}
        if not os.path.exists(output_path + str(now.year)):
            os.mkdir(output_path + str(now.year))
        csv_file_name = output_path + str(now.year) + '/' + str(now.month) + csv_file_name_end
        if not os.path.isfile(csv_file_name):
            new_file = True

        with open(csv_file_name, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if new_file:
                writer.writeheader()
                new_file = False
            writer.writerow(result_dict)
        end = timeit.timeit()
        duration = end - start
        time.sleep(interval - duration)


if __name__ == '__main__':
    main()

