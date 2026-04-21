import time
from rich.console import Console

console = Console()

def demo_application():
    """
    Fonction de démonstration interactive qui guide l'utilisateur à travers
    l'ensemble des menus et sous-menus de l'application.
    
    Un effet "typing" est simulé en affichant les messages avec des délais, et
    l'utilisateur est invité à appuyer sur Entrée à chaque étape pour continuer.
    """
    console.clear()
    console.print("[bold blue]Bienvenue dans la démonstration interactive de l'application de gestion des marchés ![/bold blue]\n")
    time.sleep(2)
    
    # Introduction générale
    messages_intro = [
        "Cette application permet de gérer les marchés, les marchands et les clients.",
        "Vous pouvez vous connecter en tant qu'administrateur, marchand ou client.",
        "Chaque rôle dispose d'un menu personnalisé avec de nombreuses fonctionnalités.",
        "",
        "Pour la démonstration, nous allons simuler une session complète en passant par chacun des menus.",
        "Par exemple, pour vous connecter, utilisez le username [bold green]senakossi[/bold green] et le mot de passe [bold green]password[/bold green].",
        "",
        "L'application utilise une base de données MongoDB en ligne, ce qui vous évite de devoir l'installer localement.",
        "En tant qu'administrateur, vous aurez accès à tous les comptes (admin, marchand, client).",
    ]
    for msg in messages_intro:
        console.print(msg)
        time.sleep(0.8)
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Menu Principal
    console.clear()
    console.print("[bold underline]=== MENU PRINCIPAL ===[/bold underline]\n")
    console.print("Voici les options disponibles dans le menu principal :\n")
    console.print("1. 🔑 Se connecter en tant qu'administrateur")
    console.print("2. 🛒 Se connecter en tant que marchand")
    console.print("3. 👥 Accéder à l'espace client")
    console.print("4. 🎬 Demo de l'application")
    console.print("5. 🚪 Quitter l'application")
    time.sleep(2)
    console.print("\nDans cette démonstration, nous allons simuler le parcours depuis le menu principal.")
    time.sleep(2)
    
    input("\nAppuyez sur Entrée pour simuler la connexion en tant qu'administrateur...")
    
    # Simulation de connexion en tant qu'administrateur
    console.clear()
    console.print("[bold blue]Étape 1 : Connexion en tant qu'administrateur[/bold blue]\n")
    console.print("Pour vous connecter en tant qu'administrateur, utilisez les identifiants suivants :")
    console.print("    Username : [bold green]senakossi[/bold green]")
    console.print("    Mot de passe : [bold green]password[/bold green]")
    time.sleep(3)
    console.print("\n[italic]Une fois les identifiants validés, vous accédez au menu administrateur...[/italic]")
    time.sleep(3)
    input("\nAppuyez sur Entrée pour continuer vers le menu administrateur...")
    
    # Menu Administrateur
    console.clear()
    console.print("[bold underline]=== MENU ADMINISTRATEUR ===[/bold underline]\n")
    console.print("En tant qu'administrateur, voici les options que vous pouvez utiliser :\n")
    console.print("1. 🏢 Gérer les marchés")
    console.print("   - Créer, afficher, modifier ou supprimer un marché.")
    console.print("2. 🛍️ Gérer les marchands")
    console.print("   - Ajouter, afficher, modifier, supprimer un marchand ou le rattacher à un marché.")
    console.print("3. 👥 Gérer les utilisateurs")
    console.print("   - Créer, afficher, modifier ou supprimer un utilisateur (admin, marchand, client).")
    console.print("4. 📊 Consulter les rapports")
    console.print("   - Visualiser divers rapports et statistiques sur les marchés, les ventes et les stocks.")
    console.print("5. 🚪 Se déconnecter")
    time.sleep(4)
    input("\nAppuyez sur Entrée pour explorer la gestion des marchés...")
    
    # Gestion des Marchés
    console.clear()
    console.print("[bold blue]Étape 2 : Gestion des Marchés[/bold blue]\n")
    console.print("Dans le menu 'Gérer les marchés', vous pouvez :")
    console.print(" - Créer un nouveau marché en fournissant son nom et ses dimensions (taille_x et taille_y).")
    console.print(" - Afficher la liste des marchés existants pour visualiser leur état.")
    console.print(" - Modifier les informations d'un marché existant.")
    console.print(" - Supprimer un marché si nécessaire.")
    time.sleep(5)
    input("\nAppuyez sur Entrée pour revenir au menu administrateur...")
    
    # Retour au menu administrateur et gestion des marchands
    console.clear()
    console.print("[bold blue]Étape 3 : Gestion des Marchands[/bold blue]\n")
    console.print("Dans le menu 'Gérer les marchands', vous pouvez :")
    console.print(" - Ajouter un marchand en créant un compte marchand.")
    console.print(" - Afficher la liste des marchands pour surveiller leurs informations.")
    console.print(" - Modifier les informations d'un marchand existant.")
    console.print(" - Supprimer un marchand si nécessaire.")
    console.print(" - Rattacher un marchand à un marché pour qu'il puisse opérer sur une zone précise.")
    time.sleep(5)
    input("\nAppuyez sur Entrée pour continuer vers la gestion des utilisateurs...")
    
    # Gestion des Utilisateurs
    console.clear()
    console.print("[bold blue]Étape 4 : Gestion des Utilisateurs[/bold blue]\n")
    console.print("Dans le menu 'Gérer les utilisateurs', l'administrateur peut :")
    console.print(" - Créer un nouvel utilisateur en choisissant son rôle (admin, marchand, client).")
    console.print(" - Afficher la liste de tous les utilisateurs enregistrés.")
    console.print(" - Modifier les informations d'un utilisateur (exemple : changer son email ou son nom).")
    console.print(" - Supprimer un utilisateur si nécessaire.")
    time.sleep(5)
    input("\nAppuyez sur Entrée pour explorer la consultation des rapports...")
    
    # Consultation des Rapports
    console.clear()
    console.print("[bold blue]Étape 5 : Consultation des Rapports[/bold blue]\n")
    console.print("L'option 'Consulter les rapports' vous permet de visualiser des statistiques détaillées, telles que :")
    console.print(" - La carte du marché affichée sous forme de graphique interactif.")
    console.print(" - Le chiffre d'affaires par marchand sous forme de diagramme en barres.")
    console.print(" - L'évolution des ventes dans le temps et d'autres analyses pertinentes.")
    console.print("Ces rapports sont générés à l'aide d'outils d'analyse de données et visualisés avec Plotly et Dash.")
    time.sleep(5)
    input("\nAppuyez sur Entrée pour revenir au menu principal...")
    
    # Retour général et conclusion
    console.clear()
    console.print("[bold blue]Étape 6 : Retour au Menu Principal et Déconnexion[/bold blue]\n")
    console.print("Une fois vos opérations terminées, vous pouvez :")
    console.print(" - Retourner au menu principal pour choisir une autre fonctionnalité.")
    console.print(" - Vous déconnecter et quitter l'application en toute sécurité.")
    console.print("\nMerci d'avoir suivi cette démonstration interactive. Nous espérons que ce tutoriel vous a aidé à mieux comprendre le fonctionnement de l'application.")
    time.sleep(3)
    input("\nAppuyez sur Entrée pour terminer la démonstration et retourner au menu principal...")
    
    console.clear()
    console.print("[bold green]Fin de la démonstration interactive. Vous allez être redirigé vers le menu principal.[/bold green]\n")
