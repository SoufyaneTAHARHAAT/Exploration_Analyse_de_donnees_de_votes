import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path='/analyse')

loy_parti = pd.read_csv('average_party_loyalty.csv')

df_cood = pd.read_csv('nosdeputes_cood.csv', sep=',')

loy_dep = pd.read_csv('party_loyalty.csv')

def shorten_party_name(party_name):
    max_length = 15  # Longueur maximale autorisée
    if len(party_name) > max_length:
        return party_name[:max_length-3] + '...'  # Tronquer et ajouter ...
    else:
        return party_name

loy_parti['short_party_name'] = loy_parti['parti_ratt_financier'].apply(shorten_party_name)

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
    dcc.Graph(id='party-loyalty-graph'),
    dcc.Graph(id='Deputy_loyalty')
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
                     x='short_party_name', 
                     y='avg', 
                     color='parti_ratt_financier',
                     labels={'avg': 'Loyauté'},
                     title='Loyauté moyenne au sein des partis',
                     template='plotly_white')
        fig.update_layout(  xaxis_title='Nom du parti',
                            yaxis_title='Loyauté',
                            xaxis_tickangle=0,
                            xaxis_tickmode='auto',
                            uniformtext_minsize=8,  
                            uniformtext_mode='hide',  
                            coloraxis_showscale=False,
                            showlegend=False) 
        return fig
    else:
        return {}
    
def percentage(dep):
    per = loy_dep.loc[loy_dep['deputy_name']==dep, 'percentage']
    if not per.empty:
        return per.iloc[0]
    else:
        return 0
        
@callback(
    Output('Deputy_loyalty', 'figure'),
    [Input('Deputy_loyalty', 'id')]
)
def update_deputy_loyalty(id):
    if id == 'Deputy_loyalty':
        fig = go.Figure()
        for _, row in df_cood.iterrows():
            per = percentage(row['slug'])
            colors=[per] + [1]
            x = row['X']
            y = row['Y']
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=dict(
                    size=10,
                    color=colors,
                    colorscale = 'Viridis',
                    opacity=0.5
                ),
                text=f"{row['nom']} ({row['parti_ratt_financier']}), loyauté : {per}",
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