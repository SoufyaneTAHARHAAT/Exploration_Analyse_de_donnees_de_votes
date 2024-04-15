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
        "A travers cette application, vous pourrez observer différentes représentations et analyses de données de votes de l'Assemblée Nationale française. \n" 
        "L'objectif de celle-ci est de permettre une exploration plus intuitive et compréhensible des décisions et opinions exprimées lors des séances.",
        style={
            'fontSize': 20,
            'textAlign': 'left',
            'font-family': 'monospace, sans-serif', 
            'color': 'black',
            'marginLeft': 30, 
            'marginRight': 30, 
            'marginTop': 20
        }
    )
    ]
)