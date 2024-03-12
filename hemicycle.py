import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import subprocess

df_cood = pd.read_csv('nosdeputes_cood.csv', sep=',')

# df_votes = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Charger les données CSV avec un encodage différent
df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Extraire les titres uniques et les noms des députés
titres = df['titre'].unique()
noms_deputes = df['deputy_name'].unique()

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
            options=[{'label': nom, 'value': nom} for nom in noms_deputes],
            value=noms_deputes[0]
        )
    ]),
    
    html.Div([
    html.Div(id='position-output', style={'fontSize': '18px'}) # Agrandir le titre
    ]),

    
    html.Div([
        dcc.Graph(id='bar-chart')
    ]),

    html.Div([
    dcc.Graph(id='hemicycle-plot'),
    html.Div(id='click-data-output')
    ])
])

# Define callback to update the position output message
@app.callback(
    Output('position-output', 'children'),
    [Input('law-select', 'value'),
     Input('deputy-select', 'value')]
)
def update_position_output(selected_titre, selected_deputy):
    if selected_deputy is None:
        return "Sélectionnez un député"
    else:
        filtered_df = df[(df['titre'] == selected_titre) & (df['deputy_name'] == selected_deputy)]
        if len(filtered_df) == 0:
            return f"Les données pour {selected_deputy} sur cette loi ne sont pas disponibles"
        else:
            position = filtered_df['position'].iloc[0]
            # return f"La position de {selected_deputy} sur '{selected_titre}' est {position}"
            return f"La position de {selected_deputy} sur cette loi est {position}"



# Définir la fonction de rappel pour mettre à jour le graphique à barres
# en fonction du titre sélectionné
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('law-select', 'value')]
)
def update_bar_chart(selected_titre):
    filtered_df = df[df['titre'] == selected_titre]
    total_votes = filtered_df['nombre_votants'].sum()
    pour_votes = filtered_df['nombre_pours'].sum()
    contre_votes = filtered_df['nombre_contres'].sum()
    abstention_votes = filtered_df['nombre_abstentions'].sum()
    
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
            'title': f'Distribution generale des votes pour cette loi',
            'yaxis': {'title': 'Pourcentage de votes (%)'},  # Mettre à jour le titre de l'axe des y
            'barmode': 'group'
        }
    }

@app.callback(
    Output('hemicycle-plot', 'figure'),
    [Input('law-select', 'value')]
)
def update_hemicycle(selected_titre):
    filtered_df = df[df['titre'] == selected_titre]
    filtered_df.set_index('deputy_name', inplace=True)
    fig = go.Figure()

    for _, row in df_cood.iterrows():
        x = row['X']
        y = row['Y']
        try : ligne = filtered_df.loc[row['slug']]['position']
        except : ligne = False
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers',
            marker=dict(
                size=10,
                color=('gray' if ligne == False else 'green' if ligne=='pour' else 'purple' if ligne=='abstention' else 'red'),
                opacity=0.5
            ),
            text=row['nom'],
            customdata=[row['id']]
        ))

    fig.update_layout(
        title='Hemicycle du Parlement Français',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=600,
        width=800,
        plot_bgcolor='white'
    )

    return fig


def define_color(parti) :
    match parti :
        case 'RN' :
            return '#152c80'
        case 'LR' :
            return 'blue'
        case 'MODEM' :
            return '#ef5b0c'
        case 'HOR' :
            return '#0adcf5'
        case 'LIOT' :
            return '#f5dc0a'
        case 'NI' :
            return '#c5c5c5'
        case 'REN' :
            return '#701fff'
        case 'SOC' :
            return '#f51fff'
        case 'ECO' :
            return 'green'
        case 'LFI' :
            return 'red'
        case 'GDR' :
            return '#a51111'


@app.callback(
    Output('click-data-output', 'children'),
    [Input('hemicycle-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        clicked_id = clickData['points'][0]['customdata']
        # passer l'id du député en paramètre en executant le script qui affiche les détails du député 
        subprocess.run(["python", "depute.py", str(clicked_id)])
        return html.Div(f'ID du député : {clicked_id}')
    else:
        return html.Div('Cliquer sur un député')

"""
@app.callback(
    Output('hemicycle-plot', 'figure'),
    [Input('hemicycle-plot', 'id')]
)
def update_plot(_):
    fig = go.Figure()

    for _, row in df_cood.iterrows():
        x = row['X']
        y = row['Y']
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers',
            marker=dict(
                size=10,
                color=define_color(row['groupe_sigle']),
                opacity=0.5
            ),
            text=row['nom'],
            customdata=[row['id']]
        ))

    fig.update_layout(
        title='Hemicycle du Parlement Français',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=600,
        width=800,
        plot_bgcolor='white'
    )

    return fig

    """

if __name__ == '__main__':
    app.run_server(debug=True)
