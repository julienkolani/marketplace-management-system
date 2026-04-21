from rich.console import Console
from rich.table import Table
from Transactions.services import (
    afficher_historique_transactions,
    afficher_transactions_par_marchand,
    afficher_toutes_transactions,
    retirer_produit,
    ventes_par_produit,
    lister_produits_par_distance,
    passer_commande,
)
from Database.models import Marche, Notification, Client
from Core.utils import clear_screen, display_title, pause, get_user_choice
import datetime
import re

console = Console()


# -----------------------------
# Affichage des transactions
# -----------------------------
def afficher_transactions(transactions, title="Historique des transactions"):
    """Affiche une liste de transactions dans un tableau."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Date", style="dim", width=20)
    table.add_column("Montant total", justify="right")
    table.add_column("Marchands", style="dim", width=30)

    for transaction in transactions:
        marchands = ", ".join([m.nom for m in transaction.marchands])
        table.add_row(
            str(transaction.id),
            transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
            f"{transaction.montant_total:.2f} XOF",
            marchands,
        )
    console.print(table)


def afficher_historique_transactions_view(client):
    """Affiche l'historique des transactions d'un client."""
    transactions = afficher_historique_transactions(client)
    if transactions:
        afficher_transactions(transactions, title="Votre historique des transactions")
    else:
        console.print("[red]Aucune transaction trouvée.[/red]")


def afficher_transactions_marchand_view(marchand):
    """Affiche les transactions d'un marchand."""
    transactions = afficher_transactions_par_marchand(marchand)
    if transactions:
        afficher_transactions(transactions, title=f"Transactions de {marchand.nom}")
    else:
        console.print("[red]Aucune transaction trouvée.[/red]")


def afficher_toutes_transactions_view():
    """Affiche toutes les transactions (réservé aux admins)."""
    transactions = afficher_toutes_transactions()
    if transactions:
        afficher_transactions(transactions, title="Toutes les transactions")
    else:
        console.print("[red]Aucune transaction trouvée.[/red]")


# -----------------------------
# Gestion du stock pour marchands
# -----------------------------
def retirer_produit_marchand_view(marchand):
    """Affiche un formulaire pour retirer un produit du stock."""
    nom_produit = input("Entrez le nom du produit à retirer : ").strip()
    try:
        produit = retirer_produit(marchand, nom_produit)
        console.print(f"[green]Produit '{produit.nom}' retiré du stock avec succès.[/green]")
    except Exception as e:  # Remplace ProduitNonTrouveError par Exception standard
        console.print(f"[red]{e}[/red]")


def afficher_ventes_par_produit_view(marchand):
    """Affiche les ventes par produit pour un marchand."""
    ventes = ventes_par_produit(marchand)
    if ventes:
        table = Table(title="Ventes par Produit", show_header=True, header_style="bold magenta")
        table.add_column("Produit", style="dim", width=30)
        table.add_column("Quantité Vendue", justify="right")
        for produit, quantite in ventes.items():
            table.add_row(produit, str(quantite))
        console.print(table)
    else:
        console.print("[red]Aucune vente par produit trouvée.[/red]")


# -----------------------------
# Affichage et recherche de produits
# -----------------------------
def afficher_produits(produits):
    """Affiche une liste de produits dans un tableau."""
    table = Table(title="Liste des produits", show_header=True, header_style="bold magenta")
    table.add_column("Nom", style="dim", width=20)
    table.add_column("Prix", justify="right")
    table.add_column("Quantité", justify="right")
    table.add_column("Marchand", style="dim", width=20)
    table.add_column("Distance", justify="right")
    for produit_info in produits:
        produit = produit_info["produit"]
        marchand = produit_info["marchand"]
        distance = produit_info["distance"]
        table.add_row(
            produit.nom,
            f"{produit.prix:.2f} XOF",
            str(produit.quantite),
            marchand.nom,
            f"{distance:.2f} unités",
        )
    console.print(table)


def rechercher_et_afficher_produits(client):
    """
    Permet au client de rechercher un produit en choisissant d'abord un marché,
    puis en saisissant le nom du produit. Si le produit n'est pas trouvé dans le marché
    sélectionné, une recherche dans les autres marchés est proposée.
    """
    clear_screen()
    display_title("=== RECHERCHE DE PRODUITS ===")
    
    # Récupérer et afficher la liste des marchés disponibles
    marches = list(Marche.objects())
    if not marches:
        console.print("[red]Aucun marché disponible actuellement.[/red]")
        pause()
        return

    console.print("Liste des marchés disponibles :")
    for index, marche in enumerate(marches, 1):
        console.print(f"{index}. {marche.nom}")
    
    # Sélection du marché
    choix_marche = get_user_choice(len(marches))
    marche_choisie = marches[choix_marche - 1]
    
    # Saisie du nom du produit recherché
    produit_nom = input("Entrez le nom du produit recherché : ").strip()
    
    # Recherche dans les marchands du marché choisi
    resultats = []
    for marchand in marche_choisie.marchands:
        for produit in marchand.produits:
            if produit_nom.lower() in produit.nom.lower():
                resultats.append((marchand, produit))
    
    if resultats:
        console.print("[green]Produit(s) trouvé(s) dans le marché choisi :[/green]")
        for idx, (marchand, produit) in enumerate(resultats, 1):
            console.print(f"{idx}. Marchand : {marchand.nom} - Produit : {produit.nom} - Prix : {produit.prix} - Stock : {produit.quantite}")
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
        else:
            console.print("[red]Produit introuvable dans tous les marchés.[/red]")
    
    pause()


def lister_et_afficher_produits_par_distance(client_x, client_y):
    """Liste et affiche tous les produits disponibles par distance."""
    produits = lister_produits_par_distance(client_x, client_y)
    if produits:
        afficher_produits(produits)
    else:
        console.print("[red]Aucun produit disponible.[/red]")


# -----------------------------
# Gestion du panier du client
# -----------------------------
def afficher_produits_panier(panier):
    """Affiche les produits du panier dans un tableau."""
    table = Table(title="Votre panier", show_header=True, header_style="bold magenta")
    table.add_column("Nom", style="dim", width=20)
    table.add_column("Prix", justify="right")
    table.add_column("Quantité", justify="right")
    for produit in panier:
        table.add_row(
            produit.nom,
            f"{produit.prix:.2f} XOF",
            str(produit.quantite),
        )
    console.print(table)


def _get_client_profile(client):
    """
    Vérifie si l'objet client possède le profil Client et le retourne.
    Si ce n'est pas le cas, tente de le récupérer à partir de l'utilisateur.
    """
    if not hasattr(client, "panier"):
        client_profile = Client.objects(user=client).first()
        if client_profile is None:
            console.print("[red]Profil client introuvable.[/red]")
            pause()
            return None
        return client_profile
    return client


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

    # Demander la quantité à ajouter
    try:
        quantite = int(input(f"Combien de {produit_choisi.nom} souhaitez-vous ajouter ? "))
    except ValueError:
        console.print("[red]Veuillez entrer une quantité numérique valide.[/red]")
        pause()
        return

    if quantite <= 0:
        console.print("[red]La quantité doit être supérieure à zéro.[/red]")
        pause()
        return

    if quantite > produit_choisi.quantite:
        console.print("[red]Quantité insuffisante en stock chez ce marchand.[/red]")
        pause()
        return

    # Ajout du produit au panier du client
    client.ajouter_au_panier(produit_choisi.nom, quantite, produit_choisi.prix)
    console.print(f"[green]{quantite} {produit_choisi.nom}(s) ajouté(s) au panier.[/green]")
    pause()


def afficher_panier_view(client):
    """Affiche le contenu du panier du client."""
    client = _get_client_profile(client)
    if client is None:
        return

    clear_screen()
    display_title("=== PANIER ===")
    if not client.panier:
        console.print("[red]Votre panier est vide.[/red]")
    else:
        console.print("Contenu du panier :")
        for index, produit in enumerate(client.panier, 1):
            console.print(f"{index}. {produit.nom} - Quantité : {produit.quantite} - Prix : {produit.prix}")
    pause()


def retirer_du_panier_view(client):
    """Permet de retirer un produit du panier du client."""
    client = _get_client_profile(client)
    if client is None:
        return

    clear_screen()
    display_title("=== RETIRER UN PRODUIT DU PANIER ===")
    if not client.panier:
        console.print("[red]Votre panier est vide.[/red]")
        pause()
        return

    # Afficher les produits du panier
    for index, produit in enumerate(client.panier, 1):
        console.print(f"{index}. {produit.nom} - Quantité : {produit.quantite} - Prix : {produit.prix}")
    choix_produit = get_user_choice(len(client.panier))
    produit_choisi = client.panier[choix_produit - 1]

    try:
        quantite = int(input(f"Combien de {produit_choisi.nom} souhaitez-vous retirer ? "))
    except ValueError:
        console.print("[red]Veuillez entrer une quantité numérique valide.[/red]")
        pause()
        return

    if quantite > produit_choisi.quantite:
        console.print("[red]Quantité à retirer trop grande.[/red]")
        pause()
        return

    if quantite == produit_choisi.quantite:
        client.retirer_du_panier(produit_choisi.nom)
    else:
        produit_choisi.quantite -= quantite
        client.save()

    console.print(f"[green]{quantite} {produit_choisi.nom}(s) retiré(s) du panier.[/green]")
    pause()


def passer_commande_view(client):
    """
    Permet au client de passer une commande à partir du contenu de son panier.
    La commande met à jour le stock, crée une transaction, vide le panier,
    et envoie une notification indiquant que la transaction a été effectuée.
    """
    client = _get_client_profile(client)
    if client is None:
        return

    clear_screen()
    display_title("=== PASSER LA COMMANDE ===")
    if not client.panier:
        console.print("[red]Votre panier est vide.[/red]")
        pause()
        return

    # Construire la commande à partir du panier
    produits_commande = [(produit.nom, produit.quantite) for produit in client.panier]

    try:
        transaction = passer_commande(client, produits_commande)
        console.print(f"[green]Commande passée avec succès ! ID de la transaction : {transaction.id}[/green]")
        # Vider le panier
        client.vider_panier()
        # Envoyer une notification au client
        notification = Notification(
            utilisateur=client.user,
            message="Transaction effectuée avec succès."
        )
        notification.save()
    except Exception as e:
        console.print(f"[red]{e}[/red]")
    pause()
