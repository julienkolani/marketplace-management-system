from Database.models import Marche, Marchand, Produit, Client, Transaction
from Core.utils import calculer_distance  # Fonction supposée disponible dans Core.utils

###############################################
# Recherche de produits
###############################################
def rechercher_produits_par_nom(nom_produit, client_x, client_y):
    """
    Recherche des produits dont le nom contient le terme recherché et
    calcule la distance entre le client et le marchand proposant le produit.
    
    :param nom_produit: Nom (ou partie du nom) du produit à rechercher.
    :param client_x: Position X du client.
    :param client_y: Position Y du client.
    :return: Liste de dictionnaires contenant le produit, le marchand et la distance,
             triés par distance croissante.
    """
    produits_trouves = []
    for marche in Marche.objects():
        for marchand in marche.marchands:
            for produit in marchand.produits:
                if nom_produit.lower() in produit.nom.lower():
                    distance = calculer_distance(client_x, client_y, marchand.position_x, marchand.position_y)
                    produits_trouves.append({
                        "produit": produit,
                        "marchand": marchand,
                        "distance": distance,
                    })
    # Trier par distance croissante
    produits_trouves.sort(key=lambda x: x["distance"])
    return produits_trouves


###############################################
# Fonctions pour le panier du client
###############################################
def ajouter_produit_au_panier(client, nom_produit, quantite):
    """
    Ajoute un produit au panier du client à partir de son nom.
    
    :param client: Instance du client.
    :param nom_produit: Nom du produit à ajouter.
    :param quantite: Quantité à ajouter.
    :return: True si le produit a été ajouté.
    :raises ValueError: Si le produit n'est pas trouvé.
    """
    produit_trouve = None
    # Parcourir tous les marchés pour trouver le produit
    for marche in Marche.objects():
        for marchand in marche.marchands:
            for produit in marchand.produits:
                if produit.nom.lower() == nom_produit.lower():
                    produit_trouve = produit
                    break
            if produit_trouve:
                break
        if produit_trouve:
            break

    if produit_trouve:
        client.ajouter_au_panier(produit_trouve.nom, quantite, produit_trouve.prix)
        return True
    else:
        raise ValueError("Produit non trouvé.")


def modifier_quantite_produit_panier(client, nom_produit, nouvelle_quantite):
    """
    Modifie la quantité d'un produit présent dans le panier du client.
    
    :param client: Instance du client.
    :param nom_produit: Nom du produit à modifier.
    :param nouvelle_quantite: Nouvelle quantité.
    :return: True si la modification est effectuée.
    :raises ValueError: Si le produit n'est pas trouvé dans le panier.
    """
    for produit in client.panier:
        if produit.nom.lower() == nom_produit.lower():
            produit.quantite = nouvelle_quantite
            client.save()
            return True
    raise ValueError("Produit non trouvé dans le panier.")


def retirer_produit_du_panier(client, nom_produit):
    """
    Retire un produit du panier du client.
    
    :param client: Instance du client.
    :param nom_produit: Nom du produit à retirer.
    :return: True si le produit a été retiré.
    :raises ValueError: Si le produit n'est pas trouvé dans le panier.
    """
    for produit in client.panier:
        if produit.nom.lower() == nom_produit.lower():
            client.panier.remove(produit)
            client.save()
            return True
    raise ValueError("Produit non trouvé dans le panier.")


###############################################
# Fonctions pour les marchands
###############################################
def ajouter_produit_marchand(marchand, nom, quantite, prix):
    """
    Ajoute un produit au stock du marchand.
    
    :param marchand: Instance du marchand.
    :param nom: Nom du produit.
    :param quantite: Quantité à ajouter.
    :param prix: Prix du produit.
    :return: Le produit ajouté.
    """
    produit = Produit(nom=nom, prix=prix, quantite=quantite)
    marchand.produits.append(produit)
    marchand.save()
    return produit


def retirer_produit_marchand(marchand, nom, quantite):
    """
    Retire une quantité d'un produit du stock du marchand.
    
    :param marchand: Instance du marchand.
    :param nom: Nom du produit.
    :param quantite: Quantité à retirer.
    :raises ValueError: Si la quantité demandée dépasse le stock ou si le produit n'est pas trouvé.
    """
    for produit in marchand.produits:
        if produit.nom.lower() == nom.lower():
            if produit.quantite < quantite:
                raise ValueError(f"Quantité insuffisante pour le produit '{produit.nom}'. Stock disponible : {produit.quantite}")
            produit.quantite -= quantite
            marchand.save()
            return
    raise ValueError(f"Produit '{nom}' non trouvé.")


def afficher_stock_marchand(marchand):
    """
    Retourne le stock du marchand.
    
    :param marchand: Instance du marchand.
    :return: Liste des produits.
    """
    return marchand.produits


###############################################
# Fonctions pour les marchés
###############################################
def creer_marche(nom, taille_x, taille_y):
    """
    Crée un nouveau marché avec le nom et les dimensions spécifiées.
    
    :param nom: Nom du marché.
    :param taille_x: Taille X de la grille.
    :param taille_y: Taille Y de la grille.
    :return: Instance du marché créé.
    """
    marche = Marche(nom=nom, taille_x=taille_x, taille_y=taille_y)
    marche.save()
    return marche


def afficher_marches():
    """
    Récupère la liste de tous les marchés.
    
    :return: QuerySet contenant les marchés.
    """
    return Marche.objects()


def supprimer_marche(nom):
    """
    Supprime un marché à partir de son nom.
    
    :param nom: Nom du marché à supprimer.
    :return: True si le marché a été supprimé.
    :raises ValueError: Si le marché n'est pas trouvé.
    """
    marche = Marche.objects(nom=nom).first()
    if marche:
        marche.delete()
        return True
    else:
        raise ValueError("Marché non trouvé.")


def ajouter_produit(marchand, nom, prix, quantite):
    """
    Ajoute un nouveau produit au stock du marchand.
    
    :param marchand: Instance du marchand.
    :param nom: Nom du produit.
    :param prix: Prix du produit.
    :param quantite: Quantité du produit.
    :return: Le produit ajouté.
    """
    produit = Produit(nom=nom, prix=prix, quantite=quantite)
    marchand.produits.append(produit)
    marchand.save()
    return produit
