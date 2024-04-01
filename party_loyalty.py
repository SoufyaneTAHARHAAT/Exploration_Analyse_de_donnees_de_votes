import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import subprocess

df_dep = pd.read_csv('https://www.nosdeputes.fr/deputes/enmandat/csv', sep=';').filter(items = ['id', 'nom', 'parti_ratt_financier'])

df_votes = pd.read_csv('deputy_votes_new_last.csv', encoding='ISO-8859-1').filter(items = ['deputy_name', 'parti_ratt_financier','titre', 'position'])

df_add = pd.DataFrame(columns = df_votes['parti_ratt_financier'].unique())
df_add['titre'] = df_votes['titre'].unique()
df_add.loc[:, df_add.columns != 'titre'] = 0

def define_vote(pos) :
    match pos : 
        case 'pour' :
            return 1
        case 'contre' :
            return -1
        case _:
            return 0

for index, row in df_votes.iterrows():
    index = df_add.index[df_add['titre'] == row['titre']].tolist()

    if index and len(index) == 1:
        index = index[0]
        df_add.at[index, row['parti_ratt_financier']] += define_vote(row['position'])

for index, row in df_add.iterrows():
    for column, value in row.items():
        if column != 'titre':
            df_add.at[index, column] = ('pour' if value > 0 else 'contre' if value < 0 else 'abstention')

df_same_votes = pd.DataFrame()
df_same_votes['deputy_name'] = df_votes['deputy_name'].unique()
df_same_votes['voted_as_party'] = 0
df_same_votes['nb_votes'] = 0

for index, row in df_votes.iterrows():
    index = df_add.index[df_add['titre'] == row['titre']].tolist()

    if index and len(index) == 1:
        index = index[0]
    
    if row['position'] == df_add.at[index, row['parti_ratt_financier']] :
        df_same_votes.loc[df_same_votes['deputy_name'] == row['deputy_name'], ['voted_as_party']] += 1

    df_same_votes.loc[df_same_votes['deputy_name'] == row['deputy_name'], ['nb_votes']] += 1

df_same_votes['percentage'] = df_same_votes['voted_as_party']/df_same_votes['nb_votes']*100

df_same_votes.to_csv('party_loyalty.csv', index=False)