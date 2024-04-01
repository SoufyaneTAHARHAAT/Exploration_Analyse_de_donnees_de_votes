import pandas as pd

# Charger le fichier CSV contenant les données des députés
df = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1')

# Créer une liste de tous les députés uniques
deputies = df['deputy_name'].unique()

# Créer une liste de tous les scrutins uniques (numéros)
scrutin_numbers = list(range(1, 11))  # Supposons qu'il y a 10 scrutins

# Créer un DataFrame vide avec les députés comme index et les scrutins comme colonnes
matrix_df = pd.DataFrame(index=deputies, columns=scrutin_numbers)

# Remplir la matrice avec les valeurs de vote en suivant la logique de codage fournie
for deputy in deputies:
    deputy_votes = df[df['deputy_name'] == deputy]
    for scrutin_number in scrutin_numbers:
        vote_value = 0  # Par défaut, on considère que les données ne sont pas disponibles
        vote_entry = deputy_votes[deputy_votes['numero'] == scrutin_number]
        if not vote_entry.empty:
            vote = vote_entry.iloc[0]['position']
            if vote == 'pour':
                vote_value = 1
            elif vote == 'contre':
                vote_value = -1
            elif vote == 'abstention':
                vote_value = 0
        matrix_df.loc[deputy, scrutin_number] = vote_value

# Exporter le DataFrame résultant dans un nouveau fichier CSV sans les numéros à gauche
matrix_df.to_csv('matrice_votes_deputes.csv', index=True, header=True, index_label='nom_depute')

