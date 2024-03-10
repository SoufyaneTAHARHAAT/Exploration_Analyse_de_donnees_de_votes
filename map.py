import json, dash, subprocess
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# charger le fichier geojson 
with open('departments.geojson') as f:
    geojson_data = json.load(f)

# extraire les données du depts du fichier geojson
department_data = []
for feature in geojson_data['features']:
    properties = feature['properties']
    department_data.append({
        "nom": properties['nom'],
        "code": properties['code'],
        "latitude": feature['geometry']['coordinates'][0][0][1],  
        "longitude": feature['geometry']['coordinates'][0][0][0] 
    })

app = dash.Dash(__name__)

# on crée le layout de la carte
app.layout = html.Div(
    children=[
    html.H1('Carte des départements', className='carte-page-title'),
    html.Div(
        children=[
        dcc.Graph(
            id='france-map',
            figure=go.Figure(go.Scattermapbox(
                lat=[department['latitude'] for department in department_data],
                lon=[department['longitude'] for department in department_data],
                mode='markers',
                marker=go.scattermapbox.Marker(size=13), #color='rgba(137, 196, 244, 1)'#),
                text=[f"{department['nom']} / {department['code']}" for department in department_data],
                hoverinfo='text',
            ),
            layout=go.Layout(
                mapbox_style="carto-positron",
                mapbox_zoom=4.5,
                mapbox_center={"lat": 46.6034, "lon": 1.8883},
            )),
            style={'height':'850px'}
        ),
    ]), 
    # on utilise ça pour satisfaire la sortie requis du callback (dummy output to avoid error)
    html.Div(id='dummy-output', style={'display': 'none'})
])

# # Callback pour gérer le clique sur un dept
@app.callback(
    Output('dummy-output', 'children'),
    [Input('france-map', 'clickData')]
)
# afficher les circonscriptions et députés de chaque département
def handle_click(deptData):
    if deptData is not None:
        # extraire le code du dept du string de format (department / code) sur la carte
        extracted_code = deptData['points'][0]['text'][-2:]
        # passer le code du dep en paramètre en executant le script qui affiche les cironscriptions 
        subprocess.run(["python", "circons.py", str(extracted_code)])

# Callback pour changer la couleur du dept on hover
@app.callback(
    Output('france-map', 'figure'),
    [Input('france-map', 'hoverData')],
    [State('france-map', 'figure')]
)
def display_hover_data(hoverData, current_figure):
    if hoverData is None or not hoverData['points']:
        return current_figure
    
    hovered_department = hoverData['points'][0]['text'][-2:]
    updated_data = []
    for dep in current_figure['data'][0]['text']:  # Assuming the hover data is associated with the first trace
        marker_color = 'rgba(137, 196, 244, 1)'  # couleur par défaut
        if dep[-2:] == hovered_department:
            marker_color = 'rgba(255, 0, 0, 1)'  # changer la couleur
        updated_data.append(marker_color)

    # créer une copie de la figure actuel et changer la couleur du dept 
    updated_figure = current_figure.copy()
    updated_figure['data'][0]['marker']['color'] = updated_data

    return updated_figure


if __name__ == '__main__':
    app.run_server(debug=True)


