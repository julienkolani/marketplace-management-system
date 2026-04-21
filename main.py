#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module principal de l'application de gestion des marchés, marchands et clients.

Ce module orchestre la navigation entre les différents menus (administrateur, marchand, client)
et intègre la gestion des interruptions (Ctrl+C) ainsi que la journalisation.
"""

import os
import logging
import multiprocessing

# Imports de bibliothèques tierces
from rich.console import Console
from rich.prompt import Prompt

# Imports internes à l'application
from Core.utils import clear_screen, display_welcome_message, display_title, get_user_choice, pause, confirm_action, is_port_available
from Core.tuto import demo_application
from Users.services import login
from Users.views import (
    creer_compte_view,
    rattacher_marchand_marche_view,
    modifier_compte_marchand_view,
    supprimer_compte_marchand_view,
    modifier_utilisateur_view,
    modifier_mon_compte_marchand_view,
    changer_mot_de_passe_view,
    afficher_informations_marchand_view,
    login_view,
    afficher_liste_marchands,
    afficher_liste_tout_utilisateurs,
    supprimer_utilisateur_par_admin_view
)
from Market.views import (
    creer_marche_view,
    afficher_liste_marches,
    supprimer_marche_view,
    modifier_marche_view,
    ajouter_produit_marchand_view,
    retirer_produit_marchand_view,
    modifier_produit_marchand_view,
    afficher_stock_marchand_view,
    afficher_chiffre_affaires_view,
)
from Transactions.views import (
    afficher_panier_view,
    retirer_du_panier_view,
    ajouter_au_panier_view,
    rechercher_et_afficher_produits,
    passer_commande_view,
    afficher_historique_transactions_view,
    afficher_ventes_par_produit_view
)
from Database.models import Client, Marchand, User, Marche

# ======================================================================
# Configuration de la journalisation et initialisation de Rich
# ======================================================================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = Console()

# Compteur global pour la gestion de Ctrl+C
CTRL_C_COUNT = 0

# ======================================================================
# Décorateur pour la gestion de Ctrl+C
# ======================================================================
def catch_ctrl_c(func):
    """
    Décorateur qui intercepte Ctrl+C.
    Si l'utilisateur appuie deux fois sur Ctrl+C, l'application se ferme.
    Sinon, l'utilisateur est redirigé vers le menu principal.
    """
    def wrapper(*args, **kwargs):
        global CTRL_C_COUNT
        try:
            CTRL_C_COUNT = 0  # Réinitialisation à l'entrée de chaque fonction de menu
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            CTRL_C_COUNT += 1
            if CTRL_C_COUNT >= 2:
                console.print("\n[bold red]Double interruption détectée. Fermeture de l'application...[/bold red]")
                exit(0)
            else:
                console.print("\n[bold yellow]Interruption détectée (Ctrl+C). Retour au menu principal...[/bold yellow]")
                menu_principal()
    return wrapper

# ======================================================================
# MENUS PRINCIPAUX
# ======================================================================

@catch_ctrl_c
def menu_principal():
    """
    Affiche le menu principal et gère les choix de l'utilisateur.
    """
    while True:
        clear_screen()
        display_welcome_message()
        display_title("=== MENU PRINCIPAL ===")
        console.print("1. 🔑 Se connecter en tant qu'administrateur")
        console.print("2. 🛒 Se connecter en tant que marchand")
        console.print("3. 👥 Accéder à l'espace client")
        console.print("4. 🎬 Demo de l'application")
        console.print("5. 🚪 Quitter l'application")
        choice = get_user_choice(5)

        if choice == 1:
            user = login("admin")
            if user:
                logging.info("Admin login successful")
                menu_administrateur()
            else:
                console.print("[red]Connexion échouée. Veuillez réessayer.[/red]")
                logging.warning("Admin login failed")
                pause()
        elif choice == 2:
            user = login("marchand")
            if user:
                logging.info("Merchant login successful")
                marchand = Marchand.objects(user=user).first()
                if marchand is None:
                    logging.warning("Cet utilisateur n'est pas un marchand.")
                    console.print("[red]Cet utilisateur n'est pas un marchand. Un admin n'est pas un marchand.[/red]")
                    pause()
                else:
                    menu_marchand(marchand)
            else:
                console.print("[red]Connexion échouée. Veuillez réessayer.[/red]")
                logging.warning("Merchant login failed")
                pause()
        elif choice == 3:
            menu_client()
        elif choice == 4:
            demo_application()
            pause()
        elif choice == 5:
            console.print("[green]Merci d'avoir utilisé l'application. À bientôt ![/green]")
            logging.info("Application exited")
            exit()

# ----------------------------------------------------------------------
# Menu Administrateur
# ----------------------------------------------------------------------
@catch_ctrl_c
def menu_administrateur():
    """
    Menu dédié aux administrateurs pour gérer marchés, marchands, utilisateurs et consulter les rapports.
    """
    while True:
        clear_screen()
        display_title("=== MENU ADMINISTRATEUR ===")
        console.print("1. 🏢 Gérer les marchés")
        console.print("2. 🛍️ Gérer les marchands")
        console.print("3. 👥 Gérer les utilisateurs")
        console.print("4. 📊 Consulter les rapports")
        console.print("5. 🚪 Se déconnecter")
        choice = get_user_choice(5)
        try:
            if choice == 1:
                gerer_marches()
            elif choice == 2:
                gerer_marchands()
            elif choice == 3:
                gerer_utilisateurs()
            elif choice == 4:
                consulter_rapports()
            elif choice == 5:
                if confirm_action("Voulez-vous vraiment vous déconnecter ?"):
                    logging.info("Admin logged out")
                    break  # Retour au menu principal
        except Exception as e:
            console.print(f"[red]Une erreur est survenue : {str(e)}[/red]")
            logging.error(f"Error in menu_administrateur: {str(e)}")
            pause()
    menu_principal()


def gerer_marches():
    """
    Permet à l'administrateur de gérer les marchés.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DES MARCHÉS ===")
        console.print("1. 🆕 Créer un marché")
        console.print("2. 📋 Afficher la liste des marchés")
        console.print("3. ✏️ Modifier un marché")
        console.print("4. ❌ Supprimer un marché")
        console.print("5. 🔙 Retour au menu administrateur")
        choice = get_user_choice(5)
        if choice == 1:
            creer_marche_view()
        elif choice == 2:
            afficher_liste_marches()
        elif choice == 3:
            modifier_marche_view()
        elif choice == 4:
            supprimer_marche_view()
        elif choice == 5:
            break
        pause()


def gerer_marchands():
    """
    Permet à l'administrateur de gérer les marchands.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DES MARCHANDS ===")
        console.print("1. ➕ Ajouter un marchand")
        console.print("2. 📋 Afficher la liste des marchands")
        console.print("3. ✏️ Modifier un marchand")
        console.print("4. ❌ Supprimer un marchand")
        console.print("5. 🔗 Rattacher un marchand à un marché")
        console.print("6. 🔙 Retour au menu administrateur")
        choice = get_user_choice(6)
        try:
            if choice == 1:
                creer_compte_view("marchand")
            elif choice == 2:
                afficher_liste_marchands()
            elif choice == 3:
                modifier_compte_marchand_view()
            elif choice == 4:
                supprimer_compte_marchand_view()
            elif choice == 5:
                rattacher_marchand_marche_view()
            elif choice == 6:
                break
        except Exception as e:
            console.print(f"[red]Erreur : {e}[/red]")
        pause()


def gerer_utilisateurs():
    """
    Permet à l'administrateur de gérer les utilisateurs.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DES UTILISATEURS ===")
        console.print("1. ➕ Ajouter un utilisateur")
        console.print("2. 📋 Afficher la liste des utilisateurs")
        console.print("3. ✏️ Modifier un utilisateur")
        console.print("4. ❌ Supprimer un utilisateur")
        console.print("5. 🔗 Rattacher un marchand à un marché")
        console.print("6. 🔙 Retour au menu administrateur")
        choice = get_user_choice(6)
        if choice == 1:
            role = Prompt.ask("Entrez le rôle de l'utilisateur (admin/marchand/client)").strip().lower()
            if role in ["admin", "marchand", "client"]:
                creer_compte_view(role)
            else:
                console.print("[red]Rôle invalide. Choisissez parmi admin, marchand ou client.[/red]")
        elif choice == 2:
            afficher_liste_tout_utilisateurs()
        elif choice == 3:
            modifier_utilisateur_view()
        elif choice == 4:
            supprimer_utilisateur_par_admin_view()
        elif choice == 5:
            rattacher_marchand_marche_view()
        elif choice == 6:
            break
        pause()

def consulter_rapports():
    """
    Lance l'application des rapports en exécutant une commande système.
    """
    console = Console()
    console.clear()
    console.print("=== RAPPORTS ===", style="bold blue")
    
    while True:
        port = Prompt.ask("Entrez le port sur lequel lancer l'application de rapports (ex: 8050)", default="8050")
        try:
            port_int = int(port)
            if is_port_available(port_int):
                break
            else:
                console.print(f"[red]Le port {port_int} est déjà utilisé. Veuillez en choisir un autre.[/red]")
        except ValueError:
            console.print("[red]Port invalide. Veuillez entrer un numéro valide.[/red]")

    command = f"python Visualization/plots.py --port {port_int}"
    console.print(f"[green]Lancement des rapports sur le port {port_int}...[/green]")
    console.print(f"[blue]Commande exécutée: {command}[/blue]")
    os.system(command)
    input("Appuyez sur CTRL + C pour revenir au menu administrateur...")

# ----------------------------------------------------------------------
# Menu Marchand
# ----------------------------------------------------------------------
@catch_ctrl_c
def menu_marchand(marchand):
    """
    Menu dédié aux marchands pour gérer leur stock, consulter leurs ventes et gérer leur compte.
    """
    while True:
        clear_screen()
        display_title("=== MENU MARCHAND ===")
        console.print("1. 📦 Gérer mon stock")
        console.print("2. 📊 Consulter mes ventes")
        console.print("3. 👤 Gérer mon compte")
        console.print("4. 🚪 Se déconnecter")
        choice = get_user_choice(4)
        if choice == 1:
            gerer_stock(marchand)
        elif choice == 2:
            consulter_ventes(marchand)
        elif choice == 3:
            gerer_compte(marchand)
        elif choice == 4:
            break
        pause()
    menu_principale_redirect()


def gerer_compte(marchand):
    """
    Permet au marchand de modifier ses informations, les afficher ou changer son mot de passe.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DU COMPTE ===")
        console.print("1. ✏️ Modifier mes informations")
        console.print("2. 📋 Afficher mes informations")
        console.print("3. 🔒 Changer mon mot de passe")
        console.print("4. 🔙 Retour au menu marchand")
        choice = get_user_choice(4)
        if choice == 1:
            modifier_mon_compte_marchand_view()
        elif choice == 2:
            afficher_informations_marchand_view(marchand)
        elif choice == 3:
            changer_mot_de_passe_view(marchand)
        elif choice == 4:
            break
        pause()


def gerer_stock(marchand):
    """
    Permet au marchand de gérer son stock : ajouter, afficher, modifier ou retirer un produit.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DU STOCK ===")
        console.print("1. ➕ Ajouter un produit")
        console.print("2. 📋 Afficher mon stock")
        console.print("3. ✏️ Modifier un produit")
        console.print("4. ❌ Retirer un produit")
        console.print("5. 🔙 Retour au menu marchand")
        choice = get_user_choice(5)
        if choice == 1:
            ajouter_produit_marchand_view(marchand)
        elif choice == 2:
            afficher_stock_marchand_view(marchand)
        elif choice == 3:
            modifier_produit_marchand_view(marchand)
        elif choice == 4:
            retirer_produit_marchand_view(marchand)
        elif choice == 5:
            break
        pause()


def consulter_ventes(marchand):
    """
    Permet au marchand de consulter son historique de ventes et son chiffre d'affaires.
    """
    while True:
        clear_screen()
        display_title("=== HISTORIQUE DES VENTES ===")
        console.print("1. 📋 Afficher les ventes par produit")
        console.print("2. 💰 Afficher mon chiffre d'affaires")
        console.print("3. 🔙 Retour au menu marchand")
        choice = get_user_choice(3)
        if choice == 1:
            afficher_ventes_par_produit_view(marchand)
        elif choice == 2:
            afficher_chiffre_affaires_view(marchand)
        elif choice == 3:
            break
        pause()

# ----------------------------------------------------------------------
# Menu Client
# ----------------------------------------------------------------------
@catch_ctrl_c
def menu_client():
    """
    Menu de base pour le client non connecté (connexion ou création de compte).
    """
    clear_screen()
    display_title("=== MENU CLIENT ===")
    console.print("1. 🔑 Se connecter")
    console.print("2. ➕ Créer un compte")
    console.print("3. 🔙 Retour au menu principal")
    choice = get_user_choice(3)
    if choice == 1:
        utilisateur = login_view()
        if utilisateur:
            menu_client_connecte(utilisateur)
        else:
            pause()
    elif choice == 2:
        utilisateur = creer_compte_view("client")
        if utilisateur:
            menu_client_connecte(utilisateur)
        else:
            pause()
    elif choice == 3:
        menu_principal()


@catch_ctrl_c
def menu_client_connecte(client):
    """
    Menu pour un client connecté, proposant la recherche de produits,
    la gestion du panier et la consultation de l'historique d'achats.
    """
    while True:
        clear_screen()
        display_title("=== MENU CLIENT ===")
        console.print("1. 🔍 Rechercher un produit")
        console.print("2. 🛒 Gérer mon panier")
        console.print("3. 📜 Consulter mon historique d'achats")
        console.print("4. 🚪 Se déconnecter")
        choice = get_user_choice(4)
        if choice == 1:
            rechercher_produits(client)
        elif choice == 2:
            gerer_panier(client)
        elif choice == 3:
            consulter_historique_achats(client)
        elif choice == 4:
            break
        pause()
    menu_principale_redirect()


def rechercher_produits(client):
    """
    Permet au client de rechercher des produits par nom.
    """
    clear_screen()
    display_title("=== RECHERCHE DE PRODUITS ===")
    console.print("1. 🔍 Rechercher")
    console.print("2. 🔙 Retour au menu client")
    choice = get_user_choice(2)
    if choice == 1:
        try:
            rechercher_et_afficher_produits(client)
        except ValueError:
            console.print("[red]Veuillez entrer des valeurs numériques valides.[/red]")
    elif choice == 2:
        return
    pause()


def gerer_panier(client):
    """
    Permet au client de gérer son panier :
    ajouter un produit, l'afficher, le retirer ou passer la commande.
    """
    while True:
        clear_screen()
        display_title("=== GESTION DU PANIER ===")
        console.print("1. ➕ Ajouter un produit au panier")
        console.print("2. 📋 Afficher mon panier")
        console.print("3. ❌ Retirer un produit du panier")
        console.print("4. 🛒 Passer la commande")
        console.print("5. 🔙 Retour au menu client")
        choice = get_user_choice(5)
        if choice == 1:
            ajouter_au_panier_view(client)
        elif choice == 2:
            afficher_panier_view(client)
        elif choice == 3:
            retirer_du_panier_view(client)
        elif choice == 4:
            passer_commande_view(client)
        elif choice == 5:
            break
        pause()


def consulter_historique_achats(client):
    """
    Affiche l'historique des achats du client.
    """
    while True:
        clear_screen()
        display_title("=== HISTORIQUE DES ACHATS ===")
        console.print("1. 📋 Afficher mes achats récents")
        console.print("2. 🔙 Retour au menu client")
        choice = get_user_choice(2)
        if choice == 1:
            afficher_historique_transactions_view(client)
        elif choice == 2:
            break
        pause()


def menu_principale_redirect():
    """
    Redirige vers le menu principal après la déconnexion d'un marchand ou d'un client.
    """
    menu_principal()


# ======================================================================
# Fonction principale
# ======================================================================
def main():
    """
    Point d'entrée de l'application.
    """
    display_welcome_message()
    try:
        menu_principal()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Interruption détectée. Fermeture de l'application...[/bold yellow]")
        exit(0)


if __name__ == "__main__":
    main()
