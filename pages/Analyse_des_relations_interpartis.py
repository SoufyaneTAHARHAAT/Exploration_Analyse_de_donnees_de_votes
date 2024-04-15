import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
from dash.dependencies import Input, Output
import plotly.express as px

dash.register_page(__name__, path='/analyse')

loy_parti = pd.read_csv('average_party_loyalty.csv')

layout = html.Div([
    html.Div(
    'Analyse de la loyauté des députés vis-à-vis de leur parti',
    style={
                'fontSize':20,
                'textAlign':'center',
                'font-family':'monospace, sans-serif', 
                'color':'black',
                'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': 40
            }),
    dcc.Graph(id='party-loyalty-graph')
])

@callback(
    Output('party-loyalty-graph', 'figure'),
    [Input('party-loyalty-graph', 'id')] 
)
def update_graph(input_id):
    if input_id == 'party-loyalty-graph':
        sorted_df = loy_parti.sort_values(by='avg', ascending=False)
        colors = px.colors.qualitative.Plotly[:len(sorted_df)]
        fig = px.bar(sorted_df, 
                     x='parti_ratt_financier', 
                     y='avg', 
                     color='parti_ratt_financier',
                     labels={'avg': 'Loyauté'},
                     title='Loyauté moyenne au sein des partis',
                     template='plotly_white')
        fig.update_layout(xaxis_title='Nom du parti',
                          yaxis_title='Loyauté',
                          xaxis_tickangle=-45,
                          uniformtext_minsize=8,  
                          uniformtext_mode='hide',  
                          coloraxis_showscale=False,
                          showlegend=False) 
        return fig
    else:
        return {}