import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html, Input, Output

# Load the CSV data with a different encoding
df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Extract unique titres
titres = df['titre'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Vote Statistics"),
    html.Div([
        dcc.Dropdown(
            id='law-select',
            options=[{'label': titre, 'value': titre} for titre in titres],
            value=titres[0]
        )
    ]),
    html.Div([
        html.H3(id='sort-type'),  # Display sort type above the chart
        dcc.Graph(id='bar-chart')
    ])
])

# Define callback to update the bar chart based on selected titre
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('sort-type', 'children')],
    [Input('law-select', 'value')]
)
def update_bar_chart(selected_titre):
    filtered_df = df[df['titre'] == selected_titre]
    total_votes = filtered_df['nombre_votants'].sum()
    pour_votes = filtered_df['nombre_pours'].sum()
    contre_votes = filtered_df['nombre_contres'].sum()
    abstention_votes = filtered_df['nombre_abstentions'].sum()
    
    # Calculate percentages
    pour_percentage = (pour_votes / total_votes) * 100
    contre_percentage = (contre_votes / total_votes) * 100
    abstention_percentage = (abstention_votes / total_votes) * 100
    
    data = [
        {'category': 'Pour', 'value': pour_percentage},
        {'category': 'Contre', 'value': contre_percentage},
        {'category': 'Abstention', 'value': abstention_percentage}
    ]
    
    # Get the sort type for the selected titre
    sort_type = filtered_df['sort'].iloc[0]  # Assuming all rows have the same sort type for a given titre
    
    return {
        'data': [
            {
                'x': [d['category']],
                'y': [d['value']],
                'type': 'bar',
                'name': d['category'],
                'text': [f'{d["value"]:.2f}%'],  # Format the label to display percentages
                'textposition': 'auto'
            } 
            for d in data
        ],
        'layout': {
            'title': f'Vote Distribution for {selected_titre}',
            'yaxis': {'title': 'Percentage of Votes (%)'},  # Update y-axis title
            'barmode': 'group'
        }
    }, f'Sort : {sort_type}'

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
