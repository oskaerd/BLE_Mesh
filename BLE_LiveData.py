import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, Event
import plotly
import plotly.graph_objs as go
import sqlite3
import atexit

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

app.layout = html.Div(
    [
        html.H2(
            'BLE Mesh Data',
            style = {
                'float':'left',
            }),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval = REFRESH_RATE * 1000
        )
    ]
)



@app.callback(Output('live-graph', 'figure'),
        events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    value_of_interest = values_of_interest_dict[value_of_interest_key]
    value_of_interest = value_of_interest['values']
    x.append(x[-1]+1)
    value_of_interest.append(value_of_interest[-1]+0.1)
    localdata = plotly.graph_objs.Scatter(
            x=list(x),
            y=list(value_of_interest),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [localdata],'layout' : go.Layout(xaxis=dict(range=[min(x),max(x)]),
                yaxis=dict(range=[min(value_of_interest),max(value_of_interest)]),)}

if __name__ == "__main__":
    atexit.register(onClose)
    app.run_server(debug=True)
