import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        # Page d'accueil
        html.Div(
            "Présentation", 
            style={
                'fontSize':35,
                'textAlign':'center',
                'font-family':'monospace, sans-serif', 
                'color':'#005b96',
                'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': 40
            }),

        html.Div(
        "Cette application offre une variété de représentations et d'analyses des données de votes de l'Assemblée Nationale française, " + 
        "\npermettant ainsi une exploration plus intuitive des décisions et opinions exprimées lors des séances. Son objectif principal est de" + 
        "\nrendre les informations plus accessibles et compréhensibles, offrant aux utilisateurs une perspective claire sur les délibérations et" + 
        "\nles tendances au sein de l'Assemblée Nationale.",
        style={
            "width": 1000,
            'fontSize': 24,
            'textAlign': 'justify',
            'font-family': 'monospace, sans-serif', 
            'color': 'black',
            'marginTop': 30,
            'lineHeight': 2,
            'marginLeft': "auto", 
            'marginRight': "auto", 
            'marginTop': 20
        }
    )
    ]
)