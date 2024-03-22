import pandas as pd
from sklearn.decomposition import PCA

# Charger la matrice de données à partir du fichier CSV
df = pd.read_csv('matrice_votes_deputes.csv', index_col=0)

# Transposer la matrice pour avoir les députés comme lignes et les scrutins comme colonnes
df = df.T

# Remplacer les valeurs manquantes par 0 ou toute autre valeur selon votre choix
df.fillna(0, inplace=True)

# Appliquer l'analyse en composantes principales (PCA)
pca = PCA(n_components=2)  # Vous pouvez spécifier le nombre de composantes principales souhaitées
pca_result = pca.fit_transform(df)

# Créer un DataFrame pour stocker les résultats de PCA
pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'], index=df.index)

# Afficher les résultats de PCA
print(pca_df)
