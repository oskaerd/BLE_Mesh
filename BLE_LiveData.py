import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, Event
import plotly
import plotly.graph_objs as go
import sqlite3
import atexit

webapp_name = 'BLE-Mesh Live Data'

database_filename = 'measurements.db'
db_read_query_head = 'SELECT *'
db_read_values = 'dev_id, temp, humidity, pressure, lux, battery)'
db_read_query_tail = ' from measurements'

REFRESH_RATE = 1

measurements_db = sqlite3.connect(database_filename)

def onClose():
    print('Database connection closed.')
    measurements_db.close()

data = measurements_db.execute(db_read_query_head  + db_read_query_tail)

data = data.fetchall()
print(len(data))

# lists storing the data to display
x = []
temperature = []
humidity = []
pressure = []
light = []
battery = []

value_of_interest_key = 'Temperature'
values_of_interest_dict = {
    'Temperature': { 'values': temperature, 'unit': '[C]' },
    'Humidity': { 'values': humidity, 'unit': '[%]' },
    'Pressure': { 'values': pressure, 'unit': '[hPa]' },
    'Light ': { 'values': light, 'unit': '[lux]' },
    'Battery': { 'values': battery, 'unit': '[%]' },
}

devices = ['0xAAAA', '0xABCD', '0xBBBA', '0xBEEF', '0x0001']

i=0
for meas in data:
    x.append(i)
    meas = list(meas)
    temperature.append(meas[1])
    humidity.append(meas[2])
    pressure.append(meas[3])
    light.append(meas[4])
    battery.append(meas[5])
    i+=1

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2(webapp_name,
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='devices-list',
                 options=[{'label': dev, 'value': dev}
                          for dev in devices],
                 value=['0x0001'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='live-graph'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000 * REFRESH_RATE),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
        dash.dependencies.Output('live-graph', 'children'),
        [ dash.dependencies.Input('devices-list', 'value') ],
        events=[dash.dependencies.Event('graph-update', 'interval')])
def update_graph(devices_names):
    # update values here
    print(devices_names)
    # prepare values
    loc_x = x
    loc_y = values_of_interest_dict[value_of_interest_key]['values']
    # later in loop
    loc_data = go.Scatter(
        x = loc_x,
        y = loc_y,
        name = 'Scatter'
    )

    graphs = []
    graphs.append(html.Div(
        dcc.Graph(
            id=value_of_interest_key,
            animate = True,
            figure = { 'data': [loc_data], 'layout':go.Layout(
                xaxis = dict(range=[min(loc_x), max(loc_y)]),
                yaxis = dict(range=[min(loc_y), max(loc_y)]),
                margin = {'l':50,'r':1,'t':45,'b':1},
                title = '{}'.format(value_of_interest_key)
            ) }
        )
    ))

    return graphs

if __name__ == "__main__":
    atexit.register(onClose)
    app.run_server(debug=True)
