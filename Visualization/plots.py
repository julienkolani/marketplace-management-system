#!/usr/bin/env python
# plots.py
"""
Dashboard du Marché Numérique

Ce script se connecte à MongoDB via son URL (PyMongo), charge les données dans des DataFrames Pandas,
et lance un dashboard interactif avec Dash et Plotly. Le dashboard est lancé dans un processus séparé,
ce qui permet de rendre la main à l'utilisateur dans le terminal.

Onglets du dashboard :
  - Carte du Marché (Bubble Chart) : Sélection du marché et affichage des marchands sous forme de bubble chart.
  - Produits par Marchand         : Sélection d'un marchand et affichage de ses produits.
  - Ventes par Marchand            : Graphique en barres des ventes (chiffre d'affaires) par marchand.
  - Analyse Complémentaire         : Exemple d'évolution des ventes dans le temps.
"""

import os
import sys
import multiprocessing
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from pymongo import MongoClient

# ------------------------------------------------------------------------------
# Configuration et connexion à MongoDB via PyMongo
# ------------------------------------------------------------------------------
MONGO_URI = "mongodb://root:example@localhost:27017/"
MONGO_DB_NAME = "marche_numerique_db"


client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# ------------------------------------------------------------------------------
# Fonctions de chargement des données dans des DataFrames
# ------------------------------------------------------------------------------

def load_transactions_dataframe():
    """Charge la collection 'transaction' dans un DataFrame."""
    transactions = list(db.transaction.find())
    data = []
    for t in transactions:
        data.append({
            'transaction_id': str(t.get('_id')),
            'client_id': str(t.get('client')) if t.get('client') else None,
            'marchand_id': str(t.get('marchand')) if t.get('marchand') else None,
            'montant_total': t.get('montant_total', 0),
            'date': t.get('date'),
            'nombre_produits': len(t.get('produits', []))
        })
    df = pd.DataFrame(data)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

def load_marchands_dataframe():
    """Charge la collection 'marchand' dans un DataFrame."""
    marchands = list(db.marchand.find())
    data = []
    for m in marchands:
        produits = m.get('produits', [])
        stock_total = sum(p.get('quantite', 0) for p in produits) if produits else 0
        data.append({
            'marchand_id': str(m.get('_id')),
            'nom': m.get('nom'),
            'position_x': m.get('position_x'),
            'position_y': m.get('position_y'),
            'stock_total': stock_total,
            'nombre_transactions': len(m.get('historique_ventes', []))
        })
    df = pd.DataFrame(data)
    return df

def load_produits_dataframe():
    """Parcourt la collection 'marchand' pour extraire les produits intégrés dans chaque document."""
    marchands = list(db.marchand.find())
    data = []
    for m in marchands:
        marchand_id = str(m.get('_id'))
        marchand_nom = m.get('nom')
        for produit in m.get('produits', []):
            data.append({
                'marchand_id': marchand_id,
                'marchand_nom': marchand_nom,
                'produit_nom': produit.get('nom'),
                'quantite': produit.get('quantite'),
                'prix': produit.get('prix')
            })
    df = pd.DataFrame(data)
    return df

def load_markets_dataframe():
    """
    Charge la collection 'marche' dans un DataFrame.
    On suppose que chaque document possède :
      - _id, nom, taille_x, taille_y
      - 'marchands' : liste des ObjectId (ou chaînes) correspondant aux marchands appartenant à ce marché.
    """
    markets = list(db.marche.find())
    data = []
    for m in markets:
        data.append({
            'market_id': str(m.get('_id')),
            'nom': m.get('nom', 'Inconnu'),
            'taille_x': m.get('taille_x'),
            'taille_y': m.get('taille_y'),
            'marchands': m.get('marchands', [])
        })
    df = pd.DataFrame(data)
    return df

# Chargement des DataFrames
df_transactions = load_transactions_dataframe()
df_marchands    = load_marchands_dataframe()
df_produits     = load_produits_dataframe()
df_markets      = load_markets_dataframe()

# ------------------------------------------------------------------------------
# Préparation d'analyses préliminaires
# ------------------------------------------------------------------------------
# Synthèse des ventes par marchand
df_sales = pd.merge(df_transactions, df_marchands, on='marchand_id', how='left')
sales_summary = df_sales.groupby('nom')['montant_total'].sum().reset_index()

# Préparation des listes d'options pour les dropdowns
merchant_options = [{"label": row["nom"], "value": row["marchand_id"]} 
                    for _, row in df_marchands.iterrows()]
default_merchant_id = merchant_options[0]["value"] if merchant_options else None

market_options = [{"label": row["nom"], "value": row["market_id"]} 
                  for _, row in df_markets.iterrows()]
default_market_id = market_options[0]["value"] if market_options else None

# ------------------------------------------------------------------------------
# Création de l'application Dash
# ------------------------------------------------------------------------------
app = dash.Dash(__name__)
server = app.server  # Pour le déploiement via WSGI, si besoin

app.layout = html.Div([
    html.H1("Dashboard du Marché Numérique", style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs", value="tab-market", children=[
        dcc.Tab(label="Carte du Marché (Bubble Chart)", value="tab-market"),
        dcc.Tab(label="Produits par Marchand", value="tab-products"),
        dcc.Tab(label="Ventes par Marchand", value="tab-sales"),
        dcc.Tab(label="Analyse Complémentaire", value="tab-additional"),
    ]),
    html.Div(id="tabs-content")
])

# Callback pour le contenu principal des onglets
@app.callback(Output("tabs-content", "children"),
              [Input("tabs", "value")])
def render_content(tab):
    if tab == "tab-market":
        return html.Div([
            html.Label("Sélectionnez un marché :"),
            dcc.Dropdown(
                id="market-dropdown",
                options=market_options,
                value=default_market_id
            ),
            dcc.Graph(id="graph-market")
        ], style={'padding': '20px'})
    elif tab == "tab-products":
        return html.Div([
            html.Label("Sélectionnez un marchand :"),
            dcc.Dropdown(
                id="merchant-dropdown",
                options=merchant_options,
                value=default_merchant_id
            ),
            dcc.Graph(id="graph-products")
        ], style={'padding': '20px'})
    elif tab == "tab-sales":
        fig_sales = go.Figure(data=[go.Bar(x=sales_summary['nom'], y=sales_summary['montant_total'])])
        fig_sales.update_layout(
            title="Chiffre d'affaires par Marchand",
            xaxis_title="Marchand",
            yaxis_title="Ventes (Montant Total)"
        )
        return html.Div([ dcc.Graph(figure=fig_sales) ], style={'padding': '20px'})
    elif tab == "tab-additional":
        # Exemple : évolution des ventes dans le temps
        if df_transactions.empty:
            fig_time = go.Figure()
            fig_time.update_layout(title="Aucune transaction disponible")
        else:
            df_time = df_transactions.copy().sort_values('date')
            fig_time = go.Figure(data=go.Scatter(x=df_time['date'], y=df_time['montant_total'],
                                                  mode='lines+markers'))
            fig_time.update_layout(title="Ventes dans le temps",
                                   xaxis_title="Date", yaxis_title="Montant Total")
        return html.Div([ dcc.Graph(figure=fig_time) ], style={'padding': '20px'})
    else:
        return html.Div("Sélectionnez un onglet.", style={'padding': '20px'})

# Callback pour mettre à jour la carte du marché (bubble chart) en fonction du marché sélectionné
@app.callback(Output("graph-market", "figure"),
              [Input("market-dropdown", "value")])
def update_market_graph(market_id):
    """
    Met à jour la carte du marché en utilisant un scatter plot sur un repère
    correspondant aux dimensions du marché.
    
    - Le repère (x, y) est défini en fonction de 'taille_x' et 'taille_y' du marché.
    - Les marchands appartenant à ce marché sont affichés avec leur position.
    - Chaque point est annoté avec le nom du marchand.
    """
    # Récupérer le marché sélectionné dans df_markets
    market_list = df_markets[df_markets['market_id'] == market_id].to_dict('records')
    if not market_list:
        fig = go.Figure()
        fig.update_layout(title="Marché non trouvé")
        return fig

    market = market_list[0]
    taille_x = market.get('taille_x', 0)
    taille_y = market.get('taille_y', 0)

    # Filtrer les marchands appartenant à ce marché (en se basant sur la liste d'IDs stockée dans le document)
    market_merchant_ids = market.get('marchands', [])
    df_market_merchants = df_marchands[df_marchands['marchand_id'].isin([str(mid) for mid in market_merchant_ids])]
    if df_market_merchants.empty:
        fig = go.Figure()
        fig.update_layout(title="Aucun marchand dans ce marché")
        return fig

    # Création du scatter plot représentant le marché sur un repère
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_market_merchants['position_x'],
        y=df_market_merchants['position_y'],
        mode='markers+text',
        text=df_market_merchants['nom'],
        textposition='top center',
        marker=dict(
            size=12,       # Taille fixe pour chaque marqueur
            color='blue'   # Couleur des marqueurs
        )
    ))
    fig.update_layout(
        title="Carte du Marché",
        xaxis_title="Coordonnée X",
        yaxis_title="Coordonnée Y",
        xaxis=dict(range=[0, taille_x], dtick=1),
        yaxis=dict(range=[0, taille_y], dtick=1),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

# Callback pour mettre à jour le graphique des produits selon le marchand sélectionné
@app.callback(Output("graph-products", "figure"),
              [Input("merchant-dropdown", "value")])
def update_products_graph(merchant_id):
    if merchant_id is None:
        return {}
    df_filtered = df_produits[df_produits['marchand_id'] == merchant_id]
    if df_filtered.empty:
        fig = go.Figure()
        fig.update_layout(title="Aucun produit trouvé pour ce marchand")
        return fig
    fig = go.Figure(data=[go.Bar(x=df_filtered['produit_nom'], y=df_filtered['quantite'])])
    marchand_nom = df_filtered['marchand_nom'].iloc[0]
    fig.update_layout(
        title=f"Produits de {marchand_nom}",
        xaxis_title="Produit",
        yaxis_title="Quantité"
    )
    return fig

# ------------------------------------------------------------------------------
# Lancement du dashboard dans un processus séparé
# ------------------------------------------------------------------------------

def run_dash_app(port):
    """Lance le serveur Dash sur le port indiqué."""
    app.run_server(host='0.0.0.0', port=port, debug=False)

def launch_dashboard(port=8050):
    """
    Lance le dashboard dans un processus séparé.
    Le processus est démarré et la main est immédiatement rendue à l'utilisateur.
    """
    p = multiprocessing.Process(target=run_dash_app, args=(port,))
    p.start()
    print(f"Dashboard lancé sur le port {port}. Vous pouvez continuer à utiliser le terminal.")
    return p

# ------------------------------------------------------------------------------
# Bloc principal
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Récupération du port via les arguments de la ligne de commande, sinon 8050 par défaut
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = 8050
    else:
        port = 8050

    # Lancer le dashboard dans un processus séparé
    process = launch_dashboard(port)

    # La main est rendue à l'utilisateur : le programme attend une entrée pour quitter
    input("Appuyez sur Entrée pour quitter ce programme (le dashboard continue de fonctionner en arrière-plan)...\n")
