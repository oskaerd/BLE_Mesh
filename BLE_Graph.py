import dash
import dash_core_components as dcc
import dash_html_components as html

class BLE_Graph():
    def __init__(self, id, datasets = [], layout = {}):
        self.datasets = datasets
        self.layout = layout

        self.figure = {
            'data': self.datasets,
            'layout': self.layout
        }

        self.graph = dcc.Graph(
            id = str(id),
            figure = self.figure
        )
