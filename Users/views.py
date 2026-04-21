from rich.console import Console
from rich.table import Table
from Users.services import (
    create_superuser,
    login,
    logout,
    creer_compte,
    modifier_compte,
    supprimer_compte,
    lister_utilisateurs,
    supprimer_utilisateur_par_admin,
    lister_marchands,
    supprimer_marchand_par_admin,
    reset_database,
)
from Database.models import User, Marche, Marchand
import re

console = Console()


def est_email_valide(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


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


# def modifier_compte_marchand_view():
#     """
#     Modifie un compte marchand existant.
#     """
#     try:
#         afficher_liste_marchands()
#         username = input("Entrez le nom d'utilisateur du marchand à modifier : ").strip()
#         if not username:
#             console.print("[red]Le nom d'utilisateur ne peut pas être vide.[/red]")
#             return

#         # Rechercher le marchand
#         user = User.objects(username=username, role="marchand").first()
#         if not user:
#             console.print(f"[red]Aucun marchand trouvé avec le nom '{username}'.[/red]")
#             return

#         # Demander les nouvelles informations
#         nouveau_username = input("Entrez le nouveau nom d'utilisateur (laissez vide pour ne pas changer) : ").strip()
#         nouvel_email = input("Entrez le nouvel email (laissez vide pour ne pas changer) : ").strip()

#         if nouveau_username:
#             if User.objects(username=nouveau_username).first():
#                 console.print(f"[red]Le nom d'utilisateur '{nouveau_username}' est déjà pris.[/red]")
#                 return
#             user.username = nouveau_username

#         if nouvel_email:
#             if User.objects(email=nouvel_email).first():
#                 console.print(f"[red]L'email '{nouvel_email}' est déjà utilisé.[/red]")
#                 return
#             user.email = nouvel_email

#         # Sauvegarder les modifications
#         user.save()
#         console.print("[green]Compte marchand modifié avec succès ![/green]")

#     except Exception as e:
#         console.print(f"[red]{e}[/red]")

def modifier_compte_marchand_view():
    """
    Modifie un compte marchand existant en permettant de changer :
      - Le nom d'utilisateur,
      - L'email,
      - La position (position_x et position_y).
    """
    try:
        afficher_liste_marchands()
        username = input("Entrez le nom d'utilisateur du marchand à modifier : ").strip()
        if not username:
            console.print("[red]Le nom d'utilisateur ne peut pas être vide.[/red]")
            return

        # Rechercher l'utilisateur marchand
        user = User.objects(username=username, role="marchand").first()
        if not user:
            console.print(f"[red]Aucun marchand trouvé avec le nom '{username}'.[/red]")
            return

        # Demander les nouvelles informations
        nouveau_username = input("Entrez le nouveau nom d'utilisateur (laissez vide pour ne pas changer) : ").strip()
        nouvel_email = input("Entrez le nouvel email (laissez vide pour ne pas changer) : ").strip()

        # Demander la nouvelle position
        nouvelle_position_x = input("Entrez la nouvelle position X (laissez vide pour ne pas changer) : ").strip()
        nouvelle_position_y = input("Entrez la nouvelle position Y (laissez vide pour ne pas changer) : ").strip()

        # Modification du nom d'utilisateur
        if nouveau_username:
            if User.objects(username=nouveau_username).first():
                console.print(f"[red]Le nom d'utilisateur '{nouveau_username}' est déjà pris.[/red]")
                return
            user.username = nouveau_username

        # Modification de l'email
        if nouvel_email:
            if User.objects(email=nouvel_email).first():
                console.print(f"[red]L'email '{nouvel_email}' est déjà utilisé.[/red]")
                return
            user.email = nouvel_email

        # Sauvegarder les modifications de l'utilisateur
        user.save()

        # Rechercher le compte marchand associé à l'utilisateur
        marchand = Marchand.objects(user=user).first()
        if not marchand:
            console.print("[red]Aucun compte marchand associé trouvé pour cet utilisateur.[/red]")
            return

        # Modification de la position X, si renseignée
        if nouvelle_position_x:
            try:
                pos_x = int(nouvelle_position_x)
                if pos_x < 0:
                    console.print("[red]La position X doit être un entier positif.[/red]")
                    return
                marchand.position_x = pos_x
            except ValueError:
                console.print("[red]La position X doit être un nombre entier valide.[/red]")
                return

        # Modification de la position Y, si renseignée
        if nouvelle_position_y:
            try:
                pos_y = int(nouvelle_position_y)
                if pos_y < 0:
                    console.print("[red]La position Y doit être un entier positif.[/red]")
                    return
                marchand.position_y = pos_y
            except ValueError:
                console.print("[red]La position Y doit être un nombre entier valide.[/red]")
                return

        # Sauvegarder les modifications sur le compte marchand
        marchand.save()
        console.print("[green]Compte marchand modifié avec succès ![/green]")

    except Exception as e:
        console.print(f"[red]{e}[/red]")

def supprimer_compte_marchand_view():
    """
    Supprime un compte marchand après confirmation.
    """
    try:
        afficher_liste_marchands()
        username = input("Entrez le nom d'utilisateur du marchand à supprimer : ").strip()
        if not username:
            console.print("[red]Le nom d'utilisateur ne peut pas être vide.[/red]")
            return

        # Rechercher le marchand
        user = User.objects(username=username, role="marchand").first()
        if not user:
            console.print(f"[red]Aucun marchand trouvé avec le nom '{username}'.[/red]")
            return

        # Confirmer la suppression
        confirmation = input(f"Êtes-vous sûr de vouloir supprimer le marchand '{username}' ? (o/n) : ").strip().lower()
        if confirmation != 'o':
            console.print("[yellow]Suppression annulée.[/yellow]")
            return

        # Supprimer le marchand et ses données rattachées
        marchand = Marchand.objects(user=user).first()
        if marchand:
            marchand.delete()  # Supprime le marchand et ses données rattachées
        user.delete()  # Supprime l'utilisateur
        console.print(f"[green]Marchand '{username}' supprimé avec succès. Toutes les données rattachées ont été perdues.[/green]")

    except Exception as e:
        console.print(f"[red]{e}[/red]")


def afficher_liste_utilisateurs(role=None):
    """Affiche la liste des utilisateurs, filtrée par rôle si spécifié."""
    utilisateurs = lister_utilisateurs(role=role)
    if utilisateurs:
        title = f"Liste des {role}s" if role else "Liste des Utilisateurs"
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Nom d'utilisateur", style="dim", width=20)
        table.add_column("Email", style="dim", width=30)
        table.add_column("Rôle", justify="right")
        for user in utilisateurs:
            table.add_row(user.username, user.email, user.role)
        console.print(table)
    else:
        console.print(f"[red]Aucun utilisateur{' ('+role+')' if role else ''} trouvé.[/red]")


def afficher_liste_tout_utilisateurs():
    """Affiche la liste de tous les utilisateurs."""
    utilisateurs = User.objects()
    if utilisateurs:
        table = Table(title="Liste des Utilisateurs", show_header=True, header_style="bold magenta")
        table.add_column("Nom d'utilisateur", style="dim", width=20)
        table.add_column("Email", style="dim", width=30)
        table.add_column("Rôle", justify="center")
        for user in utilisateurs:
            role = user.role if user.role else "Non spécifié"
            email = user.email if user.email else "Non disponible"
            table.add_row(user.username, email, role)
        console.print(table)
    else:
        console.print("[red]Aucun utilisateur trouvé.[/red]")


def modifier_mon_compte_marchand_view():
    """
    Permet au marchand de modifier ses informations personnelles.
    """
    try:
        identifiant = input("Entrez votre nom d'utilisateur ou email : ").strip()
        if not identifiant:
            console.print("[red]L'identifiant ne peut pas être vide.[/red]")
            return

        # Recherche du marchand par nom d'utilisateur ou email
        marchand = User.objects(username=identifiant).first() or User.objects(email=identifiant).first()
        if not marchand:
            console.print(f"[red]Aucun compte trouvé pour '{identifiant}'.[/red]")
            return

        # Affichage des informations actuelles
        console.print(f"Nom actuel : {getattr(marchand, 'nom', marchand.username)}")
        console.print(f"Email actuel : {marchand.email}")

        # Demande des nouvelles informations
        nouveau_nom = input("Entrez votre nouveau nom (laissez vide pour ne pas changer) : ").strip()
        nouvel_email = input("Entrez votre nouvel email (laissez vide pour ne pas changer) : ").strip()

        if nouveau_nom:
            marchand.nom = nouveau_nom

        if nouvel_email:
            if not est_email_valide(nouvel_email):
                console.print(f"[red]L'email '{nouvel_email}' n'est pas valide.[/red]")
                return
            if User.objects(email=nouvel_email).first():
                console.print(f"[red]L'email '{nouvel_email}' est déjà utilisé.[/red]")
                return
            marchand.email = nouvel_email

        confirmation = input("Confirmez-vous ces modifications ? (oui/non) : ").strip().lower()
        if confirmation != 'oui':
            console.print("[yellow]Modification annulée.[/yellow]")
            return

        marchand.save()
        console.print("[green]Informations modifiées avec succès ![/green]")

    except Exception as e:
        console.print(f"[red]Erreur : {e}[/red]")


def changer_mot_de_passe_view(marchand):
    """
    Permet au marchand de changer son mot de passe.
    """
    try:
        ancien_mot_de_passe = input("Entrez votre ancien mot de passe : ").strip()
        if not marchand.user.check_password(ancien_mot_de_passe):
            console.print("[red]Ancien mot de passe incorrect.[/red]")
            return

        nouveau_mot_de_passe = input("Entrez votre nouveau mot de passe : ").strip()
        confirmation_mot_de_passe = input("Confirmez votre nouveau mot de passe : ").strip()
        if nouveau_mot_de_passe != confirmation_mot_de_passe:
            console.print("[red]Les mots de passe ne correspondent pas.[/red]")
            return

        marchand.user.set_password(nouveau_mot_de_passe)
        marchand.user.save()
        console.print("[green]Mot de passe changé avec succès ![/green]")

    except Exception as e:
        console.print(f"[red]{e}[/red]")


def afficher_informations_marchand_view(marchand):
    """
    Affiche les informations du compte du marchand.
    """
    table = Table(title="Informations du Compte", show_header=True, header_style="bold magenta")
    table.add_column("Champ", style="dim", width=20)
    table.add_column("Valeur", style="dim", width=30)
    table.add_row("Nom d'utilisateur", marchand.user.username)
    table.add_row("Email", marchand.user.email)
    table.add_row("Rôle", marchand.user.role)
    table.add_row("Nom du marchand", marchand.nom)
    table.add_row("Position X", str(marchand.position_x))
    table.add_row("Position Y", str(marchand.position_y))
    console.print(table)


def modifier_utilisateur_view():
    """
    Modifie un utilisateur existant.
    """
    try:
        username = input("Entrez le nom d'utilisateur de l'utilisateur à modifier : ").strip()
        if not username:
            console.print("[red]Le nom d'utilisateur ne peut pas être vide.[/red]")
            return

        user = User.objects(username=username).first()
        if not user:
            console.print(f"[red]Aucun utilisateur trouvé avec le nom '{username}'.[/red]")
            return

        nouveau_username = input("Entrez le nouveau nom d'utilisateur (laissez vide pour ne pas changer) : ").strip()
        nouvel_email = input("Entrez le nouvel email (laissez vide pour ne pas changer) : ").strip()
        nouveau_role = input("Entrez le nouveau rôle (admin/marchand/client) (laissez vide pour ne pas changer) : ").strip().lower()

        if nouveau_username:
            if User.objects(username=nouveau_username).first():
                console.print(f"[red]Le nom d'utilisateur '{nouveau_username}' est déjà pris.[/red]")
                return
            user.username = nouveau_username

        if nouvel_email:
            if User.objects(email=nouvel_email).first():
                console.print(f"[red]L'email '{nouvel_email}' est déjà utilisé.[/red]")
                return
            user.email = nouvel_email

        if nouveau_role:
            if nouveau_role in ["admin", "marchand", "client"]:
                user.role = nouveau_role
            else:
                console.print("[red]Rôle invalide. Veuillez choisir parmi admin, marchand ou client.[/red]")
                return

        user.save()
        console.print("[green]Utilisateur modifié avec succès ![/green]")

    except Exception as e:
        console.print(f"[red]{e}[/red]")


def login_view():
    """Affiche le formulaire de connexion pour un client."""
    try:
        user = login('client')
        return user
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        return None


def logout_view():
    """Déconnecte l'utilisateur et affiche un message de déconnexion."""
    logout()
    console.print("[green]Déconnexion réussie. À bientôt ![/green]")


def modifier_compte_view(user):
    """Affiche le formulaire de modification de compte pour un utilisateur connecté."""
    username = input("Entrez un nouveau nom d'utilisateur (laissez vide pour ne pas changer) : ")
    email = input("Entrez une nouvelle adresse email (laissez vide pour ne pas changer) : ")
    password = input("Entrez un nouveau mot de passe (laissez vide pour ne pas changer) : ")
    try:
        modifier_compte(user, username=username, email=email, password=password)
        console.print("[green]Compte modifié avec succès ![/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def supprimer_compte_view(user):
    """Affiche un message de confirmation pour la suppression du compte de l'utilisateur connecté."""
    confirmation = input("Êtes-vous sûr de vouloir supprimer votre compte ? (oui/non) : ")
    if confirmation.lower() == "oui":
        try:
            supprimer_compte(user.username)
            console.print("[green]Compte supprimé avec succès.[/green]")
        except Exception as e:
            console.print(f"[red]{e}[/red]")
    else:
        console.print("[yellow]Suppression annulée.[/yellow]")


def supprimer_utilisateur_par_admin_view(role=None):
    """Affiche le formulaire de suppression d'un utilisateur (ou marchand) par l'admin."""
    username = input("Entrez le nom d'utilisateur à supprimer : ")
    confirmation = input(f"Êtes-vous sûr de vouloir supprimer l'utilisateur {username} ? (oui/non) : ")
    if confirmation.lower() == "oui":
        try:
            supprimer_utilisateur_par_admin(username)
            console.print(f"[green]{role.capitalize()} supprimé avec succès.[/green]")
        except Exception as e:
            console.print(f"[red]{e}[/red]")
    else:
        console.print("[yellow]Suppression annulée.[/yellow]")


def afficher_liste_marchands():
    """Affiche la liste des marchands avec des informations détaillées."""
    marchands = lister_marchands()
    if marchands:
        table = Table(title="Liste des marchands", show_header=True, header_style="bold magenta")
        table.add_column("Nom du Marchand", style="dim", width=20)
        table.add_column("Email", justify="left")
        table.add_column("Position (X, Y)", justify="center")
        table.add_column("Marché Associé", justify="left")
        for marchand in marchands:
            email = marchand.user.email if marchand.user else "Non disponible"
            marche_associe = Marche.objects(marchands=marchand).first()
            nom_marche = marche_associe.nom if marche_associe else "Aucun marché associé"
            table.add_row(
                marchand.nom,
                email,
                f"({marchand.position_x}, {marchand.position_y})",
                nom_marche
            )
        console.print(table)
    else:
        console.print("[red]Aucun marchand trouvé.[/red]")


def supprimer_marchand_par_admin_view():
    """Affiche le formulaire de suppression d'un marchand par l'admin."""
    nom_marchand = input("Entrez le nom du marchand à supprimer : ")
    try:
        supprimer_marchand_par_admin(nom_marchand)
        console.print("[green]Marchand supprimé avec succès.[/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def reset_database_view():
    """Affiche un message de confirmation pour la réinitialisation de la base de données."""
    confirmation = input("Êtes-vous sûr de vouloir tout supprimer ? (oui/non) : ")
    if confirmation.lower() == "oui":
        reset_database()
        console.print("[green]Base de données réinitialisée avec succès.[/green]")
    else:
        console.print("[yellow]Réinitialisation annulée.[/yellow]")
