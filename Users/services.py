from Database.models import User, Marchand, Client
from Core.utils import clear_screen, handle_error
import bcrypt
import getpass

def create_superuser():
    """Crée un super utilisateur par défaut (admin/admin)."""
    if not User.objects(username="admin").first():
        admin = User(username="admin", email="admin@example.com", role="admin")
        admin.set_password("admin")  # Mot de passe par défaut
        admin.save()
        print("Super utilisateur 'admin' créé avec succès.")
    else:
        print("Le super utilisateur 'admin' existe déjà.")

def log(username, password):
    """
    Authentifie un utilisateur.
    :param username: Nom d'utilisateur.
    :param password: Mot de passe.
    :return: Instance de l'utilisateur.
    """
    user = User.objects(username=username).first()
    if not user:
        raise ValueError("Utilisateur non trouvé.")
    if not user.check_password(password):
        raise ValueError("Mot de passe incorrect.")
    return user

def logout():
    """
    Déconnecte l'utilisateur.
    """
    exit()

def creer_compte(username, email, password, role):
    """
    Crée un nouveau compte utilisateur.
    :param username: Nom d'utilisateur.
    :param email: Adresse email.
    :param password: Mot de passe.
    :param role: Rôle de l'utilisateur (admin, marchand, client).
    """
    if User.objects(username=username).first():
        raise ValueError("Ce nom d'utilisateur est déjà pris.")
    if User.objects(email=email).first():
        raise ValueError("Cette adresse email est déjà utilisée.")

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    user.save()

    return user

def modifier_compte(user, **kwargs):
    """
    Modifie les informations d'un utilisateur.
    :param user: Instance de l'utilisateur.
    :param kwargs: Champs à modifier (username, email, password, etc.).
    """
    if "username" in kwargs:
        if User.objects(username=kwargs["username"]).first():
            raise ValueError("Ce nom d'utilisateur est déjà pris.")
        user.username = kwargs["username"]
    if "email" in kwargs:
        if User.objects(email=kwargs["email"]).first():
            raise ValueError("Cette adresse email est déjà utilisée.")
        user.email = kwargs["email"]
    if "password" in kwargs:
        user.set_password(kwargs["password"])
    user.save()

def supprimer_compte(username):
    """
    Supprime un compte utilisateur.
    :param username: Nom d'utilisateur.
    """
    user = User.objects(username=username).first()
    if not user:
        raise ValueError("Utilisateur non trouvé.")
    user.delete()

def lister_utilisateurs(role=None):
    """
    Liste tous les utilisateurs.
    :param role: (Optionnel) Filtre par rôle.
    :return: Liste des utilisateurs.
    """
    return User.objects(role=role)

def supprimer_utilisateur_par_admin(username):
    """
    Supprime un utilisateur (réservé aux admins).
    :param username: Nom d'utilisateur.
    """
    user = User.objects(username=username).first()
    if not user:
        raise ValueError("Utilisateur non trouvé.")
    if user.role == "admin":
        raise ValueError("Impossible de supprimer un administrateur.")
    user.delete()

def lister_marchands():
    """
    Liste tous les marchands.
    :return: Liste des marchands.
    """
    return Marchand.objects()

def supprimer_marchand_par_admin(nom_marchand):
    """
    Supprime un marchand (réservé aux admins).
    :param nom_marchand: Nom du marchand.
    """
    marchand = Marchand.objects(nom=nom_marchand).first()
    if not marchand:
        raise ValueError("Marchand non trouvé.")
    marchand.delete()

def reset_database():
    """
    Réinitialise la base de données en supprimant tous les utilisateurs.
    """
    confirmation = input("Êtes-vous sûr de vouloir tout supprimer ? (oui/non) : ")
    if confirmation.lower() == "oui":
        User.drop_collection()  # Supprime tous les utilisateurs
        print("Base de données réinitialisée avec succès.")
        create_superuser()  # Recrée le super utilisateur par défaut
    else:
        print("Réinitialisation annulée.")

ROLE_HIERARCHY = {
    "admin": ["admin", "marchand", "client"],  # Un admin peut se connecter en tant qu'admin, marchand ou client
    "marchand": ["marchand", "client"],         # Un marchand peut se connecter en tant que marchand ou client
    "client": ["client"],                         # Un client ne peut se connecter qu'en tant que client
}

def login(role):
    """
    Gère la connexion pour un rôle donné (admin, marchand ou client).
    :param role: Rôle souhaité par l'utilisateur (admin, marchand, client).
    :return: L'utilisateur connecté si les conditions sont respectées, None sinon.
    """
    if role not in ROLE_HIERARCHY:
        raise ValueError(f"Rôle invalide : {role}. Rôles valides : {', '.join(ROLE_HIERARCHY.keys())}")

    print(f"=== CONNEXION {role.upper()} ===")

    username = input("Entrez votre nom d'utilisateur : ")
    password = getpass.getpass("Entrez votre mot de passe : ")

    try:
        user = log(username, password)
        if role in ROLE_HIERARCHY[user.role]:
            print(f"Connexion réussie ! Bienvenue, {user.username}.")
            return user
        else:
            print(f"Accès refusé : En tant que {user.role}, vous ne pouvez pas vous connecter en tant que {role}.")
            return None
    except ValueError as e:
        print(e)
    return None
