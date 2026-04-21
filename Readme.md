## Partie 1 : Conception et Programmation

---

### 1. Créer un espace marché avec une structure spatiale définie

**Description :**
Construire une représentation logique du marché sous forme d’un repère 2D (par exemple, une grille cartésienne). Chaque marchand doit être assigné à une position unique ((x, y)).

**Fonctionnalités attendues :**

- Créer un espace de taille configurable (exemple : (10×10) ou (50×50)).
- Assurer que les emplacements attribués aux marchands soient uniques.

**À rendre :**

- Le code de la classe ou des fonctions permettant de définir cet espace.
- Une démonstration du placement des marchands avec quelques cas de test.

**Réponse :**

```python

class Marche(Document):
    """
    Modèle représentant un marché avec une grille définie et des marchands associés.
    """
    nom = StringField(required=True, max_length=100)
    taille_x = IntField(required=True, min_value=1)
    taille_y = IntField(required=True, min_value=1)
    marchands = ListField(ReferenceField(Marchand))

    def est_emplacement_libre(self, x: int, y: int) -> bool:
        for marchand in self.marchands:
            if marchand.position_x == x and marchand.position_y == y:
                return False
        return True

    def ajouter_marchand(self, marchand: Marchand, x: int, y: int) -> bool:
        if not self.est_emplacement_libre(x, y):
            return False
        marchand.position_x = x
        marchand.position_y = y
        marchand.save() 
        self.marchands.append(marchand)
        self.save()
        return True


    def afficher_grille_plotly(self):
        grille = [[0 for _ in range(self.taille_x)] for _ in range(self.taille_y)]
        for marchand in self.marchands:
            if 0 <= marchand.position_y < self.taille_y and 0 <= marchand.position_x < self.taille_x:
                grille[marchand.position_y][marchand.position_x] = 1

        fig = go.Figure(data=go.Heatmap(z=grille, colorscale="Viridis"))
        fig.update_layout(title="Carte du marché")
        plot(fig, filename="marche.html")


```

---

### 2. Définir un marchand et gérer ses informations

**Description :**
Créer un modèle pour représenter un marchand, incluant son identité, son stock (produits, quantités, prix) et sa localisation dans le marché.

**Fonctionnalités attendues :**

- Une classe représentant le marchand, avec des attributs tels que le nom, le stock et la position dans le marché.
- Des méthodes pour mettre à jour le stock (ajouter, retirer) et pour afficher les informations.
- Historique des ventes et statistiques par marchand.

**À rendre :**

- Le code de la classe avec des exemples d’instances de marchands.
- Des tests d’ajouts/retraits de stock.

**Réponse :**

```python

class User(Document):
    """
    Modèle représentant un utilisateur (admin, marchand ou client).
    """
    username = StringField(required=True, unique=True, max_length=50)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    role = StringField(required=True, choices=['admin', 'marchand', 'client'])
    date_inscription = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['username', 'email'],
    }

    def set_password(self, password: str):
        """Hash et stocke le mot de passe en utilisant bcrypt."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Vérifie le mot de passe par rapport au hash stocké."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_notifications(self):
        """Récupère les notifications non lues de l'utilisateur."""
        return Notification.objects(utilisateur=self, lue=False)

    def clean(self):
        """
        Validation personnalisée avant l'enregistrement.
        Le nom d'utilisateur ne doit contenir que des lettres et des chiffres.
        """
        if not self.username.isalnum():
            raise ValidationError("Le nom d'utilisateur ne doit contenir que des lettres et des chiffres.")

class Marchand(Document):
    """
    Modèle représentant un marchand, associé à un utilisateur.
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    # On synchronisera ici le nom avec le username de l'utilisateur
    nom = StringField(required=True, max_length=100)
    position_x = IntField(required=True, min_value=0)
    position_y = IntField(required=True, min_value=0)
    produits = ListField(EmbeddedDocumentField(Produit))
    historique_ventes = ListField(ReferenceField('Transaction'))
    promotions = ListField(EmbeddedDocumentField(Promotion))

    meta = {
        'indexes': ['user', 'position_x', 'position_y'],
    }

    def ajouter_produit(self, nom: str, quantite: int, prix: float):
        produit = Produit(nom=nom, quantite=quantite, prix=prix)
        self.produits.append(produit)
        self.save()

    def retirer_produit(self, nom: str, quantite: int) -> bool:
        for produit in self.produits:
            if produit.nom == nom:
                if produit.quantite >= quantite:
                    produit.quantite -= quantite
                    if produit.quantite == 0:
                        self.produits.remove(produit)
                    self.save()
                    return True
                else:
                    return False
        return False

    def appliquer_promotion(self, produit_nom: str, reduction: float) -> bool:
        for produit in self.produits:
            if produit.nom == produit_nom:
                promotion = Promotion(produit=produit, pourcentage=reduction)
                self.promotions.append(promotion)
                self.save()
                return True
        return False

    def get_stock_total(self) -> int:
        return sum(produit.quantite for produit in self.produits)

    def get_chiffre_affaires(self) -> float:
        return sum(transaction.montant_total for transaction in self.historique_ventes)


```

---

### 3. Ajouter des marchands à un marché

**Description :**
Développer un mécanisme pour insérer un marchand dans l’espace du marché.

**Fonctionnalités attendues :**

- Une fonction permettant d’ajouter un marchand tout en vérifiant que sa position dans le marché est libre.
- Une gestion des erreurs si l’emplacement est déjà occupé.

**À rendre :**

- Le code de la fonction d’ajout.
- Des tests associés.

**Réponse :**

```python



def creer_compte_view(role):
    """
    Affiche le formulaire de création de compte en fonction du rôle.
    Si le rôle est "marchand", propose également de rattacher le marchand à un marché.
    """
    username = input("Entrez un nom d'utilisateur : ").strip()
    email = input("Entrez votre adresse email : ").strip()
    password = input("Entrez un mot de passe : ").strip()

    try:
        # Vérifier si l'email est valide
        if not est_email_valide(email):
            console.print(f"[red]L'email '{email}' n'est pas valide.[/red]")
            return

        # Vérifier si l'utilisateur ou l'email existe déjà
        if User.objects(username=username).first():
            console.print(f"[red]Le nom d'utilisateur '{username}' est déjà pris.[/red]")
            return
        if User.objects(email=email).first():
            console.print(f"[red]L'email '{email}' est déjà utilisé.[/red]")
            return

        # Créer le compte
        user = creer_compte(username, email, password, role)
        console.print(f"[green]Compte {role} créé avec succès ! Bienvenue, {user.username}.[/green]")

        # Si le compte créé correspond à un marchand, proposer de le rattacher à un marché
        if role == "marchand":
            rattacher = input("Voulez-vous rattacher ce marchand à un marché maintenant ? (o/n) : ").strip().lower()
            if rattacher == 'o':
                rattacher_marchand_marche_view(user)
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def rattacher_marchand_marche_view(user=None):
    """
    Rattache un marchand à un marché.
    Si aucun utilisateur n'est fourni, demande le nom d'utilisateur du marchand à rattacher.
    """
    try:
        # Si aucun utilisateur n'est fourni, demander le nom d'utilisateur
        if user is None:
            afficher_liste_marchands()
            username = input("Entrez le nom d'utilisateur du marchand à rattacher : ").strip()
            if not username:
                console.print("[red]Le nom d'utilisateur ne peut pas être vide.[/red]")
                return
            user = User.objects(username=username, role="marchand").first()
            if not user:
                console.print(f"[red]Aucun marchand trouvé avec le nom '{username}'.[/red]")
                return

        # Afficher la liste des marchés disponibles
        marches = Marche.objects()
        if not marches:
            console.print("[red]Aucun marché disponible.[/red]")
            return

        console.print("Liste des marchés disponibles :")
        for i, marche in enumerate(marches, start=1):
            console.print(f"{i}. {marche.nom} (Taille : {marche.taille_x}x{marche.taille_y})")

        # Demander à l'utilisateur de choisir un marché
        choix = int(input("Choisissez un marché (numéro) : "))
        if choix < 1 or choix > len(marches):
            console.print("[red]Choix invalide.[/red]")
            return

        marche = marches[choix - 1]

        # Demander les coordonnées dans la grille
        position_x = int(input("Entrez la position X dans la grille : "))
        position_y = int(input("Entrez la position Y dans la grille : "))

        # Vérifier si l'emplacement est libre
        if not marche.est_emplacement_libre(position_x, position_y):
            console.print("[red]L'emplacement est déjà occupé.[/red]")
            return

        # Créer ou mettre à jour le marchand et le rattacher au marché
        marchand = Marchand.objects(user=user).first()
        if not marchand:
            marchand = Marchand(user=user, nom=user.username)
        marchand.position_x = position_x
        marchand.position_y = position_y
        marchand.save()
        marche.ajouter_marchand(marchand, position_x, position_y)
        console.print(f"[green]Marchand rattaché au marché '{marche.nom}' avec succès ![/green]")

    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides.[/red]")


```

---

### 4. Générer une carte interactive des emplacements des marchands

**Description :**
Produire une visualisation graphique montrant les positions des marchands dans l’espace du marché.

**Fonctionnalités attendues :**

- Une carte interactive en 2D où chaque marchand est représenté par un point.
- Utilisation de couleurs pour indiquer l’état des stocks (vert : stock élevé, orange : moyen, rouge : faible).
- Annotation de chaque point avec le nom du marchand.

**À rendre :**

- Un graphique produit avec Matplotlib ou Plotly.
- Le code pour générer cette visualisation.

**Réponse :**

```python

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


```

---

### 5. Optimisation des achats pour un client

**Description :**
Permettre à un acheteur de trouver les marchands les plus adaptés pour ses besoins.

**Fonctionnalités attendues :**

- Une fonction prenant en entrée une liste de produits souhaités et leurs quantités.
- Recherche des marchands ayant ces produits, en optimisant par distance (calculée via la distance euclidienne ou une autre distance adaptée) et par prix.
- Retour des marchands recommandés, avec leurs coordonnées, le coût total, et une mise à jour graphique de la carte.

**À rendre :**

- Le code de la fonction.
- Un exemple d’utilisation avec un cas concret simulé.

**Réponse :**

```python

def ajouter_au_panier_view(client):
    """
    Permet d'ajouter un produit au panier du client.
    Deux modes sont disponibles :
      1. Par parcours (sélection du marché, marchand puis produit)
      2. Par recherche (recherche par nom, éventuellement dans plusieurs marchés)
    """
    client = _get_client_profile(client)
    if client is None:
        return

    clear_screen()
    display_title("=== AJOUTER UN PRODUIT AU PANIER ===")
  
    console.print("Choisissez le mode d'ajout :")
    console.print("1. Par parcours")
    console.print("2. Par recherche")
    mode = get_user_choice(2)
  
    # --- Mode 1 : Par parcours ---
    if mode == 1:
        marches = list(Marche.objects())
        if not marches:
            console.print("[red]Aucun marché disponible actuellement.[/red]")
            pause()
            return

        console.print("Liste des marchés disponibles :")
        for index, marche in enumerate(marches, 1):
            console.print(f"{index}. {marche.nom}")
        choix_marche = get_user_choice(len(marches))
        marche_choisie = marches[choix_marche - 1]

        if not marche_choisie.marchands:
            console.print(f"[red]Aucun marchand n'est présent dans le marché {marche_choisie.nom}.[/red]")
            pause()
            return

        console.print(f"Marchands présents dans le marché {marche_choisie.nom} :")
        for index, marchand in enumerate(marche_choisie.marchands, 1):
            console.print(f"{index}. {marchand.nom}")
        choix_marchand = get_user_choice(len(marche_choisie.marchands))
        marchand_choisi = marche_choisie.marchands[choix_marchand - 1]

        if not marchand_choisi.produits:
            console.print(f"[red]Aucun produit disponible chez {marchand_choisi.nom}.[/red]")
            pause()
            return

        console.print(f"Produits disponibles chez {marchand_choisi.nom} :")
        for index, produit in enumerate(marchand_choisi.produits, 1):
            console.print(f"{index}. {produit.nom} - Prix : {produit.prix} - Stock : {produit.quantite}")
        choix_produit = get_user_choice(len(marchand_choisi.produits))
        produit_choisi = marchand_choisi.produits[choix_produit - 1]

    # --- Mode 2 : Par recherche ---
    elif mode == 2:
        marches = list(Marche.objects())
        if not marches:
            console.print("[red]Aucun marché disponible actuellement.[/red]")
            pause()
            return

        console.print("Liste des marchés disponibles :")
        for index, marche in enumerate(marches, 1):
            console.print(f"{index}. {marche.nom}")
        choix_marche = get_user_choice(len(marches))
        marche_choisie = marches[choix_marche - 1]
      
        produit_nom = input("Entrez le nom du produit recherché : ").strip()
      
        # Recherche dans le marché choisi
        resultats = []
        for marchand in marche_choisie.marchands:
            for produit in marchand.produits:
                if produit_nom.lower() in produit.nom.lower():
                    resultats.append((marchand, produit))
      
        if resultats:
            console.print("[green]Produit(s) trouvé(s) dans le marché choisi :[/green]")
            for idx, (marchand, produit) in enumerate(resultats, 1):
                console.print(f"{idx}. Marchand : {marchand.nom} - Produit : {produit.nom} - Prix : {produit.prix} - Stock : {produit.quantite}")
            choix_resultat = get_user_choice(len(resultats))
            marchand_choisi, produit_choisi = resultats[choix_resultat - 1]
        else:
            console.print(f"[yellow]Produit non trouvé dans le marché {marche_choisie.nom}.[/yellow]")
            # Recherche dans les autres marchés
            autres_resultats = []
            for marche in marches:
                if marche == marche_choisie:
                    continue
                for marchand in marche.marchands:
                    for produit in marchand.produits:
                        if produit_nom.lower() in produit.nom.lower():
                            autres_resultats.append((marche, marchand, produit))
            if autres_resultats:
                console.print("[green]Produit trouvé dans d'autres marchés :[/green]")
                for idx, (marche, marchand, produit) in enumerate(autres_resultats, 1):
                    console.print(f"{idx}. Marché : {marche.nom} - Marchand : {marchand.nom} - Produit : {produit.nom} - Prix : {produit.prix} - Stock : {produit.quantite}")
                choix_resultat = get_user_choice(len(autres_resultats))
                # On récupère le marchand et le produit choisis
                _, marchand_choisi, produit_choisi = autres_resultats[choix_resultat - 1]
            else:
                console.print("[red]Produit introuvable dans tous les marchés.[/red]")
                pause()
                return


```
