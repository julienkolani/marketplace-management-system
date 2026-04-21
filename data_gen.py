import random
import re
import time
from datetime import datetime, timezone
from unidecode import unidecode

from mongoengine import (
    connect, disconnect, ValidationError
)

from Database.models import Client, Marchand, User, Marche, Produit, Transaction
from Database.Services import supprimer_toute_la_base

# Suppression de toute la base avant de générer les données
supprimer_toute_la_base()
time.sleep(1)

# Ensemble global pour stocker les usernames déjà utilisés
used_usernames = set()

def generate_unique_username(full_name):
    """
    Génère un username unique à partir d'un nom complet.
    On convertit le nom en minuscules, on retire les accents et les caractères non alphanumériques.
    En cas de doublon, on ajoute un suffixe numérique.
    """
    base_username = re.sub(r'\W+', '', unidecode(full_name.lower()))
    username = base_username
    counter = 1
    while username in used_usernames:
        username = f"{base_username}{counter}"
        counter += 1
    used_usernames.add(username)
    return username

# =============================================================================
# FONCTIONS DE GÉNÉRATION DES COMPTES FIXES
# =============================================================================

def generate_fixed_admin_users():
    """
    Crée les comptes admin fixes : 'senakossi', 'admin', 'root', 'administrateur'.
    """
    fixed_admin_usernames = ["senakossi", "admin", "root", "administrateur"]
    admin_users = []
    for username in fixed_admin_usernames:
        email = f"{username}@gmail.com"
        user = User(username=username, email=email, role='admin')
        user.set_password("password")
        user.save()
        admin_users.append(user)
    return admin_users

def generate_fixed_merchant_users():
    """
    Crée le compte marchand fixe : 'julien marchand'.
    """
    fixed_names = ["julien marchand"]
    merchant_users = []
    for full_name in fixed_names:
        # On peut forcer le username via la fonction generate_unique_username
        username = generate_unique_username(full_name)
        email = f"{username}@gmail.com"
        user = User(username=username, email=email, role='marchand')
        user.set_password("password")
        user.save()
        merchant_users.append(user)
    return merchant_users

def generate_fixed_client_users():
    """
    Crée le compte client fixe : 'clients'.
    """
    fixed_names = ["clients"]
    client_users = []
    for full_name in fixed_names:
        username = generate_unique_username(full_name)
        email = f"{username}@exemple.com"
        user = User(username=username, email=email, role='client')
        user.set_password("password")
        user.save()
        client_users.append(user)
    return client_users

# =============================================================================
# FONCTIONS DE GÉNÉRATION DES DONNÉES ALÉATOIREMENT
# =============================================================================

def generate_markets():
    """
    Crée 5 marchés aux noms togolais et aux tailles de grille différentes.
    """
    market_definitions = [
        {"nom": "Marché de Lomé",       "taille_x": 10, "taille_y": 10, "nombre_marchands": 15},
        {"nom": "Marché de Sokodé",      "taille_x": 8,  "taille_y": 8,  "nombre_marchands": 5},
        {"nom": "Marché de Kara",        "taille_x": 6,  "taille_y": 6,  "nombre_marchands": 3},
        {"nom": "Marché d'Atakpamé",     "taille_x": 5,  "taille_y": 5,  "nombre_marchands": 4},
        {"nom": "Marché de Dapaong",     "taille_x": 4,  "taille_y": 4,  "nombre_marchands": 3},
    ]
    markets = {}
    for md in market_definitions:
        market = Marche(nom=md["nom"], taille_x=md["taille_x"], taille_y=md["taille_y"])
        market.save()
        markets[md["nom"]] = {
            "market": market,
            "nombre_marchands": md["nombre_marchands"],
            "taille_x": md["taille_x"],
            "taille_y": md["taille_y"]
        }
    return markets

def generate_admin_users(num_admins=0):
    """
    Crée des utilisateurs admin aléatoires.
    Ici, on peut décider de ne pas en générer si l'on souhaite uniquement les comptes fixes.
    """
    admin_users = []
    admin_names = ["Sena Kossi", "Komla Dovi"]
    for i in range(num_admins):
        name = admin_names[i % len(admin_names)]
        username = generate_unique_username(name)
        email = f"{username}@gmail.com"
        user = User(username=username, email=email, role='admin')
        user.set_password("password")
        user.save()
        admin_users.append(user)
    return admin_users

def generate_merchant_users():
    """
    Crée 30 utilisateurs marchand aléatoires avec des noms réels.
    """
    merchant_users = []
    merchant_names = [
        "Komlan Aglago", "Kossi Amoou", "Messan Kossi", "Yawovi Soglo", "Afi Tchakabou",
        "Kossi Ameka", "Agbeko Anani", "Fabrice Mawugbe", "Nadège Lawson", "Foufou Dakpogan",
        "Sessi Doseh", "Kodjo Yawo", "Nana Koffi", "Mawuli Agboyibor", "Dodzi Gbadamassi",
        "Yawovi Adom", "Akouvi Mensah", "Esso Barou", "Sika Kossi", "Ahoua Tchane",
        "Sessi Amewou", "Komlan Avivi", "Kossi Agbeko", "Messan Adodo", "Yawovi Agbeko",
        "Afi Mensah", "Kossi Adzo", "Agbeko Dovi", "Fabrice Adotey", "Nadège Gbadamassi"
    ]
    for name in merchant_names:
        username = generate_unique_username(name)
        email = f"{username}@gmail.com"
        user = User(username=username, email=email, role='marchand')
        user.set_password("password")
        user.save()
        merchant_users.append(user)
    return merchant_users

def generate_merchant_products(merchant_user):
    """
    Pour un marchand (dérivé via son User), crée entre 10 et 20 produits
    avec des noms inspirés du contexte togolais.
    """
    marchand = Marchand.objects(user=merchant_user).first()
    num_products = random.randint(10, 20)
    base_names = [
        "Attiéké", "Foufou", "Koklo", "Gboma", "Akpan", "Yovo",
        "Gbegan", "Agbeli", "Djenkou", "Pâte", "Riz", "Maïs"
    ]
    used_names = set()
    for i in range(num_products):
        if len(used_names) < len(base_names):
            name = random.choice([n for n in base_names if n not in used_names])
            used_names.add(name)
        else:
            name = random.choice(base_names) + f" {i}"
        quantite = random.randint(10, 100)
        prix = round(random.uniform(1, 100), 2)
        produit = Produit(nom=name, quantite=quantite, prix=prix)
        marchand.produits.append(produit)
    marchand.save()

def generate_client_users(num_clients=70):
    """
    Crée num_clients utilisateurs client aléatoires avec des noms réalistes.
    """
    client_users = []
    first_names = [
        "Kossi", "Komlan", "Messan", "Yawovi", "Afi", "Sessi", "Nafissatou", "Akofa",
        "Ame", "Togbe", "Fadima", "Akossiwa", "Edem", "Dodzi", "Gnatou", "Kpatcha",
        "Senami", "Nana", "Fabrice", "Ekou", "Salimata", "Assiba", "Adjoa", "Kouame",
        "Davi", "Issa", "Yao", "Mawuli", "Mireille", "Esther"
    ]
    last_names = [
        "Agbeko", "Amouzou", "Dosseh", "Kouami", "Soglo", "Dovi", "Gbadamassi",
        "Mensah", "Tchakadé", "Adotey", "Akpah", "Sanni", "Ayi", "Koukpaki",
        "NGuessan", "Zinsou", "Sesso", "Amegbor", "Tchagbe", "Avivi"
    ]
    for i in range(num_clients):
        first = random.choice(first_names)
        last = random.choice(last_names)
        full_name = f"{first} {last}"
        username = generate_unique_username(full_name)
        email = f"{username}@exemple.com"
        user = User(username=username, email=email, role='client')
        user.set_password("password")
        user.save()
        client_users.append(user)
    return client_users

# =============================================================================
# ASSIGNATION DES MARCHANDS AUX MARCHÉS
# =============================================================================

def assign_merchants_to_markets(merchant_users, markets):
    """
    Répartit les marchands dans les marchés créés selon la répartition indiquée.
    Pour chaque marchand, on recherche une position (x,y) libre dans le marché.
    La position est choisie aléatoirement dans la grille.
    """
    assigned = 0
    # Pour diversifier, on mélange la liste des marchands à affecter
    random.shuffle(merchant_users)
    for market_name, data in markets.items():
        market = data["market"]
        count = data["nombre_marchands"]
        for _ in range(count):
            if assigned >= len(merchant_users):
                break
            user = merchant_users[assigned]
            marchand = Marchand.objects(user=user).first()
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(0, data["taille_x"] - 1)
                y = random.randint(0, data["taille_y"] - 1)
                if market.est_emplacement_libre(x, y):
                    market.ajouter_marchand(marchand, x, y)
                    placed = True
                attempts += 1
            if not placed:
                print(f"Impossible de placer le marchand {marchand.nom} dans le marché {market.nom}")
            assigned += 1

# =============================================================================
# GÉNÉRATION DES TRANSACTIONS
# =============================================================================

def generate_transactions(client_users, merchant_users, num_transactions_range=(1, 3)):
    """
    Pour chaque client, génère un nombre aléatoire (entre num_transactions_range[0]
    et num_transactions_range[1]) de transactions.
    Chaque transaction sélectionne aléatoirement un marchand (ayant encore du stock)
    et achète 1 à 3 produits parmi ceux proposés.
    La transaction est validée et ajoutée aux historiques du client et du marchand.
    """
    for client_user in client_users:
        client_doc = Client.objects(user=client_user).first()
        if not client_doc:
            continue
        num_transactions = random.randint(num_transactions_range[0], num_transactions_range[1])
        for _ in range(num_transactions):
            # Sélectionner un marchand ayant encore des produits en stock
            valid_merchants = []
            for m in merchant_users:
                marchand = Marchand.objects(user=m).first()
                if marchand and any(prod.quantite > 0 for prod in marchand.produits):
                    valid_merchants.append(m)
            if not valid_merchants:
                continue
            merchant_user = random.choice(valid_merchants)
            marchand = Marchand.objects(user=merchant_user).first()
            if not marchand.produits:
                continue
            num_items = random.randint(1, min(3, len(marchand.produits)))
            selected_products = random.sample(marchand.produits, num_items)
            purchased_items = []
            for prod in selected_products:
                if prod.quantite <= 0:
                    continue
                max_qty = min(prod.quantite, 5)
                qty = random.randint(1, max_qty)
                # Conserver les caractéristiques du produit acheté dans la transaction
                purchased_item = Produit(nom=prod.nom, quantite=qty, prix=prod.prix)
                purchased_items.append(purchased_item)
                # Déduire la quantité achetée du stock du marchand
                marchand.retirer_produit(prod.nom, qty)
            if not purchased_items:
                continue
            transaction = Transaction(
                client=client_doc,
                marchand=marchand,
                produits=purchased_items,
                date=datetime.now(timezone.utc)
            )
            try:
                transaction.valider_transaction()
            except ValidationError as e:
                print("Erreur de validation de transaction:", e)
                continue
            # Mise à jour des historiques d'achats et de ventes
            client_doc.historique_achats.append(transaction)
            client_doc.save()
            marchand.historique_ventes.append(transaction)
            marchand.save()

# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def main():
    # 1. Génération des marchés
    try:
        print("=== Génération 1 pass: Génération des marchés ===")
        markets = generate_markets()
        print("✅ Génération des marchés réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la génération des marchés: {e}")
        return

    # 2. Création des comptes fixes
    try:
        print("=== Génération 2 pass: Création des comptes fixes ===")
        fixed_admins = generate_fixed_admin_users()
        fixed_merchants = generate_fixed_merchant_users()
        fixed_clients = generate_fixed_client_users()
        print("✅ Création des comptes fixes réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la création des comptes fixes: {e}")
        return

    # 3. Création des comptes aléatoires (admins si besoin, marchands et clients)
    try:
        print("=== Génération 3 pass: Création des comptes aléatoires ===")
        # On peut ajuster le nombre d'admins aléatoires ; ici on les désactive en passant 0
        random_admins = generate_admin_users(0)
        random_merchants = generate_merchant_users()
        random_clients = generate_client_users(70)
        print("✅ Création des comptes aléatoires réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la création des comptes aléatoires: {e}")
        return

    # Fusionner les listes de marchands et de clients
    all_merchant_users = fixed_merchants + random_merchants
    all_client_users = fixed_clients + random_clients

    # 4. Création des produits pour chaque marchand
    try:
        print("=== Génération 4 pass: Création des produits pour chaque marchand ===")
        for user in all_merchant_users:
            generate_merchant_products(user)
        print("✅ Création des produits pour chaque marchand réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la création des produits pour chaque marchand: {e}")
        return

    # 5. Affectation des marchands aux marchés
    try:
        print("=== Génération 5 pass: Affectation des marchands aux marchés ===")
        assign_merchants_to_markets(all_merchant_users, markets)
        print("✅ Affectation des marchands aux marchés réussie")
    except Exception as e:
        print(f"❌ Erreur lors de l'affectation des marchands aux marchés: {e}")
        return

    # 6. Génération des transactions (achats des clients)
    try:
        print("=== Génération 6 pass: Génération des transactions ===")
        generate_transactions(all_client_users, all_merchant_users)
        print("✅ Génération des transactions réussie")
    except Exception as e:
        print(f"❌ Erreur lors de la génération des transactions: {e}")
        return

    print("=== Génération des données terminée ===")

if __name__ == "__main__":
    main()
