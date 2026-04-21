## **Liste des Tâches Atomiques**

### **1. Gestion du Marché**
1. **Créer une grille 2D pour représenter le marché** :
   - Implémenter une structure de données pour représenter une grille de taille configurable.
2. **Vérifier si un emplacement est libre** :
   - Implémenter une fonction pour vérifier si une position (x, y) est disponible.
3. **Ajouter un marchand à un emplacement** :
   - Implémenter une fonction pour ajouter un marchand à une position spécifique.
4. **Supprimer un marchand d'un emplacement** :
   - Implémenter une fonction pour retirer un marchand de la grille.
5. **Afficher la grille du marché** :
   - Implémenter une fonction pour afficher la grille avec les emplacements occupés et libres.

---

### **2. Gestion des Marchands**
6. **Créer une classe `Marchand`** :
   - Implémenter une classe avec des attributs (nom, stock, position).
7. **Ajouter un produit au stock** :
   - Implémenter une méthode pour ajouter un produit avec une quantité et un prix.
8. **Retirer un produit du stock** :
   - Implémenter une méthode pour retirer une quantité spécifique d'un produit.
9. **Afficher le stock d'un marchand** :
   - Implémenter une méthode pour afficher les produits disponibles et leurs quantités.
10. **Mettre à jour le prix d'un produit** :
    - Implémenter une méthode pour modifier le prix d'un produit.
11. **Enregistrer une vente** :
    - Implémenter une méthode pour enregistrer une transaction dans l'historique des ventes.
12. **Afficher l'historique des ventes** :
    - Implémenter une méthode pour afficher les ventes passées.

---

### **3. Gestion des Clients**
13. **Créer une classe `Client`** :
    - Implémenter une classe avec des attributs (nom, panier, historique d'achats).
14. **Ajouter un produit au panier** :
    - Implémenter une méthode pour ajouter un produit au panier.
15. **Retirer un produit du panier** :
    - Implémenter une méthode pour retirer un produit du panier.
16. **Afficher le panier** :
    - Implémenter une méthode pour afficher les produits dans le panier.
17. **Passer une commande** :
    - Implémenter une méthode pour valider une commande et mettre à jour les stocks.
18. **Afficher l'historique d'achats** :
    - Implémenter une méthode pour afficher les achats précédents.

---

### **4. Gestion des Transactions**
19. **Créer une classe `Transaction`** :
    - Implémenter une classe pour représenter une transaction (produit, quantité, prix, date).
20. **Enregistrer une transaction** :
    - Implémenter une fonction pour enregistrer une transaction dans la base de données.
21. **Afficher les transactions** :
    - Implémenter une fonction pour afficher les transactions passées.

---

### **5. Interface Utilisateur (Terminal)**
22. **Implémenter le menu principal** :
    - Créer un menu avec les options pour se connecter en tant qu'admin, marchand ou client.
23. **Implémenter le menu administrateur** :
    - Ajouter les sous-menus pour gérer les marchés, les marchands, les utilisateurs et les rapports.
24. **Implémenter le menu marchand** :
    - Ajouter les sous-menus pour gérer le stock, consulter les ventes et gérer les promotions.
25. **Implémenter le menu client** :
    - Ajouter les sous-menus pour rechercher des produits, gérer le panier et consulter l'historique d'achats.
26. **Styliser les menus avec Rich** :
    - Utiliser `rich` pour améliorer l'affichage des menus, des titres et des messages.

---

### **6. Recherche et Optimisation**
27. **Rechercher un produit par nom** :
    - Implémenter une fonction pour rechercher un produit par son nom.
28. **Rechercher un produit par catégorie** :
    - Implémenter une fonction pour rechercher un produit par catégorie.
29. **Trouver les marchands les plus proches** :
    - Implémenter une fonction pour calculer la distance entre un client et les marchands.
30. **Optimiser un panier d'achat** :
    - Implémenter une fonction pour recommander les marchands les plus adaptés.

---

### **7. Gestion des Promotions**
31. **Créer une promotion** :
    - Implémenter une fonction pour appliquer une réduction sur un produit.
32. **Afficher les promotions** :
    - Implémenter une fonction pour afficher les promotions en cours.
33. **Supprimer une promotion** :
    - Implémenter une fonction pour retirer une promotion.

---

### **8. Notifications et Alertes**
34. **Notifier un marchand d'un stock faible** :
    - Implémenter une fonction pour envoyer une alerte lorsque le stock est faible.
35. **Notifier un client d'une promotion** :
    - Implémenter une fonction pour informer un client d'une promotion sur un produit.

---

### **9. Gestion des Données MongoDB**
36. **Configurer MongoDB** :
    - Installer et configurer MongoDB pour le projet.
37. **Créer une collection pour les marchés** :
    - Implémenter une collection pour stocker les informations des marchés.
38. **Créer une collection pour les marchands** :
    - Implémenter une collection pour stocker les informations des marchands.
39. **Créer une collection pour les transactions** :
    - Implémenter une collection pour stocker les transactions.
40. **Insérer des données dans MongoDB** :
    - Implémenter des fonctions pour insérer des données dans les collections.
41. **Récupérer des données de MongoDB** :
    - Implémenter des fonctions pour récupérer des données des collections.

---

### **10. Analyse des Données**
42. **Extraire les données MongoDB en DataFrame** :
    - Implémenter une fonction pour charger les données dans un DataFrame Pandas.
43. **Analyser les ventes** :
    - Implémenter une fonction pour identifier les produits les plus vendus.
44. **Générer un histogramme des ventes** :
    - Implémenter une fonction pour créer un histogramme des produits les plus vendus.
45. **Générer un diagramme circulaire des ventes par marchand** :
    - Implémenter une fonction pour créer un diagramme circulaire.
46. **Générer une heatmap des stocks** :
    - Implémenter une fonction pour créer une heatmap des niveaux de stock.

---

### **11. Tests et Validation**
47. **Tester la création d'un marché** :
    - Vérifier que la grille est correctement créée.
48. **Tester l'ajout d'un marchand** :
    - Vérifier qu'un marchand est bien ajouté à un emplacement libre.
49. **Tester la gestion du stock** :
    - Vérifier que les produits sont correctement ajoutés et retirés du stock.
50. **Tester les transactions** :
    - Vérifier que les transactions sont correctement enregistrées.

---

### **12. Documentation**
51. **Documenter les fonctions** :
    - Ajouter des docstrings pour expliquer le fonctionnement de chaque fonction.
52. **Rédiger un guide d'utilisation** :
    - Expliquer comment utiliser chaque fonctionnalité de l'application.

---

### **13. Déploiement et Finalisation**
53. **Nettoyer le code** :
    - Supprimer les commentaires inutiles et optimiser le code.
54. **Préparer une démonstration** :
    - Préparer des scénarios pour montrer toutes les fonctionnalités.
55. **Présenter le projet** :
    - Préparer une présentation pour expliquer le projet et ses fonctionnalités.

---

## **Résumé des Tâches Atomiques**

| **Tâche**                          | **Description**                                                                 |
|------------------------------------|---------------------------------------------------------------------------------|
| **Gestion du marché**              | Créer une grille, vérifier les emplacements, ajouter/supprimer des marchands.   |
| **Gestion des marchands**          | Gérer le stock, enregistrer les ventes, afficher l'historique.                  |
| **Gestion des clients**            | Gérer le panier, passer des commandes, afficher l'historique d'achats.          |
| **Gestion des transactions**       | Enregistrer et afficher les transactions.                                       |
| **Interface utilisateur**          | Implémenter les menus et améliorer l'affichage avec Rich.                       |
| **Recherche et optimisation**      | Rechercher des produits, optimiser les achats.                                  |
| **Gestion des promotions**         | Créer, afficher et supprimer des promotions.                                    |
| **Notifications et alertes**       | Envoyer des alertes pour les stocks faibles et les promotions.                  |
| **Gestion des données MongoDB**    | Configurer MongoDB, créer des collections, insérer/récupérer des données.       |
| **Analyse des données**            | Extraire les données, analyser les ventes, générer des graphiques.              |
| **Tests et validation**            | Tester chaque fonctionnalité pour valider son bon fonctionnement.               |
| **Documentation**                  | Documenter le code et rédiger un guide d'utilisation.                           |
| **Déploiement et finalisation**    | Nettoyer le code, préparer une démonstration et présenter le projet.            |

---
