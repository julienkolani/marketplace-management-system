from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    EmailField,
    ListField,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField,
    BooleanField,
    connect,
    ValidationError,
    CASCADE,
    signals
)
import bcrypt
from datetime import datetime
import plotly.graph_objects as go
from plotly.offline import plot
from Core.settings import MONGO_URI, MONGO_DB_NAME

# ------------------------------------------------------------------------------
# Connexion à MongoDB
# ------------------------------------------------------------------------------
connect(db=MONGO_DB_NAME, host=MONGO_URI, alias='default')

# ------------------------------------------------------------------------------
# Modèle User
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Modèle Produit (EmbeddedDocument)
# ------------------------------------------------------------------------------
class Produit(EmbeddedDocument):
    """
    Modèle représentant un produit.
    """
    nom = StringField(required=True, max_length=100)
    quantite = IntField(required=True, min_value=0)
    prix = FloatField(required=True, min_value=0)


# ------------------------------------------------------------------------------
# Modèle Promotion (EmbeddedDocument)
# ------------------------------------------------------------------------------
class Promotion(EmbeddedDocument):
    """
    Modèle représentant une promotion appliquée sur un produit.
    """
    produit = EmbeddedDocumentField(Produit, required=True)
    pourcentage = FloatField(required=True, min_value=0, max_value=100)
    date_debut = DateTimeField(default=datetime.utcnow)
    date_fin = DateTimeField()

    def clean(self):
        """
        Validation personnalisée pour la promotion.
        Le pourcentage doit être entre 0 et 100 et la date de fin doit être postérieure à la date de début.
        """
        if self.pourcentage < 0 or self.pourcentage > 100:
            raise ValidationError("Le pourcentage de réduction doit être compris entre 0 et 100%.")
        if self.date_fin and self.date_fin <= self.date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")


# ------------------------------------------------------------------------------
# Modèle Marchand
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Modèle Client
# ------------------------------------------------------------------------------
class Client(Document):
    """
    Modèle représentant un client, associé à un utilisateur.
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    nom = StringField(required=True, max_length=100)
    panier = ListField(EmbeddedDocumentField(Produit))
    historique_achats = ListField(ReferenceField('Transaction'))

    def ajouter_au_panier(self, nom: str, quantite: int, prix: float):
        produit = Produit(nom=nom, quantite=quantite, prix=prix)
        self.panier.append(produit)
        self.save()

    def retirer_du_panier(self, nom: str) -> bool:
        for produit in self.panier:
            if produit.nom == nom:
                self.panier.remove(produit)
                self.save()
                return True
        return False

    def vider_panier(self):
        self.panier.clear()
        self.save()


# ------------------------------------------------------------------------------
# Modèle Transaction
# ------------------------------------------------------------------------------
class Transaction(Document):
    """
    Modèle représentant une transaction entre un client et un marchand.
    """
    client = ReferenceField(Client, required=True, reverse_delete_rule=CASCADE)
    marchand = ReferenceField(Marchand, required=True, reverse_delete_rule=CASCADE)
    produits = ListField(EmbeddedDocumentField(Produit))
    montant_total = FloatField(required=True)
    date = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['client', 'marchand', 'date'],
    }

    def valider_transaction(self):
        total = 0
        for produit in self.produits:
            if produit.quantite > 0:
                total += produit.prix * produit.quantite
        self.montant_total = total

        if total <= 0:
            raise ValidationError("La transaction est invalide (montant total nul ou négatif).")
        self.save()


# ------------------------------------------------------------------------------
# Modèle Notification
# ------------------------------------------------------------------------------
class Notification(Document):
    """
    Modèle représentant une notification destinée à un utilisateur.
    """
    utilisateur = ReferenceField(User, required=True, reverse_delete_rule=CASCADE)
    message = StringField(required=True, max_length=500)
    date = DateTimeField(default=datetime.utcnow)
    lue = BooleanField(default=False)

    def marquer_comme_lue(self):
        self.lue = True
        self.save()


# ------------------------------------------------------------------------------
# Modèle Marche
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
# Signal de synchronisation des profils
# ------------------------------------------------------------------------------
def sync_profiles(sender, document, **kwargs):
    """
    Synchronise les documents Marchand et Client en fonction du rôle de l'utilisateur.
      - Pour un utilisateur de rôle 'admin' ou 'marchand', on s'assure qu'un document Marchand existe.
      - Pour tous les rôles, on s'assure qu'un document Client existe.
    """
    # --- Gestion du profil Marchand ---
    marchand = Marchand.objects(user=document).first()
    if document.role in ['admin', 'marchand']:
        if not marchand:
            # On peut initialiser position_x et position_y à des valeurs par défaut (ici 0)
            marchand = Marchand(user=document, nom=document.username, position_x=0, position_y=0)
        else:
            # Synchronisation du champ nom
            marchand.nom = document.username
        marchand.save()
    else:
        # Si le rôle n'est pas marchand ou admin, on supprime le document Marchand s'il existe
        if marchand:
            marchand.delete()

    # --- Gestion du profil Client ---
    client = Client.objects(user=document).first()
    if not client:
        client = Client(user=document, nom=document.username)
    else:
        client.nom = document.username
    client.save()


# Connecter le signal post_save sur le modèle User
signals.post_save.connect(sync_profiles, sender=User)
