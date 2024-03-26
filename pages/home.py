import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        # main app framework
        html.Div(
            "Bienvenue à l'application de visualisation des données des parlementaire", 
            style={
                'fontSize':35,
                'textAlign':'center',
                'font-family':'monospace, sans-serif', 
                'color':'#005b96',
                'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': 40
            }),
    ]
)