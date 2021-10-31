# class to procces smart meter data into dict which can be used to plot different type of graphs with plotly
# This graphs can be displayed on the dashboard
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os


class SmartMeterDataYear:
    def __init__(self, data_location, year):
        self.year = year
        self.folder = data_location + '//' + str(year)
        self.data_months = {}
        for i in range(1, 13):
            folder = self.folder + '//' + str(i)
            if os.path.exists(folder):
                self.data_months[i] = SmartMeterDatObjectMonth(folder)

    def get_usage_month(self, month):
        return self.data_months[month].get_month_electricity_usage()

    def plot_usage_per_month(self, what='Electricity', fig=None):
        usage = []
        months = []
        for month in range(1, 13):
            if month in self.data_months:
                if what == 'Electricity':
                    usage.append(self.data_months[month].get_month_electricity_usage())
                    y_label = 'Electricity usage (kWh)'
                else:
                    usage.append(self.data_months[month].get_month_gas_usage())
                    y_label = 'Gas usage (m^3)'
                months.append(month)
        if fig is None:
            fig = go.Figure()
        fig.layout.yaxis.title = y_label
        fig.add_trace(go.Bar(x=months, y=usage, name=str(self.year)))
        fig.update_layout(title_text=what )
        return fig


class SmartMeterDatObjectMonth:
    def __init__(self, folder):
        self.folder = folder
        self.data = {}
        for i in range(1, 32):
            filename = self.folder + '//' + str(i) + 'smartmeter.csv'
            if os.path.exists(filename):
                self.data[i] = SmartMeterDataObjectDay(filename)

    def plot_gas_usage(self):
        dates = []
        gas_usage = []
        for day in self.data:
            dates.append(self.data[day].time_axis)
            gas_usage.append(self.data[day].data['gas'])
        df = pd.DataFrame(list(zip(dates, gas_usage)), columns=['Date', 'gas'])
        fig = px.line(df, x='Date', y="gas")
        return fig

    def plot_gas_usage_per_day(self):
        gas_usage = []
        days = []
        for day in self.data:
            gas_usage.append(self.data[day].get_total_gas_usage())
            days.append(day)
        df = pd.DataFrame(list(zip(days, gas_usage)), columns=['Day', 'gas'])
        fig = px.bar(df, x='Day', y="gas")
        return fig

    def plot_el_usage_per_day(self):
        el_usage = []
        days = []
        for day in self.data:
            el_usage.append(self.data[day].get_total_el_usage())
            days.append(day)
        df = pd.DataFrame(list(zip(days, el_usage)), columns=['Day', 'el_usage'])
        fig = px.bar(df, x='Day', y="el_usage")
        return fig

    def get_month_electricity_usage(self):
        last_day = max(self.data.keys())
        first_day = min(self.data.keys())
        low_consumed = self.data[last_day].data['low_consumed'].iloc[-1] - self.data[first_day].data['low_consumed'][0]
        high_consumed = self.data[last_day].data['high_consumed'].iloc[-1] - self.data[first_day].data['high_consumed'][0]
        total_usage = low_consumed + high_consumed
        return total_usage

    def get_month_gas_usage(self):
        last_day = max(self.data.keys())
        first_day = min(self.data.keys())
        total_usage = self.data[last_day].data['gas'].iloc[-1] - self.data[first_day].data['gas'][0]
        return total_usage


class SmartMeterDataObjectDay:
    def __init__(self, file):
        self.file = file
        self.data = pd.read_csv(self.file)
        self.date = self.data['date']

        self.time_begin = []
        self.time_begin.append(0.0)
        self.time_axis = []
        self.time_axis.append(datetime.strptime(self.date[0][0:-7], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))
        for i in range(1, len(self.date)):
            self.time_axis.append(datetime.strptime(self.date[i][0:-7], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))
            self.time_begin.append(self.time_axis[-1] - self.time_axis[0])
        self.data['datetime'] = pd.Series(self.time_axis)

    def plot_gas(self):
        fig = px.line(self.data, x='datetime', y="gas")
        return fig

    def plot_electricity_consumed(self):
        fig = px.line(self.data, x='datetime', y=["low_consumed", "high_consumed"])
        return fig

    def get_total_gas_usage(self):
        gas_used = list(self.data['gas'])[-1] - self.data['gas'][0]

        return gas_used

    def get_total_el_usage(self):
        el_low = list(self.data['low_consumed'])[-1] - self.data['low_consumed'][0]
        el_high = list(self.data['high_consumed'])[-1] - self.data['high_consumed'][0]
        return el_high + el_low


class HistoricalData:
    def __init__(self, file):
        data = pd.read_excel(file)
        self.hist_usage = {}
        for year, month, el_usage, gas_usage in zip(data['jaar'], data['maand'], data['elektriciteit'], data['gas']):
            usage_dict = {'Electricity': el_usage,
                          'Gas': gas_usage}
            if year in self.hist_usage:
                if month in self.hist_usage[year]:
                    raise RuntimeError(month + ' in ' + year + ' is found twice in historical usage')
                else:
                    self.hist_usage[year][month] = usage_dict
            else:
                self.hist_usage[year] = {month: usage_dict}

    def plot_usage(self, year, what='Electricity', fig=None):
        if fig is None:
            fig = go.Figure()
        if year not in self.hist_usage:
            raise RuntimeError(str(year) + ' not in historical data')
        el_usage = []
        months = []
        for month in self.hist_usage[year]:
            months.append(month)
            el_usage.append(self.hist_usage[year][month][what])
        fig.add_trace(go.Bar(x=months, y=el_usage, name=str(year)))
        return fig


def main():
    folder = r'Y:\\'
    smart_data = SmartMeterDataYear(folder, 2021)
    #print(smart_data.get_usage_month(1))
    #smart_data.plot_el_usage_per_day().show()
    #smart_data.plot_gas_usage_per_day().show()
    i = 1
    hist_data_file = r'Y:\2020\histories_data.xlsx'
    hist_data = HistoricalData(hist_data_file)
    figure = smart_data.plot_usage_per_month()

    figure = hist_data.plot_usage(year=2020, fig=figure)
    hist_data.plot_usage(year=2019, fig=figure).show()
    figure2 = smart_data.plot_usage_per_month(what='gas')
    figure2 = hist_data.plot_usage(year=2020, what='gas', fig=figure2)
    hist_data.plot_usage(year=2019, what='gas', fig=figure2).show()
    smart_data.plot_usage_per_month(what='gas').show()
    smart_data.data_months[10].plot_gas_usage_per_day().show()



if __name__ == '__main__':
    main()
