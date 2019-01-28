import dash
import dash_core_components as dcc
import dash_html_components as html

from dashWebAppColors import BLE_WebAppColors
from BLE_Graph import BLE_Graph

class BLE_AppLayout:
    def __init__(self):
        self.style = BLE_WebAppColors()

        self.init_graph = BLE_Graph('example')

        self.layout = html.Div([
                html.H1(
                       ['Ble App']
            ),
            BLE_Graph(id='example', datasets=[
                {'x': [1, 2, 3, 4, 5], 'y': [9, 6, 2, 1, 5], 'type': 'line', 'name': 'Boats'},
                {'x': [1, 2, 3, 4, 5], 'y': [8, 7, 2, 7, 3], 'type': 'bar', 'name': 'Cars'},
            ], layout = {
                'title': 'Basic Dash Example'
            }).graph
        ])

    def getLayout(self):
        return self.layout