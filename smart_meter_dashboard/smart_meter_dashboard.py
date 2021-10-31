import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import helper_functions
import proccess_smart_meter_data

# load the data and reload every day or so.
folder = r'c:\\'
smart_data = proccess_smart_meter_data.SmartMeterDataYear(folder, 2021)

com_list = ['Electricity', 'Gas']
years = [2020, 2021]
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June'
          'July',
          'Augustus',
          'September',
          'October',
          'November'
          'December']
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(children=
             [html.H3("What commodity you want to display"),
              dcc.RadioItems(id='commodity', options=helper_functions.list2dict(com_list)),
              html.Br(),
              html.H3("Select year"),
              dcc.Dropdown(id='years', options=helper_functions.list2dict(years)),
              html.Br(),
              html.H3("Select month"),
              dcc.Dropdown(id='months', options=helper_functions.list2dict(months, values=values)),
              html.Br(),
              dcc.Input(id='days', type='number', min=1, max=31)
              ]),
    html.Div(id='figures', children=[
        dcc.Graph(id='year'),
        dcc.Graph(id='month'),
        dcc.Graph(id='day'),

    ])

])


@app.callback(Output('year', 'figure'),
              [Input('commodity', 'value'),
               Input('years', 'value')]
              )
def make_year_fig(commodity, year):
    if commodity is None:
        return {}
    if year is None:
        return {}
    return smart_data.plot_usage_per_month(commodity)


@app.callback(Output('month', 'figure'),
              [Input('commodity', 'value'),
               Input('months', 'value')])
def make_month_fig(commodity, month):
    if commodity is None:
        return {}
    if month is None:
        return {}
    if commodity == 'Electricity':
        return smart_data.data_months[month].plot_el_usage_per_day()

    return smart_data.data_months[month].plot_gas_usage_per_day()


@app.callback(Output('day', 'figure'),
              [Input('commodity', 'value'),
               Input('months', 'value'),
               Input('days', 'value')])
def make_day_plot(commodity, month, day):
    if commodity is None:
        return {}
    if month is None:
        return {}
    if day is None:
        return {}

    if day > days_per_month[month-1]:
        return {}
    if commodity == 'Electricity':
        return smart_data.data_months[month].data[day].plot_electricity_consumed()
    return smart_data.data_months[month].data[day].plot_gas()

if __name__ == '__main__':
    app.run_server(debug=True, host="192.168.178.23", port=8050)
