import pandas as pd
from datetime import datetime
import plotly.express as px


def rindex(mylist, myvalue):
    return len(mylist) - mylist[::-1].index(myvalue) - 1


class SmartMeterDataObjectDay:
    def __init__(self, file):
        self.file = file
        self.data = pd.read_csv(self.file)
        self.date = self.data['date']

        self.time_begin = []
        self.time_begin.append(0.0)
        self.time_axis = []
        self.time_axis.append(datetime.strptime(self.date[0][0:-7], '%Y-%m-%d %H:%M:%S')) #+ timedelta(hours=1))
        for i in range(1, len(self.date)):
            self.time_axis.append(datetime.strptime(self.date[i][0:-7], '%Y-%m-%d %H:%M:%S')) #+ timedelta(hours=1))
            self.time_begin.append(self.time_axis[-1] - self.time_axis[0])
        self.data['datetime'] = pd.Series(self.time_axis)
        self.gas_usage_per_hour = []
        self.el_low_usage_per_hour = []
        self.el_high_usage_per_hour = []
        self.el_low_prod_per_hour = []
        self.el_high_prod_per_hour = []
        self.ppv_per_hour = []
        self.hours = []
        self.convert_to_hourly_data()

    def convert_to_hourly_data(self):
        hours = [item.hour for item in self.data['datetime']]
        for i in range(24):
            if i in hours:
                start = hours.index(i)
                end = rindex(hours, i)
                self.gas_usage_per_hour.append(self.data['gas'][end] - self.data['gas'][start])
                self.el_low_usage_per_hour.append(self.data['low_consumed'][end] - self.data['low_consumed'][start])
                self.el_high_usage_per_hour.append(self.data['high_consumed'][end] - self.data['high_consumed'][start])
                if 'produced_low' in self.data:
                    value = self.data['produced_low'][end] - self.data['produced_low'][start]
                    self.el_low_prod_per_hour.append(value)
                    value = float(self.data['produced_high'][end] - self.data['produced_high'][start])
                    self.el_high_prod_per_hour.append(value)
                else:
                    self.el_low_prod_per_hour.append(0.0)
                    self.el_high_prod_per_hour.append(0.0)
                if 'ppv' in self.data:
                    # ppv is in watts
                    value = 0.0
                    for j in range(start,end):
                        timedelta = self.time_axis[j + 1] - self.time_axis[j]
                        value += self.data['ppv'][j] * timedelta.seconds / 1000.0 / 3600.0

                    self.ppv_per_hour.append(value)
                else:
                    self.ppv_per_hour.append(0.0)
                self.hours.append(i)

    def plot_gas(self):
        df = pd.DataFrame(list(zip(self.hours, self.gas_usage_per_hour)), columns=['Hours', 'Gas usage (m^3)'])
        fig = px.bar(df, x='Hours', y="Gas usage (m^3)")
        return fig

    def plot_electricity_consumed(self):
        df = pd.DataFrame(list(zip(self.hours, self.el_low_usage_per_hour, self.el_high_usage_per_hour)), columns=['Hours', 'Low el usage', 'high el usage'])
        fig = px.bar(df, x='Hours', y=["Low el usage", "high el usage"])
        return fig

    def plot_electricity_produced(self):
        df = pd.DataFrame(list(zip(self.hours, self.el_low_prod_per_hour, self.el_high_prod_per_hour)), columns=['Hours', 'Low el production', 'high el production'])
        fig = px.bar(df, x='Hours', y=["Low el production", "high el production"])
        return fig

    def get_total_gas_usage(self):
        gas_used = list(self.data['gas'])[-1] - self.data['gas'][0]
        return gas_used

    def get_total_el_usage(self):
        el_low = list(self.data['low_consumed'])[-1] - self.data['low_consumed'][0]
        el_high = list(self.data['high_consumed'])[-1] - self.data['high_consumed'][0]
        return el_high + el_low

    def get_el_high_consumed(self):
        return list(self.data['high_consumed'])[-1] - self.data['high_consumed'][0]

    def get_el_low_consumed(self):
        return list(self.data['low_consumed'])[-1] - self.data['low_consumed'][0]

    def get_el_high_produced(self):
        return list(self.data['produced_high'])[-1] - self.data['produced_high'][0]

    def get_el_low_produced(self):
        return list(self.data['produced_low'])[-1] - self.data['produced_low'][0]

    def get_values(self, name):
        if name == 'ppv':
            return self.get_ppv()
        if name in self.data:
            return list(self.data[name])[-1] - self.data[name][0]
        return 0.0

    def get_ppv(self):
        return sum(self.ppv_per_hour)