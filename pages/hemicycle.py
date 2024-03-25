import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import subprocess

dash.register_page(__name__, path='/hemicycle')

df = pd.read_csv('https://www.nosdeputes.fr/deputes/enmandat/csv', sep=';').filter(items = ['id', 'nom', 'sexe', 'date_naissance', 'num_deptmt', 'nom_circo', 'groupe_sigle', 'parti_ratt_financier', 'place_en_hemicycle']).dropna(subset=['place_en_hemicycle']) 

def calculate_coordinates(seat, max_seat):
    segment_size = max_seat / 12
    segment = int((seat - 1) // segment_size)
    angle = (seat - segment * segment_size - 1) * np.pi / (segment_size - 1)
    radius = 12 - segment
    x = np.cos(angle) * radius
    y = np.sin(angle) * radius
    return x, y


layout = html.Div([
    html.H1("Hemicycle du Parlement Français"),
    dcc.Graph(id='hemicycle-plot'),
    html.Div(id='click-data-output')
])

@callback(
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

@callback(
    Output('hemicycle-plot', 'figure'),
    [Input('hemicycle-plot', 'id')]
)
def update_plot(_):
    max_seat = 650
    fig = go.Figure()

    for _, row in df.iterrows():
        x, y = calculate_coordinates(row['place_en_hemicycle'], max_seat)
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers',
            marker=dict(
                size=5,
                color='blue',
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
