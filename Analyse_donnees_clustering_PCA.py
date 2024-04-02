import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

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
    # Appliquer l'algorithme CAH
    agg_clustering = AgglomerativeClustering(n_clusters=n_clusters)
    labels = agg_clustering.fit_predict(df)
    
    # Calculer le coefficient de silhouette
    silhouette_avg = silhouette_score(df, labels)
    silhouette_scores.append(silhouette_avg)

# Trouver le nombre optimal de clusters
optimal_n_clusters = silhouette_scores.index(max(silhouette_scores)) + 2  # +2 car on a commencé avec 2 clusters

# Appliquer l'algorithme CAH avec le nombre optimal de clusters
agg_clustering = AgglomerativeClustering(n_clusters=optimal_n_clusters)
labels = agg_clustering.fit_predict(df)

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



# Créer une liste pour stocker les noms et les partis politiques des députés par cluster
deputies_with_party = [[] for _ in range(optimal_n_clusters)]
for deputy_name, label in zip(deputy_names, labels):
    party = deputy_info[deputy_info['deputy_name'] == deputy_name]['parti_ratt_financier'].iloc[0]
    deputies_with_party[label].append((deputy_name, party))

# Créer l'application Dash
app = dash.Dash(__name__)

# Layout de l'application Dash
app.layout = html.Div([
    dcc.Graph(figure=fig_2d),
    dcc.Graph(figure=fig_bar),
    html.Div([
        html.H2('Noms des députés et leur parti politique par cluster'),
        *[html.Div([
            html.H4(f'Cluster {i+1}'),
            html.Ul([
                html.Li(f'{deputy[0]} - {deputy[1]}') 
                for deputy in deputies_with_party[i]
            ])
        ]) for i in range(optimal_n_clusters)]
    ])
])

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run_server(debug=True)
