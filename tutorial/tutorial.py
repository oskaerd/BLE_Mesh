import dash
import dash_core_components as dcc
import dash_html_components as html
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def generate_random_data(points, name):
    x = []
    y = []
    add = 0
    if name == 'Gateway':
        add=2
    for i in range(points):
        x.append(i+32)
        y.append(22 + add + float(random.randint(1, 100))/100)

    return {
        'x': x, 'y' : y, 'type': 'line', 'name': name
    }

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children=["BLE Mesh Network: "], style={
        'textAlign':'left', 'color':colors['text'], 'padding-left':'2%'
    }),
    html.H4(children='''
            Sensor nodes data.
        ''', style={
            'textAlign':'left', 'color':colors['text'], 'padding-left':'7%'
        }),
    html.Div('''
            todo: workout displaying date instead of measure number, rearange app layout
        ''', style={
            'color':colors['text'], 'padding-left':'1%'
        }
    ),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    #{'x': [1,2,3], 'y': [10,1,2], 'type': 'line', 'name':'Gateway'},
                    generate_random_data(17, 'Gateway'),
                    #{'x': [1,2,3], 'y': [2,4,5], 'type': 'line', 'name':'Node2'},
                    generate_random_data(17, 'Node-2')
                ],
                'layout': {
                    'title':'Temperature',
                    'plot_bgcolor':colors['background'],
                    'paper_bgcolor':colors['background'],
                    'font': {
                        'color':colors['text']
                    }
                }
            }
        ),
            html.Label(
                'Data type: ', style={
                    'color':colors['text']
                }
            ),
            dcc.RadioItems(
            options=[
                {'label': 'Temperature', 'value': 'MTL'},
                {'label': 'Pressure', 'value': 'MTLs'},
                {'label': 'Humidity', 'value': 'SF'},
                {'label': 'Lux', 'value': 'SFa'},
                {'label': 'Battery', 'value': 'SFaa'},
            ],
            value='MTL',
            style={'color':colors['text']}
        ),
        html.Label(
                'Display nodes: ', style={
                    'color':colors['text']
                }
            ),
            dcc.Dropdown(
            options=[
                {'label': 'Gateway', 'value': 'MTL'},
                {'label': 'Node-2', 'value': 'MTLs'},
                {'label': 'Node-1', 'value': 'SF'},
                {'label': 'Node-3', 'value': 'SFaa'},
            ],
            value=['MTL', 'MTLs'],
            multi=True,
            style={'color':'black'}
        ),
    ]
)

if __name__=="__main__":
    app.run_server(debug=True)
