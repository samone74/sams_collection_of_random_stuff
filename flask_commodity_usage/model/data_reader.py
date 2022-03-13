
class data_reader:
    def __init__(self, config):
        i = 1

    def get_years(self):
        # find the popssible year for which there is data
        return 2020, 2021

    def get_months(self, year):
        # returns the month in the given year for which there is measurement data
        return [1,2,3,4]

    def get_days(self, year, month):
        # returns the days in the month for which there is measurement data
        return [1, 2, 3, 4, 5]

    def get_usage_year(self, year):
        # returns a dict with the electicity consumption, production and gas usage
        return {}

