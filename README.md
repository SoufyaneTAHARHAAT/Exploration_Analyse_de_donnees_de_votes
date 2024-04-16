# Exploration_Analyse_de_donnees_de_votes
# ********** Lancement du projet **********
# Pour lancer l'application, il faut éxecuter le fichier de l'entrée app.py en lançant la commande "python app.py" dans le terminal du dossier du projet
# Après, il faut aller à votre navigateur et lancer le lien suivant: "localhost:8050/"
# NB: parfois, ça peut arriver que Dash change de numéro du port de l'application, il suffit de voir dans le terminal le numéro du port utilisé par Dash
# ***************************************************

# modifications faites par Amine ECHHIBOU sur le fichier hemicycle !
# => j'ai ajouter une ligne dans le fichier hemicycle.py (ligne 37) pour pouvoir éxecuter le fichier depute.py qui affichera le député lors du clique 

# Modifications faites par Soufyane TAHARHAAT sur les deux fichiers data_collector et das_vusialisation, j y ai ajouté de nouvelles options quant au choix de depute, loi et résultats (résulat spécifique à chaque député et résultat globale du vote de la loi)

# le fichier "map.py"
# affichage de la carte de france avec les différents départements, lors du clique sur un département, on
# affiche  les cironscriptions associées à ce dernier avec leurs députés, si on pose la souris sur l'une
# des points bleu, on affiche en POPUP le nom et le code du département

# Modification faites par Soufyane le 19/03
# J'ai ajouté un autre filtre au fichier dash_scrutin_st... pour qu'à chaque fois qu'on choisi une loi, on choisi uniquement parmi les deputes qui y ont participes
# 23/03 J'ai ajouté les partis rattachés à chaque député. J'ai creer une fonction qui genere la matrice de deputes_scrutins pour faire une analyse PCA.
