# Menu

## **1. Menu Principal (Accès à tous les utilisateurs)**

Ce menu est accessible dès la connexion. Il permet à l'utilisateur de choisir son rôle ou de se déconnecter.

```
=== MENU PRINCIPAL ===
1. Se connecter en tant qu'administrateur
2. Se connecter en tant que marchand
3. Se connecter en tant que client
4. Quitter l'application
```

---

## **2. Menu Administrateur**

Une fois connecté en tant qu'administrateur, l'utilisateur accède à ce menu. Il permet de gérer les marchés, les marchands, les utilisateurs, et de consulter les rapports.

```
=== MENU ADMINISTRATEUR ===
1. Gérer les marchés
2. Gérer les marchands
3. Gérer les utilisateurs
4. Consulter les rapports
5. Se déconnecter
```

### **2.1 Sous-menu : Gérer les marchés**

```
=== GESTION DES MARCHÉS ===
1. Créer un marché
2. Afficher la liste des marchés
3. Supprimer un marché
4. Retour au menu administrateur
```

### **2.2 Sous-menu : Gérer les marchands**

```
=== GESTION DES MARCHANDS ===
1. Ajouter un marchand
2. Afficher la liste des marchands
3. Supprimer un marchand
4. Retour au menu administrateur
```

### **2.3 Sous-menu : Gérer les utilisateurs**

```
=== GESTION DES UTILISATEURS ===
1. Ajouter un utilisateur
2. Afficher la liste des utilisateurs
3. Supprimer un utilisateur
4. Retour au menu administrateur
```

### **2.4 Sous-menu : Consulter les rapports**

```
=== RAPPORTS ===
1. Rapport des ventes
2. Rapport des stocks
3. Rapport des performances des marchands
4. Retour au menu administrateur
```

---

## **3. Menu Marchand**

Une fois connecté en tant que marchand, l'utilisateur accède à ce menu. Il permet de gérer son stock, consulter ses ventes, et gérer ses promotions.

```
=== MENU MARCHAND ===
1. Gérer mon stock
2. Consulter mes ventes
3. Gérer mes promotions
4. Se déconnecter
```

### **3.1 Sous-menu : Gérer mon stock**

```
=== GESTION DU STOCK ===
1. Ajouter un produit
2. Retirer un produit
3. Afficher mon stock
4. Retour au menu marchand
```

### **3.2 Sous-menu : Consulter mes ventes**

```
=== HISTORIQUE DES VENTES ===
1. Afficher les ventes du mois
2. Afficher les ventes par produit
3. Retour au menu marchand
```

### **3.3 Sous-menu : Gérer mes promotions**

```
=== GESTION DES PROMOTIONS ===
1. Créer une promotion
2. Afficher mes promotions
3. Supprimer une promotion
4. Retour au menu marchand
```

---

## **4. Menu Client**

Une fois connecté en tant que client, l'utilisateur accède à ce menu. Il permet de rechercher des produits, gérer son panier, et consulter son historique d'achats.

```
=== MENU CLIENT ===
1. Rechercher un produit
2. Gérer mon panier
3. Consulter mon historique d'achats
4. Se déconnecter
```

### **4.1 Sous-menu : Rechercher un produit**

```
=== RECHERCHE DE PRODUITS ===
1. Rechercher par nom
2. Rechercher par catégorie
3. Retour au menu client
```

### **4.2 Sous-menu : Gérer mon panier**

```
=== GESTION DU PANIER ===
1. Afficher mon panier
2. Ajouter un produit au panier
3. Retirer un produit du panier
4. Passer la commande
5. Retour au menu client
```

### **4.3 Sous-menu : Consulter mon historique d'achats**

```
=== HISTORIQUE DES ACHATS ===
1. Afficher mes achats récents
2. Afficher mes achats par produit
3. Retour au menu client
```

---

## **5. Menu Connexion**

Ce menu est accessible avant la connexion. Il permet à l'utilisateur de se connecter ou de quitter l'application.

```
=== MENU DE CONNEXION ===
1. Se connecter
2. Quitter l'application
```

---

## **6. Menu Déconnexion**

Ce menu est accessible depuis n'importe quel menu principal ou sous-menu. Il permet à l'utilisateur de se déconnecter et de revenir au menu principal.

```
=== DÉCONNEXION ===
1. Se déconnecter
2. Retour au menu précédent
```

---

## **7. Menu Quitter**

Ce menu est accessible depuis le menu principal ou le menu de connexion. Il permet de quitter l'application.

```
=== QUITTER ===
1. Confirmer la fermeture de l'application
2. Retour au menu précédent
```

---

## **Résumé des menus**

| **Menu**                | **Sous-menu**      | **Actions**                                            |
| ----------------------------- | ------------------------ | ------------------------------------------------------------ |
| **Menu Principal**      |                          | Connexion (admin, marchand, client) ou quitter               |
| **Menu Administrateur** | Gérer les marchés      | Créer, afficher, supprimer un marché                       |
|                               | Gérer les marchands     | Ajouter, afficher, supprimer un marchand                     |
|                               | Gérer les utilisateurs  | Ajouter, afficher, supprimer un utilisateur                  |
|                               | Consulter les rapports   | Ventes, stocks, performances des marchands                   |
| **Menu Marchand**       | Gérer mon stock         | Ajouter, retirer, afficher des produits                      |
|                               | Consulter mes ventes     | Afficher les ventes par mois ou par produit                  |
|                               | Gérer mes promotions    | Créer, afficher, supprimer des promotions                   |
| **Menu Client**         | Rechercher un produit    | Rechercher par nom ou catégorie                             |
|                               | Gérer mon panier        | Afficher, ajouter, retirer des produits, passer une commande |
|                               | Consulter mon historique | Afficher les achats récents ou par produit                  |
| **Menu Connexion**      |                          | Se connecter ou quitter                                      |
| **Menu Déconnexion**   |                          | Se déconnecter ou retourner au menu précédent             |
| **Menu Quitter**        |                          | Confirmer la fermeture ou retourner au menu précédent      |
