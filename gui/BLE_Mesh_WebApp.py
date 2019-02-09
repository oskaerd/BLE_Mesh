import dash
import dash_core_components as dcc
import dash_html_components as html

from BLE_AppLayout import BLE_AppLayout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app_layout = BLE_AppLayout()

app.layout = app_layout.getLayout()

if __name__=="__main__":
    app.run_server(debug=True)
