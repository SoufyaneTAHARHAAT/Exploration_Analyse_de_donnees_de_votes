import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json

# Step 1: Load Data
def loadDeputes():
    with open('nosdeputes.json', 'r') as file:
        data = json.load(file)
    return data['deputes']

def extract_ages(data):
    ages = [2024 - int(deputy['depute']['date_naissance'][:4]) for deputy in data]
    return ages

def age_distribution_graph(ages):
    fig = px.histogram(x=ages, 
                       height=500,
                       nbins=20, 
                       labels={'x': 'Age'},
                       title='Distribution d\'age des députés en france',
                       color_discrete_sequence=['rgba(137, 196, 244, 1)'],)
    fig.update_yaxes(title_text="Nombre des députés")
    fig.update_layout(bargap=0.15, title_x=0.5, title_font_size=20)
    fig.update_traces(hovertemplate='<b>Age</b>: %{x}<br><b>Total députés</b>: %{y}',
                      hoverlabel=dict(
                          bgcolor='rgba(255, 0, 0, 0.6)',
                          font=dict(color='#ffffff'),
                          bordercolor='#ffffff'))
    return fig

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(f"Nombre total des députés: {len(loadDeputes())}", className="total-deputes-title"),
    dcc.Graph(id='age-graph',
              config={'displayModeBar': False, 'scrollZoom': False})
])

@app.callback(
    Output('age-graph', 'figure'),
    [Input('age-graph', 'id')]
)
def update_age_graph(dummy_input):

    deputies_data = loadDeputes()    
    ages = extract_ages(deputies_data)
    fig = age_distribution_graph(ages)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

# on peut par exemple afficher juste les députés qui sont dans une certaine distribution d'age
# quand l'utilisateur clique sur une bar de l'histogramme