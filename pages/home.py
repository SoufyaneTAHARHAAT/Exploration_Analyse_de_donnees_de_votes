import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        # main app framework
        html.Div("Bienvenue à l'application de visualisation des données des parlementaire", style={'fontSize':50, 'textAlign':'center'}),
        html.Hr(),
    ]
)