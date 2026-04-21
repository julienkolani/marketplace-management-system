from rich.console import Console
from rich.table import Table
from Market.services import (
    creer_marche,
    afficher_marches,
    supprimer_marche,
    ajouter_produit,
)
from Database.models import Client, Marchand, Marche, Produit, Promotion, Transaction, Notification
from datetime import datetime
from Core.utils import clear_screen, display_title, pause, get_user_choice

console = Console()

###############################################
# Gestion des marchés
###############################################
def creer_marche_view():
    """
    Vue pour créer un nouveau marché.
    Demande le nom du marché et les dimensions de la grille, puis crée le marché.
    """
    try:
        nom = input("Entrez le nom du marché : ").strip()
        if not nom:
            console.print("[red]Le nom du marché ne peut pas être vide.[/red]")
            return

        if Marche.objects(nom=nom).first():
            console.print(f"[red]Un marché avec le nom '{nom}' existe déjà.[/red]")
            return

        taille_x = int(input("Entrez la taille X de la grille : "))
        taille_y = int(input("Entrez la taille Y de la grille : "))
        if taille_x <= 0 or taille_y <= 0:
            console.print("[red]Les dimensions doivent être des entiers positifs.[/red]")
            return

        creer_marche(nom, taille_x, taille_y)
        console.print("[green]Marché créé avec succès ![/green]")

    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides pour les dimensions.[/red]")


def afficher_liste_marches():
    """
    Affiche la liste des marchés existants sous forme de tableau.
    """
    marches = afficher_marches()
    if marches:
        table = Table(title="Liste des marchés", show_header=True, header_style="bold magenta")
        table.add_column("Nom", style="dim", width=20)
        table.add_column("Taille X", justify="right")
        table.add_column("Taille Y", justify="right")
        for marche in marches:
            table.add_row(marche.nom, str(marche.taille_x), str(marche.taille_y))
        console.print(table)
    else:
        console.print("[yellow]Aucun marché trouvé.[/yellow]")


def modifier_marche_view():
    """
    Vue pour modifier un marché existant.
    Permet de changer le nom et/ou les dimensions de la grille.
    """
    try:
        afficher_liste_marches()
        ancien_nom = input("Entrez le nom du marché à modifier : ").strip()
        if not ancien_nom:
            console.print("[red]Le nom du marché ne peut pas être vide.[/red]")
            return

        marche = Marche.objects(nom=ancien_nom).first()
        if not marche:
            console.print(f"[red]Aucun marché trouvé avec le nom '{ancien_nom}'.[/red]")
            return

        nouveau_nom = input("Entrez le nouveau nom du marché (laissez vide pour ne pas changer) : ").strip()
        if nouveau_nom:
            if Marche.objects(nom=nouveau_nom).first():
                console.print(f"[red]Un marché avec le nom '{nouveau_nom}' existe déjà.[/red]")
                return
            marche.nom = nouveau_nom

        nouvelle_taille_x = input("Entrez la nouvelle taille X de la grille (laissez vide pour ne pas changer) : ").strip()
        nouvelle_taille_y = input("Entrez la nouvelle taille Y de la grille (laissez vide pour ne pas changer) : ").strip()

        if nouvelle_taille_x:
            nouvelle_taille_x = int(nouvelle_taille_x)
            if nouvelle_taille_x <= 0:
                console.print("[red]La taille X doit être un entier positif.[/red]")
                return
            marche.taille_x = nouvelle_taille_x

        if nouvelle_taille_y:
            nouvelle_taille_y = int(nouvelle_taille_y)
            if nouvelle_taille_y <= 0:
                console.print("[red]La taille Y doit être un entier positif.[/red]")
                return
            marche.taille_y = nouvelle_taille_y

        marche.save()
        console.print("[green]Marché modifié avec succès ![/green]")

    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides pour les dimensions.[/red]")


def supprimer_marche_view():
    """
    Vue pour supprimer un marché existant.
    Affiche la liste des marchés, demande le nom du marché à supprimer et le supprime.
    """
    marches = afficher_marches()
    if not marches:
        console.print("[red]Aucun marché à supprimer.[/red]")
        return

    console.print("[blue]Voici la liste des marchés disponibles :[/blue]")
    afficher_liste_marches()
    nom = input("Entrez le nom du marché à supprimer : ").strip()
    if not nom:
        console.print("[red]Le nom du marché ne peut pas être vide.[/red]")
        return

    try:
        supprimer_marche(nom)
        console.print(f"[green]Le marché '{nom}' a été supprimé avec succès ![/green]")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")


###############################################
# Gestion du stock (Produits)
###############################################
def ajouter_produit_marchand_view(marchand):
    """
    Vue pour ajouter un produit au stock du marchand.
    Demande le nom, le prix et la quantité, puis ajoute le produit.
    """
    nom = input("Entrez le nom du produit : ").strip()
    try:
        prix = float(input("Entrez le prix du produit : "))
        quantite = int(input("Entrez la quantité du produit : "))
        produit = ajouter_produit(marchand, nom, prix, quantite)
        console.print(f"[green]Produit '{produit.nom}' ajouté avec succès au stock ![/green]")
    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides pour le prix et la quantité.[/red]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def retirer_produit_marchand_view(marchand):
    """
    Vue pour retirer un produit (ou une quantité d'un produit) du stock du marchand.
    Affiche d'abord le stock, puis demande le nom du produit et la quantité à retirer.
    """
    if not marchand.produits:
        console.print("[red]Votre stock est vide.[/red]")
        return

    afficher_stock_marchand_view(marchand)

    try:
        nom = input("Entrez le nom du produit à retirer : ").strip()
        quantite = int(input("Entrez la quantité à retirer : "))
        produit = next((p for p in marchand.produits if p.nom == nom), None)
        if not produit:
            console.print(f"[red]Produit '{nom}' non trouvé.[/red]")
            return
        if produit.quantite < quantite:
            console.print(f"[red]Quantité insuffisante. Stock actuel : {produit.quantite}[/red]")
            return

        produit.quantite -= quantite
        if produit.quantite == 0:
            marchand.produits.remove(produit)
            console.print(f"[green]Produit '{nom}' retiré du stock.[/green]")
        else:
            console.print(f"[green]Quantité mise à jour pour le produit '{nom}'.[/green]")

        marchand.save()
    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides.[/red]")


def modifier_produit_marchand_view(marchand):
    """
    Vue pour modifier un produit existant dans le stock du marchand.
    Affiche le stock, demande le nom du produit à modifier et les nouvelles valeurs.
    """
    if not marchand.produits:
        console.print("[red]Votre stock est vide.[/red]")
        return

    afficher_stock_marchand_view(marchand)
    try:
        nom = input("Entrez le nom du produit à modifier : ").strip()
        produit = next((p for p in marchand.produits if p.nom == nom), None)
        if not produit:
            console.print(f"[red]Produit '{nom}' non trouvé.[/red]")
            return

        nouveau_nom = input(f"Entrez le nouveau nom (actuel : {produit.nom}) : ").strip()
        nouvelle_quantite = input(f"Entrez la nouvelle quantité (actuelle : {produit.quantite}) : ").strip()
        nouveau_prix = input(f"Entrez le nouveau prix (actuel : {produit.prix}) : ").strip()

        if nouveau_nom:
            produit.nom = nouveau_nom
        if nouvelle_quantite:
            produit.quantite = int(nouvelle_quantite)
        if nouveau_prix:
            produit.prix = float(nouveau_prix)

        marchand.save()
        console.print(f"[green]Produit '{nom}' modifié avec succès.[/green]")
    except ValueError:
        console.print("[red]Veuillez entrer des valeurs valides.[/red]")


def afficher_stock_marchand_view(marchand):
    """
    Affiche le stock du marchand sous forme de tableau.
    """
    if not marchand.produits:
        console.print("[red]Votre stock est vide.[/red]")
        return

    table = Table(title="Stock du Marchand", show_header=True, header_style="bold magenta")
    table.add_column("Nom", style="dim", width=20)
    table.add_column("Quantité", justify="right")
    table.add_column("Prix unitaire", justify="right")
    for produit in marchand.produits:
        table.add_row(produit.nom, str(produit.quantite), f"{produit.prix} XOF")
    console.print(table)


###############################################
# Affichage des ventes et du chiffre d'affaires
###############################################
def afficher_chiffre_affaires_view(marchand):
    """
    Affiche le chiffre d'affaires total du marchand.
    """
    try:
        chiffre_affaires = marchand.get_chiffre_affaires()
        console.print(f"[bold green]Votre chiffre d'affaires total est de : {chiffre_affaires:.2f} XOF[/bold green]")
    except Exception as e:
        console.print(f"[red]Erreur : {e}[/red]")


def afficher_ventes_mois_view(marchand):
    """
    Affiche les ventes du mois pour le marchand sous forme de tableau.
    """
    try:
        maintenant = datetime.now()
        mois_actuel = maintenant.month
        annee_actuelle = maintenant.year

        transactions = Transaction.objects(
            marchand=marchand,
            date__gte=datetime(annee_actuelle, mois_actuel, 1),
            date__lt=datetime(annee_actuelle, mois_actuel + 1, 1) if mois_actuel < 12 else datetime(annee_actuelle + 1, 1, 1)
        )

        if not transactions:
            console.print("[red]Aucune vente ce mois-ci.[/red]")
            return

        table = Table(title=f"Ventes du Mois {mois_actuel}/{annee_actuelle}", show_header=True, header_style="bold magenta")
        table.add_column("Date", style="dim", width=20)
        table.add_column("Produit", style="dim", width=20)
        table.add_column("Quantité", justify="right")
        table.add_column("Montant (XOF)", justify="right")

        total_mois = 0
        for transaction in transactions:
            for produit in transaction.produits:
                montant = produit.prix * produit.quantite
                table.add_row(
                    transaction.date.strftime("%Y-%m-%d"),
                    produit.nom,
                    str(produit.quantite),
                    f"{montant:.2f} XOF"
                )
                total_mois += montant

        console.print(table)
        console.print(f"[bold green]Total des ventes du mois : {total_mois:.2f} XOF[/bold green]")
    except Exception as e:
        console.print(f"[red]Erreur : {e}[/red]")


def afficher_ventes_par_produit_view(marchand):
    """
    Affiche les ventes regroupées par produit pour le marchand sous forme de tableau.
    """
    try:
        transactions = Transaction.objects(marchand=marchand)
        if not transactions:
            console.print("[red]Aucune vente enregistrée.[/red]")
            return

        ventes_par_produit = {}
        for transaction in transactions:
            for produit in transaction.produits:
                if produit.nom in ventes_par_produit:
                    ventes_par_produit[produit.nom]["quantite"] += produit.quantite
                    ventes_par_produit[produit.nom]["montant"] += produit.prix * produit.quantite
                else:
                    ventes_par_produit[produit.nom] = {
                        "quantite": produit.quantite,
                        "montant": produit.prix * produit.quantite
                    }

        table = Table(title="Ventes par Produit", show_header=True, header_style="bold magenta")
        table.add_column("Produit", style="dim", width=20)
        table.add_column("Quantité Vendue", justify="right")
        table.add_column("Montant Total (XOF)", justify="right")
        for produit, details in ventes_par_produit.items():
            table.add_row(
                produit,
                str(details["quantite"]),
                f"{details['montant']:.2f} XOF"
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Erreur : {e}[/red]")
