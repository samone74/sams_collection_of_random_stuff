# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from smeterd.meter import SmartMeter

from datetime import datetime, timedelta
from datetime import date
from time import mktime, localtime
import time
import timeit
import csv
import os
import tracemalloc


def main():
    fieldnames = ['date', 'gas', 'low_consumed', 'high_consumed', 'current_consumed']
    interval = 60
    output_path = '/media/pi/MyPassport/'
    csv_file_name_end = 'smartmeter.csv'
    new_file = False
    snapshot1 = None
    while True:
        start = timeit.timeit()
        # reading the smart meter
        try:
            meter = SmartMeter('/dev/ttyUSB0')
            meter.serial.baudrate = 115200
            packet = meter.read_one_packet()
            meter.disconnect()
        except:
            continue
        now = datetime.now()
        print("now =", now)

        # storing the result in csv file
        result_dict = {'date': str(now), 'gas': packet['gas']['total'],
                       'low_consumed': packet['kwh']['low']['consumed'],
                       'high_consumed': packet['kwh']['high']['consumed'],
                       'current_consumed': packet['kwh']['current_consumed']}

        if not os.path.exists(output_path + str(now.year)):
            os.mkdir(output_path + str(now.year))
        if not os.path.exists(output_path + str(now.year) + '/' + str(now.month)):
            os.mkdir(output_path + str(now.year) + '/' + str(now.month))
        csv_file_name = output_path + str(now.year) + '/' + str(now.month) + '/' + str(now.day) + csv_file_name_end
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

        if not snapshot1:
            snapshot1 = tracemalloc.take_snapshot()
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        print("[ Top 10 ]")
        for stat in top_stats[:10]:
            print(stat)
        time.sleep(interval - duration)
        snapshot1 = snapshot2

        time.sleep(interval - duration)


if __name__ == '__main__':
    tracemalloc.start()
    main()
