import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import subprocess

df = pd.read_csv('nosdeputes_cood.csv', sep=',')

df_votes = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')



app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Hemicycle du Parlement Français"),
    dcc.Graph(id='hemicycle-plot'),
    html.Div(id='click-data-output')
])

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

@app.callback(
    Output('hemicycle-plot', 'figure'),
    [Input('hemicycle-plot', 'id')]
)
def update_plot(_):
    max_seat = 650
    fig = go.Figure()

    for _, row in df.iterrows():
        x = row['X']
        y = row['Y']
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

if __name__ == '__main__':
    app.run_server(debug=True)
