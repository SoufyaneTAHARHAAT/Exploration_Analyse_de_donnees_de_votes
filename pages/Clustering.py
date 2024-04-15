import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path="/clustering")

# Charger la matrice à partir du fichier CSV
df = pd.read_csv('matrice_votes_deputes.csv')

deputy_names = df['nom_depute']

# Supprimer la colonne des noms des députés
df = df.drop(columns=['nom_depute'])

# Sélectionner uniquement les colonnes de valeurs numériques à normaliser
data_to_normalize = df.iloc[:, 1:]

# Initialiser le scaler
scaler = MinMaxScaler()

# Normaliser les données et remplacer les valeurs dans le DataFrame
df.iloc[:, 1:] = scaler.fit_transform(data_to_normalize)

# Initialiser une liste pour stocker les valeurs du coefficient de silhouette
silhouette_scores = []

# Essayer différents nombres de clusters
for n_clusters in range(2, 11):
    # Appliquer l'algorithme K-Means
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(df)
    
    # Calculer le coefficient de silhouette
    silhouette_avg = silhouette_score(df, labels)
    silhouette_scores.append(silhouette_avg)

# Trouver le nombre optimal de clusters
optimal_n_clusters = silhouette_scores.index(max(silhouette_scores)) + 2  # +2 car on a commencé avec 2 clusters

# Appliquer l'algorithme K-Means avec le nombre optimal de clusters
kmeans = KMeans(n_clusters=optimal_n_clusters)
labels = kmeans.fit_predict(df)

# Réduire la dimensionnalité des données à 2D
pca = PCA(n_components=2)
data_2d = pca.fit_transform(df)

# Créer un DataFrame pour les données réduites à 2D
data_2d_df = pd.DataFrame(data_2d, columns=['Composante principale 1', 'Composante principale 2'])

# Ajouter les étiquettes des clusters au DataFrame
data_2d_df['Cluster'] = labels

# Créer une figure Plotly Express pour visualiser les clusters dans l'espace 2D
fig_2d = px.scatter(data_2d_df, x='Composante principale 1', y='Composante principale 2', color='Cluster', 
                    title='Clusters dans l\'espace 2D (PCA)', opacity=0.7)

# Compter le nombre de députés dans chaque cluster
cluster_counts = pd.Series(labels).value_counts().sort_index()

# Créer un diagramme à barres pour la répartition des députés dans chaque cluster
fig_bar = go.Figure(data=[go.Bar(x=cluster_counts.index, y=cluster_counts.values, marker_color='skyblue')])
fig_bar.update_layout(title='Répartition des députés dans chaque cluster', xaxis_title='Cluster', yaxis_title='Nombre de députés')

# Charger le fichier contenant les informations sur les députés (nom et parti politique)
deputy_info = pd.read_csv('deputy_votes_new_last.csv', encoding='latin1')

# Créer un dictionnaire pour stocker les députés par parti politique et par cluster
deputies_by_party_and_cluster = {cluster: {} for cluster in range(optimal_n_clusters)}
for deputy_name, label in zip(deputy_names, labels):
    party = deputy_info[deputy_info['deputy_name'] == deputy_name]['parti_ratt_financier'].iloc[0]
    if party not in deputies_by_party_and_cluster[label]:
        deputies_by_party_and_cluster[label][party] = []
    deputies_by_party_and_cluster[label][party].append(deputy_name)

# Créer l'application Dash
# app = dash.Dash(__name__)

# Layout de l'application Dash
layout = html.Div([
    dcc.Graph(id='2d-plot', figure=fig_2d),
    dcc.Graph(id='bar-plot', figure=fig_bar),
    html.Div(id='party-deputies'),
])

# Callback pour afficher les députés du parti sélectionné et leur pourcentage lorsqu'une barre est cliquée
@callback(
    Output('party-deputies', 'children'),
    [Input('bar-plot', 'clickData')]
)
def display_party_deputies(click_data):
    if click_data is None:
        return ''
    cluster = click_data['points'][0]['x']
    party_deputies = []
    party_percentages = {}
    total_deputies = sum(cluster_counts)
    for party, deputies in deputies_by_party_and_cluster[cluster].items():
        party_count = len(deputies)
        party_percentages[party] = (party_count / total_deputies) * 100
        party_deputies.append(html.Div([
            html.H3(f'Parti politique : {party} ({party_percentages[party]:.2f}%)'),
            html.Ul([
                html.Li(deputy) for deputy in deputies
            ])
        ]))
    return party_deputies

# # Exécuter l'application Dash
# if __name__ == '__main__':
#     app.run_server(debug=True)
