import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import subprocess

# Load CSV data with a different encoding
df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Load unique titles
titres = df['titre'].unique()

# Load coordinates CSV
df_cood = pd.read_csv('nosdeputes_cood.csv', sep=',')

# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the application with larger titles
app.layout = html.Div([
    html.H1("Statistiques de vote", style={'fontSize': '32px'}),  # Add a style to enlarge the title

    html.Div([
        html.Label('Sélectionnez un titre de loi :', style={'fontSize': '18px'}),  # Enlarge the title
        dcc.Dropdown(
            id='law-select',
            options=[{'label': titre, 'value': titre} for titre in titres],
            value=titres[0]
        )
    ]),

    html.Div([
        html.Label('Sélectionnez un nom de député :', style={'fontSize': '18px'}),  # Enlarge the title
        dcc.Dropdown(
            id='deputy-select',
            style={'width': '50%'},  # Reduce the width for better fit
            value='',  # Set a default value
            disabled=True  # Disable dropdown until a law is selected
        )
    ]),

    html.Div([
        html.Div(id='position-output', style={'fontSize': '18px'})  # Enlarge the title
    ]),

    html.Div([
        dcc.Graph(id='bar-chart')
    ]),

    html.Div([
        dcc.Graph(id='hemicycle-plot'),
        html.Div(id='click-data-output')
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
        return True  # Disable dropdown when no law is selected

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

# Define callback to update the bar chart based on selected law
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
        sort = filtered_df['sort'].iloc[0]  # Add sort
        
        # Calculate percentages
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
                    'text': [f'{d["value"]:.2f}%'],  # Format label to show percentages
                    'textposition': 'auto'
                } 
                for d in data
            ],
            'layout': {
                'title': f'Distribution generale des votes pour la loi choisie/ Decision finale ({sort})',  # Add sort to title
                'yaxis': {'title': 'Pourcentage de votes (%)'},  # Update y-axis title
                'barmode': 'group'
            }
        }
    else:
        return {}  # Return an empty figure if no law is selected

# Define callback to update the hemicycle plot based on selected law
@app.callback(
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
                    color=('gray' if ligne == False else 'blue' if ligne=='pour' else 'green' if ligne=='abstention' else '#f77915'),
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
    else:
        return go.Figure()
# Define callback to handle click data on the hemicycle plot
@app.callback(
    Output('click-data-output', 'children'),
    [Input('hemicycle-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        clicked_id = clickData['points'][0]['customdata']
        # Pass the deputy's id as a parameter by executing the script that displays the deputy's details
        subprocess.run(["python", "depute.py", str(clicked_id)])
        return html.Div(f'ID du député : {clicked_id}')
    else:
        return html.Div('Cliquer sur un député')

def define_color(parti):
    match parti:
        case 'RN':
            return '#152c80'
        case 'LR':
            return 'blue'
        case 'MODEM':
            return '#ef5b0c'
        case 'HOR':
            return '#0adcf5'
        case 'LIOT':
            return '#f5dc0a'
        case 'NI':
            return '#c5c5c5'
        case 'REN':
            return '#701fff'
        case 'SOC':
            return '#f51fff'
        case 'ECO':
            return 'green'
        case 'LFI':
            return 'red'
        case 'GDR':
            return '#a51111'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
