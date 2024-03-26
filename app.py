import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        # main app framework
        html.Div(
            "Visualisation des données parlementaires", 
            style={
                'fontSize':45,
                'textAlign':'center',
                'marginLeft': 'auto', 'marginRight': 'auto', 'marginTop': 20, 'marginBottom': 40,
                'color':'#005b96',
                'font-family':'monospace, sans-serif', 
            }),
        html.Div([
            dcc.Link(
                page['name'], 
                href=page['path'], 
                style={
                    'text-decoration':'none',
                    'margin-left':20,
                    'margin-right':20,
                    'font-size':24,
                    'font-family':'monospace, sans-serif', 
                    'color':'#005b96',
                    'letter-spacing':2,    
                    'padding-left':10, 'padding-right':10,
                    'border-left':'5px solid #005b96'        
                }) for page in dash.page_registry.values()
        ]),

        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)