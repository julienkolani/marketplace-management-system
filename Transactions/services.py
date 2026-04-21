from mongoengine import (
    connect, disconnect, Document, EmbeddedDocument, StringField, EmailField,
    ListField, EmbeddedDocumentField, FloatField, IntField, DateTimeField,
    ReferenceField, BooleanField, ValidationError, CASCADE
)
from Core.settings import MONGO_URI, MONGO_DB_NAME
from Database.models import Transaction, Marchand, Client, Produit, Marche, Promotion
from datetime import datetime
from Core.utils import calculer_distance  # (exemple d'import utile, à adapter selon votre utils)

# Connexion à MongoDB
connect(db=MONGO_DB_NAME, host=MONGO_URI, alias='default')


# -----------------------------
# Traitement des transactions
# -----------------------------
def passer_commande(client, produits_commande):
    """
    Traite la commande à partir d'une liste de tuples (nom_produit, quantite).
    
    Pour chaque produit, la fonction vérifie :
      - Qu'un marchand le propose (en s'assurant que tous les produits proviennent du même marchand)
      - Que le stock est suffisant
      
    Ensuite :
      - Le stock du marchand est mis à jour
      - La transaction est créée, validée et sauvegardée
      - Les historiques du client et du marchand sont mis à jour
      
    :param client: Instance du client.
    :param produits_commande: Liste de tuples (nom_produit, quantite).
    :return: Instance de la transaction.
    :raises ValueError: Si un produit est introuvable ou si le stock est insuffisant,
                         ou si les produits proviennent de marchands différents.
    """
    marchand_commande = None
    commande_produits = []  # Liste de tuples (produit, quantite)

    # Parcourir les produits commandés (issus du panier)
    for nom, quantite in produits_commande:
        # Rechercher les marchands proposant ce produit (insensible à la casse)
        marchands = Marchand.objects(produits__nom__iexact=nom)
        if not marchands:
            raise ValueError(f"Produit '{nom}' non disponible chez aucun marchand.")

        # Choisir le premier marchand trouvé
        current_marchand = marchands.first()

        # Pour le premier produit, mémoriser le marchand de la commande
        if marchand_commande is None:
            marchand_commande = current_marchand
        # Vérifier que tous les produits proviennent du même marchand
        elif marchand_commande.id != current_marchand.id:
            raise ValueError("Tous les produits commandés doivent provenir du même marchand.")

        # Rechercher le produit dans le marchand choisi
        produit_trouve = None
        for p in current_marchand.produits:
            if p.nom.lower() == nom.lower():
                produit_trouve = p
                break

        if produit_trouve is None:
            raise ValueError(f"Produit '{nom}' non trouvé chez le marchand {current_marchand.nom}.")

        # Vérifier le stock disponible
        if quantite > produit_trouve.quantite:
            raise ValueError(f"Quantité insuffisante pour le produit '{nom}' chez {current_marchand.nom}.")

        commande_produits.append((produit_trouve, quantite))

    # Calcul du montant total et mise à jour des stocks
    total = 0
    for produit, quantite in commande_produits:
        total += produit.prix * quantite
        produit.quantite -= quantite

    # Sauvegarder la mise à jour du stock du marchand
    marchand_commande.save()

    # Créer la transaction
    transaction = Transaction(
        client=client,
        marchand=marchand_commande,  # Ici, le champ 'marchand' (singulier) est utilisé
        produits=[Produit(nom=p.nom, quantite=q, prix=p.prix) for p, q in commande_produits],
        montant_total=total
    )
    # La méthode 'valider_transaction' doit effectuer les vérifications et sauvegarder la transaction
    transaction.valider_transaction()

    # Mettre à jour l'historique du client et du marchand
    client.historique_achats.append(transaction)
    client.save()

    marchand_commande.historique_ventes.append(transaction)
    marchand_commande.save()

    return transaction


def afficher_historique_transactions(client):
    """
    Récupère l'historique des transactions d'un client.
    :param client: Instance du client.
    :return: Liste des transactions.
    """
    return Transaction.objects(client=client)


def afficher_transactions_par_marchand(marchand):
    """
    Récupère les transactions d'un marchand.
    :param marchand: Instance du marchand.
    :return: Liste des transactions.
    """
    return Transaction.objects(marchands__in=[marchand])


def afficher_toutes_transactions():
    """
    Récupère toutes les transactions (réservé aux admins).
    :return: Liste des transactions.
    """
    return Transaction.objects()


# -----------------------------
# Gestion du stock et des promotions
# -----------------------------
def retirer_produit(marchand, nom_produit):
    """
    Permet de retirer un produit du stock du marchand.
    :param marchand: Instance du marchand.
    :param nom_produit: Nom du produit à retirer.
    :return: Produit retiré.
    :raises ValueError: Si le produit n'est pas trouvé.
    """
    produit = next((p for p in marchand.produits if p.nom.lower() == nom_produit.lower()), None)
    if produit:
        marchand.produits.remove(produit)
        marchand.save()
        return produit
    else:
        raise ValueError(f"Produit '{nom_produit}' non trouvé dans votre stock.")


def afficher_stock(marchand):
    """
    Retourne les produits présents dans le stock d'un marchand.
    :param marchand: Instance du marchand.
    :return: Liste des produits.
    """
    return marchand.produits


def afficher_ventes_mois(marchand):
    """
    Récupère les transactions réalisées par un marchand depuis le début du mois.
    :param marchand: Instance du marchand.
    :return: Liste des transactions.
    """
    debut_mois = datetime(datetime.utcnow().year, datetime.utcnow().month, 1)
    transactions = Transaction.objects(marchands__in=[marchand], date__gte=debut_mois)
    return transactions


def ventes_par_produit(marchand):
    """
    Calcule les ventes par produit pour un marchand.
    :param marchand: Instance du marchand.
    :return: Dictionnaire {nom_produit: quantite_vendue}.
    """
    ventes = {}
    transactions = Transaction.objects(marchands__in=[marchand])
    for transaction in transactions:
        for produit in transaction.produits:
            ventes[produit.nom] = ventes.get(produit.nom, 0) + produit.quantite
    return ventes


def creer_promotion(marchand, produit, pourcentage, date_debut, date_fin):
    """
    Crée une promotion sur un produit pour un marchand.
    :param marchand: Instance du marchand.
    :param produit: Produit concerné.
    :param pourcentage: Pourcentage de réduction.
    :param date_debut: Date de début de la promotion.
    :param date_fin: Date de fin de la promotion.
    :return: Instance de la promotion.
    """
    promotion = Promotion(
        produit=produit,
        pourcentage=pourcentage,
        date_debut=date_debut,
        date_fin=date_fin
    )
    marchand.promotions.append(promotion)
    marchand.save()
    return promotion


def afficher_promotions(marchand):
    """
    Retourne les promotions existantes d'un marchand.
    :param marchand: Instance du marchand.
    :return: Liste des promotions.
    """
    return marchand.promotions


def supprimer_promotion(marchand, promotion_id):
    """
    Supprime une promotion pour un marchand.
    :param marchand: Instance du marchand.
    :param promotion_id: Identifiant de la promotion à supprimer.
    :raises ValueError: Si la promotion n'est pas trouvée.
    """
    promotion = next((p for p in marchand.promotions if p.id == promotion_id), None)
    if promotion:
        marchand.promotions.remove(promotion)
        marchand.save()
    else:
        raise ValueError(f"Promotion avec ID {promotion_id} non trouvée.")


# -----------------------------
# Recherche de produits par distance
# -----------------------------
def lister_produits_par_distance(client_x, client_y):
    """
    Liste tous les produits disponibles, triés par distance par rapport à une position donnée.
    :param client_x: Position X du client.
    :param client_y: Position Y du client.
    :return: Liste des dictionnaires contenant 'produit', 'marchand' et 'distance'.
    """
    produits_trouves = []
    for marche in Marche.objects():
        for marchand in marche.marchands:
            for produit in marchand.produits:
                distance = calculer_distance(client_x, client_y, marchand.position_x, marchand.position_y)
                produits_trouves.append({
                    "produit": produit,
                    "marchand": marchand,
                    "distance": distance,
                })
    produits_trouves.sort(key=lambda x: x["distance"])
    return produits_trouves
