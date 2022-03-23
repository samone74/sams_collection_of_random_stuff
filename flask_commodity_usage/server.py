from flask import Flask, render_template, url_for, redirect
from flask import jsonify
import yaml
from model import data_reader
app = Flask(__name__)

config_file = 'config.yml'

data = data_reader.DataReader(config_file)


@app.route('/', methods=['GET'])
# here you can click to the different parts of usage.
def hello_world():
    path = url_for('get_usage')
    return 'hello world'


@app.route('/current_usage')
#shows the latest reading of the smart meter
def get_current_state():
    return "Still needs tobe implemented"


@app.route('/get_overview/<string:commodity>')
def get_year_usage(commodity):

    years = [['years','electricity usage (kWh'],
             [2020, 10000],
             [2021, 20000]]
    return render_template('welcome.html', rows=years)



@app.route('/get_usage')
# will show an table with the usage per year.
# One year can then be selected to get an overview of every month of that year
def get_years_usage():
    years = data.get_years()
    results = [['year'] + data.items]
    for year in years:
        result = data.get_usage_year(year)
        path = url_for('get_usage')
        row = [year]
        for item in result:
            row.append(result[item])
        results.append(row)
    return render_template('welcome.html', rows=results)


@app.route('/get_usage/<int:year>')
# this will show an overview of the usage per month of the selected year
# every month can be clicked to show an overview of that month by day
def get_usage_year(year):
    months = data.get_months(year)
    results = [['year'] + data.items]
    for month in months:
        result = data.get_usage_month(year, month)
        row = [month]
        for item in result:
            row.append(result[item])
        results.append(row)
    return render_template('welcome.html', rows=results)


@app.route('/get_usage/<int:year>/<int:month>')
# this will show an over view of the usage of that month per day
# possibility togo back to the month or the year overview.
def get_usage_month(year, month):
    days = data.get_days(year,month)
    results = [['year'] + data.items]
    for day in days:
        result = data.get_usage_day(year, month, day)
        row = [day]
        for item in result:
            row.append(result[item])
        results.append(row)
    return render_template('welcome.html', rows=results)


@app.route('/get_usage/<int:year>/<int:month>/<int:day>')
# this will show an overview of the usage per day on hourly base
def get_usage_day(year, month, day):
    return "Still needs to be implemented " + str(month) + " " + str(day)


if __name__ == '__main__':
    # reading the config file
    with open("config.yml", "r") as f:
        config = yaml.safe_load(f)
    app.run(debug=True, port=config['settings']['port'], host=config['settings']['host'])
