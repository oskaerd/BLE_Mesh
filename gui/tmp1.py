import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import socket
import _thread
import atexit

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('socet created')
PORT = 9001
IP_ADDR = '192.168.0.38'
s.bind((IP_ADDR, PORT))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

def on_close():
    global s
    print('port closed')
    s.close()

def get_data(dummy):
    while True:
        data, addr = s.recvfrom(1024)
        print('received: ' + str(list(data)))

def run_app(dummy):
    while True:
        app.run_server(debug=True)

if __name__ == '__main__':
    atexit.register(on_close)

    _thread.start_new_thread( get_data, ('data',))
    #_thread.start_new_thread( run_app, ('app',) )
    app.run_server(debug=True, host = '127.0.0.1')
    
    while True:
        pass
