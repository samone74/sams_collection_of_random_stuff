import pickle

import yaml
import os
from model.day_results import SmartMeterDataObjectDay


def sort_list_convert_int(l, **kwargs):
    # converts a list of string to a list of ints and sorts the list
    if 'cutoff' in kwargs:
        l = [int(el[:len(el) - len(kwargs['cutoff'])]) for el in l]
    else:
        l = [int(el) for el in l]
    l.sort()
    return l


class DataReader:
    def __init__(self, config_file):
        i = 1
        self.config_file = config_file
        with open(self.config_file, "r") as f:
            config = yaml.safe_load(f)
        self.data_folder = config['database']['data_folder']
        self.file_end = 'smartmeter.csv'
        self.items = ['high_consumed',
                      'low_consumed',
                      'produced_high',
                      'produced_low',
                      'ppv']
        # TODO check if data fo,lder exists

    def get_years(self):
        # find the possible year for which there is data
        years = os.listdir(self.data_folder)
        return sort_list_convert_int(years)

    def get_months(self, year):
        # returns the month in the given year for which there is measurement data
        months = os.listdir(os.path.join(self.data_folder, str(year)))
        return sort_list_convert_int(months)

    def get_days(self, year, month):
        # returns the days in the month for which there is measurement data
        path = os.path.join(self.data_folder, str(year), str(month))
        days = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        return sort_list_convert_int(days, cutoff=self.file_end)

    def get_usage_year(self, year):
        months = self.get_months(year)
        results = {item: 0.0 for item in self.items}
        for month in months:
            result = self.get_usage_month(year, month)
            for item in result:
                results[item] += result[item]
        # returns a dict with the electricity consumption, production and gas usage
        return results

    def get_usage_month(self, year, month):
        results = {item: 0.0 for item in self.items}
        days = self.get_days(year, month)
        for day in days:
            result = self.get_usage_day(year, month, day)
            for item in result:
                results[item] += result[item]
        return results

    def get_usage_day(self, year, month, day):
        file = os.path.join(self.data_folder, str(year), str(month), str(day) + self.file_end)
        pickle_path = os.path.join(self.data_folder, str(year), str(month), 'pickle')
        if not os.path.exists(pickle_path):
            os.mkdir(pickle_path)
        pickle_file = os.path.join(pickle_path, str(day) + self.file_end)
        pickle_file = pickle_file[:-3] + 'pickle'
        if os.path.exists(pickle_file):
            data = pickle.load(open(pickle_file, "rb"))
        else:
            data = SmartMeterDataObjectDay(file)
            pickle.dump(data, open(pickle_file, "wb"))
        result_dict = {}
        for item in self.items:
            result_dict[item] = data.get_values(item)
        return result_dict


if __name__ == '__main__':
    config_file = 'test.yml'
    data = DataReader(config_file)
    print(data.get_years())
    print(data.get_months(2021))
    print(data.get_days(2021, 11))

    print(data.get_usage_day(2022, 3, 15))
    print(data.get_usage_month(2022, 3))
    print(data.get_usage_year(2022))
