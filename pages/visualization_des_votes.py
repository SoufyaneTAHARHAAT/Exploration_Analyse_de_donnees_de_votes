import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import subprocess

dash.register_page(__name__, path='/Visualisation_des_votes')

# Visualisation des votes des députés

df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

titres = df['titre'].unique()

df_cood = pd.read_csv('nosdeputes_cood.csv', sep=',')

layout = html.Div([
    html.H1("Statistiques de vote", style={'fontSize': '32px'}), 

    html.Div([
        html.Label('Sélectionnez un titre de loi :', style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='law-select',
            options=[{'label': titre, 'value': titre} for titre in titres],
            value=''
        )
    ]),

    html.Div([
        html.Label('Sélectionnez un nom de député :', style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='deputy-select',
            style={'width': '50%'},  
            value='',  
            disabled=True 
        )
    ]),

    html.Div([
        html.Div(id='position-output', style={'fontSize': '18px'}),  
        html.Div(id='parti-output', style={'fontSize': '18px'})  
    ]),

    html.Div(
        style={'display': 'flex', 'justify-content': 'center'},
        children=[
        dcc.Graph(id='hemicycle-plot'),
    ]),

    html.Div(style={'display': 'flex', 'justify-content': 'center'},id='click-data-output'),

    html.Div([
        dcc.Graph(id='bar-chart')
    ])


])

# Selection d'un titre de loi dans le menu déroulant

@callback(
    Output('deputy-select', 'options'),
    [Input('law-select', 'value')]
)
def update_deputy_options(selected_titre):
    if selected_titre:
        filtered_df = df[df['titre'] == selected_titre]
        available_deputies = filtered_df['deputy_name'].unique()
        deputy_options = [{'label': deputy, 'value': deputy} for deputy in available_deputies]
        return deputy_options
    else:
        return []

# Si titre selectionné on autorise la sélection de député

@callback(
    Output('deputy-select', 'disabled'),
    [Input('law-select', 'value')]
)
def enable_deputy_dropdown(selected_titre):
    if selected_titre:
        return False  
    else:
        return True  

#  Affichage du parti et de la position du député selectionné

@callback(
    [Output('position-output', 'children'),
     Output('parti-output', 'children')],
    [Input('law-select', 'value'),
     Input('deputy-select', 'value')]
)
def update_position_and_party_output(selected_titre, selected_deputy):
    if selected_titre and selected_deputy:
        filtered_df = df[(df['titre'] == selected_titre) & (df['deputy_name'] == selected_deputy)]
        if len(filtered_df) == 0:
            return f"Les données pour {selected_deputy} sur cette loi ne sont pas disponibles", ""
        else:
            position = filtered_df['position'].iloc[0]
            parti_ratt_financier = filtered_df['parti_ratt_financier'].iloc[0]
            return f"La position de {selected_deputy} sur cette loi est {position}", f"Parti rattaché : {parti_ratt_financier}"
    else:
        return "", ""


# Diagramme de barres avec les pourcentages pour / contre / abstention

@callback(
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
        sort = filtered_df['sort'].iloc[0] 
        
       
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
                    'text': [f'{d["value"]:.2f}%'], 
                    'textposition': 'auto'
                } 
                for d in data
            ],
            'layout': {
                'title': f'Distribution generale des votes pour la loi choisie/ Decision finale ({sort})',
                'yaxis': {'title': 'Pourcentage de votes (%)'},
                'barmode': 'group'
            }
        }
    else:
        return {} 
    
# Retourne la couleur associé au parti

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

# Affiche l'hémicycle de parlementaires et leur parti si aucune loi est sélectionnée, sinon la position des députés sur la loi

@callback(
    Output('hemicycle-plot', 'figure'),
    [Input('law-select', 'value')]
)
def update_hemicycle(selected_titre):
    if selected_titre:
        filtered_df = df[df['titre'] == selected_titre]
        filtered_df.set_index('deputy_name', inplace=True)
        fig = go.Figure()

        for _, row in df_cood.iterrows():
            x = row['X']
            y = row['Y']
            try:
                ligne = filtered_df.loc[row['slug']]['position']
            except:
                ligne = False
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=dict(
                    size=10,
                    color=('gray' if ligne == False else 'blue' if ligne=='pour' else 'green'
 if ligne=='abstention' else '#f77915'),
                opacity=0.5
            ),
            text=f"{row['nom']} ({row['parti_ratt_financier']})",
            customdata=[row['id']],
            hoverinfo='text'
            ))

        fig.update_layout(
            title='Hemicycle du Parlement Français',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False,
            height=800,
            width=1200,
            plot_bgcolor='white'
        )

        return fig
    else:
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
            text=f"{row['nom']} ({row['parti_ratt_financier']})",
            customdata=[row['id']],
            hoverinfo='text'
        ))

    fig.update_layout(
        title='Hemicycle du Parlement Français',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
        height=800,
        width=1200,
        plot_bgcolor='white'
    )

    return fig
        
# Renvoie d'ID du député dans l'hémicycle sur lequel on clique et affiche ses informations

@callback(
    Output('click-data-output', 'children'),
    [Input('hemicycle-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        clicked_id = clickData['points'][0]['customdata']
        subprocess.run(["python", "depute.py", str(clicked_id)])
        return html.Div(f'ID du député : {clicked_id}')
    else:
        return html.Div('Cliquer sur un député pour afficher ses informations')

