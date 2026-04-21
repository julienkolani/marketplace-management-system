from mongoengine import (
    connect, disconnect, Document, EmbeddedDocument,
    StringField, EmailField, ListField, EmbeddedDocumentField,
    FloatField, IntField, DateTimeField, ReferenceField,
    BooleanField, ValidationError, CASCADE, get_db
)
from Core.settings import MONGO_URI, MONGO_DB_NAME
from Database.models import User, Produit, Marchand, Client, Transaction, Marche, Notification

# Connexion à MongoDB
connect(db=MONGO_DB_NAME, host=MONGO_URI, alias='default')

# ============================================================================
# Méthodes pour interagir avec la base de données
# ============================================================================

def supprimer_toute_la_base():
    """Supprime toutes les collections de la base de données (uniquement pour les Documents)."""
    # Produit et Promotion sont des EmbeddedDocument, ils n'ont pas de collection associée.
    User.drop_collection()
    Marchand.drop_collection()
    Client.drop_collection()
    Transaction.drop_collection()
    Marche.drop_collection()
    Notification.drop_collection()
    print("Toutes les collections ont été supprimées.")

def supprimer_donnees_model(model):
    """Supprime toutes les données d'un modèle spécifique (pour les Documents)."""
    if issubclass(model, Document):
        model.drop_collection()
        print(f"Toutes les données du modèle {model.__name__} ont été supprimées.")
    else:
        print(f"Le modèle {model.__name__} n'est pas un Document et ne peut pas être vidé.")

def mettre_a_jour_donnees_model(model, filtre, mise_a_jour):
    """Met à jour les données d'un modèle spécifique en fonction d'un filtre (pour les Documents)."""
    if issubclass(model, Document):
        model.objects(**filtre).update(**mise_a_jour)
        print(f"Les données du modèle {model.__name__} ont été mises à jour.")
    else:
        print(f"Le modèle {model.__name__} n'est pas un Document et ne peut pas être mis à jour.")

def ajouter_donnees_model(model, **donnees):
    """Ajoute des données à un modèle spécifique (pour les Documents)."""
    if issubclass(model, Document):
        instance = model(**donnees)
        instance.save()
        print(f"Les données ont été ajoutées au modèle {model.__name__}.")
    else:
        print(f"Le modèle {model.__name__} n'est pas un Document et ne peut pas être utilisé pour ajouter des données.")

def supprimer_donnees_model_par_filtre(model, **filtre):
    """Supprime les données d'un modèle spécifique en fonction d'un filtre (pour les Documents)."""
    if issubclass(model, Document):
        model.objects(**filtre).delete()
        print(f"Les données du modèle {model.__name__} ont été supprimées en fonction du filtre.")
    else:
        print(f"Le modèle {model.__name__} n'est pas un Document et ne peut pas être utilisé pour supprimer des données.")

def obtenir_donnees_model(model, **filtre):
    """Obtient les données d'un modèle spécifique en fonction d'un filtre (pour les Documents)."""
    if issubclass(model, Document):
        return model.objects(**filtre)
    else:
        print(f"Le modèle {model.__name__} n'est pas un Document et ne peut pas être utilisé pour obtenir des données.")
        return None

# ============================================================================
# Fonctions complémentaires pour explorer la base de données
# ============================================================================

def lister_tables():
    """
    Liste les collections (tables) présentes dans la base de données.
    """
    db = get_db()
    tables = db.list_collection_names()
    print("Collections dans la base de données:")
    for table in tables:
        print(" -", table)
    return tables

def afficher_structure_table(model):
    """
    Affiche la structure d'un modèle (table) en listant ses champs et leur type.
    Ce modèle doit être une sous-classe de Document.
    """
    if not issubclass(model, Document):
        print(f"{model.__name__} n'est pas un Document.")
        return
    print(f"Structure du modèle {model.__name__}:")
    for field_name, field in model._fields.items():
        # Pour une lecture plus claire, on affiche le nom du champ et la classe du field.
        print(f"  {field_name} : {field.__class__.__name__}")

def afficher_structure_toutes_tables():
    """
    Affiche la structure de tous les modèles (tables) connus.
    Les modèles pris en compte sont User, Marchand, Client, Transaction, Marche, Notification.
    """
    models = [User, Marchand, Client, Transaction, Marche, Notification]
    for model in models:
        print("----------------------------------------------------")
        afficher_structure_table(model)
    print("----------------------------------------------------")

def lister_methodes():
    """
    Liste les fonctions définies dans ce module.
    """
    import types
    fonctions = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType)]
    print("Fonctions définies dans ce module:")
    for f in fonctions:
        print(" -", f)
    return fonctions

# ============================================================================
# Exemple d'utilisation
# ============================================================================

if __name__ == "__main__":
    # print("=== Exemple d'utilisation des services ===\n")

    # # Exemple de suppression de toutes les collections
    # print("Suppression de toutes les collections...")
    # supprimer_toute_la_base()

    # # Exemple de suppression des données du modèle User
    # print("\nSuppression de toutes les données du modèle User...")
    # supprimer_donnees_model(User)

    # # Exemple de mise à jour du modèle User
    # print("\nMise à jour du modèle User...")
    # mettre_a_jour_donnees_model(User, {"username": "old_username"}, {"username": "new_username"})

    # # Exemple d'ajout de données dans le modèle User
    # print("\nAjout de données dans le modèle User...")
    # ajouter_donnees_model(
    #     User,
    #     username="new_user",
    #     email="new_user@example.com",
    #     password_hash="hashed_password",
    #     role="client"
    # )

    # # Exemple de suppression de données avec filtre dans le modèle User
    # print("\nSuppression de données dans le modèle User avec filtre username='new_user'...")
    # supprimer_donnees_model_par_filtre(User, username="new_user")

    # # Exemple d'obtention des données dans le modèle User
    # print("\nObtention des données du modèle User avec filtre role='client'...")
    # utilisateurs = obtenir_donnees_model(User, role="client")
    # if utilisateurs:
    #     for utilisateur in utilisateurs:
    #         print("Utilisateur :", utilisateur.username)

    # # Liste des collections présentes dans la base
    # print("\nListe des tables (collections) dans la base :")
    # lister_tables()

    # # Affichage de la structure de chaque table
    # print("\nAffichage de la structure de toutes les tables (modèles) :")
    # afficher_structure_toutes_tables()

    # # Liste des fonctions (méthodes) définies dans ce module
    # print("\nListe des fonctions définies dans le module :")
    # lister_methodes()
    pass