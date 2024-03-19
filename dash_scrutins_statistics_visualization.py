import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html, Input, Output

# Charger les données CSV avec un encodage différent
df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Extraire les titres uniques et les noms des députés
titres = df['titre'].unique()

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Définir la mise en page de l'application avec des titres plus grands
app.layout = html.Div([
    html.H1("Statistiques de vote", style={'fontSize': '32px'}),  # Ajouter un style pour agrandir le titre
    
    html.Div([
        html.Label('Sélectionnez un titre de loi :', style={'fontSize': '18px'}),  # Agrandir le titre
        dcc.Dropdown(
            id='law-select',
            options=[{'label': titre, 'value': titre} for titre in titres],
            value=titres[0]
        )
    ]),
    
    html.Div([
        html.Label('Sélectionnez un nom de député :', style={'fontSize': '18px'}),  # Agrandir le titre
        dcc.Dropdown(
            id='deputy-select',
            style={'width': '50%'},  # Réduire la largeur pour un meilleur ajustement
            value='',  # Définir une valeur par défaut
            disabled=True  # Désactiver le menu déroulant jusqu'à ce qu'une loi soit sélectionnée
        )
    ]),
    
    html.Div([
    html.Div(id='position-output', style={'fontSize': '18px'}) # Agrandir le titre
    ]),

    
    html.Div([
        dcc.Graph(id='bar-chart')
    ])
])

# Define callback to update deputy dropdown options based on selected law
@app.callback(
    Output('deputy-select', 'options'),
    [Input('law-select', 'value')]
)
def update_deputy_options(selected_titre):
    if selected_titre:
        # Filter dataframe based on selected law and deputies with available data
        filtered_df = df[df['titre'] == selected_titre]
        available_deputies = filtered_df['deputy_name'].unique()
        # Construct options for deputy dropdown
        deputy_options = [{'label': deputy, 'value': deputy} for deputy in available_deputies]
        return deputy_options
    else:
        # If no law is selected, return empty options
        return []

# Define callback to enable deputy dropdown when a law is selected
@app.callback(
    Output('deputy-select', 'disabled'),
    [Input('law-select', 'value')]
)
def enable_deputy_dropdown(selected_titre):
    if selected_titre:
        return False  # Enable dropdown when a law is selected
    else:
        return True   # Disable dropdown when no law is selected

# Define callback to update the position output message
@app.callback(
    Output('position-output', 'children'),
    [Input('law-select', 'value'),
     Input('deputy-select', 'value')]
)
def update_position_output(selected_titre, selected_deputy):
    if selected_titre and selected_deputy:
        filtered_df = df[(df['titre'] == selected_titre) & (df['deputy_name'] == selected_deputy)]
        if len(filtered_df) == 0:
            return f"Les données pour {selected_deputy} sur cette loi ne sont pas disponibles"
        else:
            position = filtered_df['position'].iloc[0]
            return f"La position de {selected_deputy} sur cette loi est {position}"
    else:
        return ""

# Définir la fonction de rappel pour mettre à jour le graphique à barres
# en fonction du titre sélectionné
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('law-select', 'value')]
)
def update_bar_chart(selected_titre):
    if selected_titre:
        filtered_df = df[df['titre'] == selected_titre]
        total_votes = filtered_df['nombre_votants'].sum()
        pour_votes = filtered_df['nombre_pours'].sum()
        contre_votes = filtered_df['nombre_contres'].sum()
        abstention_votes = filtered_df['nombre_abstentions'].sum()
        sort = filtered_df['sort'].iloc[0]  # Ajout du sort
        
        # Calculer les pourcentages
        pour_percentage = (pour_votes / total_votes) * 100
        contre_percentage = (contre_votes / total_votes) * 100
        abstention_percentage = (abstention_votes / total_votes) * 100
        
        data = [
            {'category': 'Pour', 'value': pour_percentage},
            {'category': 'Contre', 'value': contre_percentage},
            {'category': 'Abstention', 'value': abstention_percentage}
        ]
        
        return {
            'data': [
                {
                    'x': [d['category']],
                    'y': [d['value']],
                    'type': 'bar',
                    'name': d['category'],
                    'text': [f'{d["value"]:.2f}%'],  # Formater l'étiquette pour afficher les pourcentages
                    'textposition': 'auto'
                } 
                for d in data
            ],
            'layout': {
                'title': f'Distribution generale des votes pour la loi choisie/ Decision finale ({sort})',  # Ajout du sort dans le titre
                'yaxis': {'title': 'Pourcentage de votes (%)'},  # Mettre à jour le titre de l'axe des y
                'barmode': 'group'
            }
        }
    else:
        return {}

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
