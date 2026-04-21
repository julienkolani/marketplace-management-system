# **Pipeline d'utilisation**

## **1. Pipeline d'utilisation pour l'administrateur**

### **1.1 Créer un marché**

1. **Se connecter** :
   - L'administrateur ouvre l'application et se connecte avec son identifiant et son mot de passe.
2. **Accéder au tableau de bord** :
   - Il accède à la section "Gestion des marchés".
3. **Créer un marché** :
   - Il clique sur "Créer un marché".
   - Il saisit la taille du marché (exemple : 10x10).
   - Il valide la création.
4. **Confirmation** :
   - Le système affiche un message de succès et met à jour la liste des marchés.

---

### **1.2 Ajouter un marchand**

1. **Se connecter** :
   - L'administrateur se connecte à l'application.
2. **Accéder à la gestion des marchands** :
   - Il accède à la section "Gestion des marchands".
3. **Sélectionner un marché** :
   - Il choisit un marché existant dans la liste.
4. **Ajouter un marchand** :
   - Il clique sur "Ajouter un marchand".
   - Il saisit les informations du marchand (nom, produits initiaux, position dans la grille).
   - Il valide l'ajout.
5. **Confirmation** :
   - Le système vérifie que l'emplacement est libre et ajoute le marchand.
   - Un message de succès est affiché.

---

### **1.3 Supprimer un utilisateur**

1. **Se connecter** :
   - L'administrateur se connecte à l'application.
2. **Accéder à la gestion des utilisateurs** :
   - Il accède à la section "Gestion des utilisateurs".
3. **Rechercher l'utilisateur** :
   - Il recherche l'utilisateur à supprimer par son nom ou son identifiant.
4. **Supprimer l'utilisateur** :
   - Il clique sur "Supprimer" à côté de l'utilisateur.
   - Il confirme la suppression.
5. **Confirmation** :
   - Le système supprime l'utilisateur et affiche un message de succès.

---

### **1.4 Générer un rapport des ventes**

1. **Se connecter** :
   - L'administrateur se connecte à l'application.
2. **Accéder aux rapports** :
   - Il accède à la section "Rapports et analyses".
3. **Choisir le type de rapport** :
   - Il sélectionne "Rapport des ventes".
4. **Configurer le rapport** :
   - Il choisit la période (exemple : dernier mois) et les marchands à inclure.
5. **Générer le rapport** :
   - Il clique sur "Générer".
6. **Visualiser le rapport** :
   - Le système affiche un tableau et des graphiques (histogrammes, diagrammes circulaires).

---

## **2. Pipeline d'utilisation pour le marchand**

### **2.1 Ajouter un produit au stock**

1. **Se connecter** :
   - Le marchand se connecte à l'application.
2. **Accéder à la gestion du stock** :
   - Il accède à la section "Gestion du stock".
3. **Ajouter un produit** :
   - Il clique sur "Ajouter un produit".
   - Il saisit les détails du produit (nom, quantité, prix).
   - Il valide l'ajout.
4. **Confirmation** :
   - Le système met à jour le stock et affiche un message de succès.

---

### **2.2 Consulter l'historique des ventes**

1. **Se connecter** :
   - Le marchand se connecte à l'application.
2. **Accéder à l'historique des ventes** :
   - Il accède à la section "Historique des ventes".
3. **Choisir la période** :
   - Il sélectionne une période (exemple : dernier mois).
4. **Visualiser les ventes** :
   - Le système affiche un tableau détaillé des ventes avec les produits, quantités, et revenus.

---

### **2.3 Mettre à jour le prix d'un produit**

1. **Se connecter** :
   - Le marchand se connecte à l'application.
2. **Accéder à la gestion du stock** :
   - Il accède à la section "Gestion du stock".
3. **Rechercher le produit** :
   - Il recherche le produit à modifier par son nom.
4. **Modifier le prix** :
   - Il clique sur "Modifier" à côté du produit.
   - Il saisit le nouveau prix.
   - Il valide la modification.
5. **Confirmation** :
   - Le système met à jour le prix et affiche un message de succès.

---

## **3. Pipeline d'utilisation pour le client**

### **3.1 Rechercher un produit**

1. **Se connecter** :
   - Le client se connecte à l'application.
2. **Accéder à la recherche** :
   - Il accède à la barre de recherche.
3. **Saisir le produit** :
   - Il saisit le nom du produit recherché.
4. **Visualiser les résultats** :
   - Le système affiche une liste de marchands proposant le produit avec leurs prix et positions.

---

### **3.2 Passer une commande**

1. **Se connecter** :
   - Le client se connecte à l'application.
2. **Ajouter des produits au panier** :
   - Il recherche des produits et les ajoute à son panier.
3. **Valider le panier** :
   - Il accède à son panier et clique sur "Passer la commande".
4. **Choisir les marchands optimaux** :
   - Le système propose les marchands les plus proches et les moins chers.
5. **Confirmer la commande** :
   - Il valide la commande et choisit un mode de paiement.
6. **Confirmation** :
   - Le système enregistre la transaction et met à jour les stocks.

---

### **3.3 Consulter l'historique des achats**

1. **Se connecter** :
   - Le client se connecte à l'application.
2. **Accéder à l'historique des achats** :
   - Il accède à la section "Historique des achats".
3. **Visualiser les achats** :
   - Le système affiche une liste de ses achats précédents avec les détails (produits, prix, date).

---

## **4. Pipeline d'utilisation pour les notifications**

### **4.1 Notifier un marchand d'un stock faible**

1. **Détection du stock faible** :
   - Le système détecte qu'un produit est en stock faible (quantité < seuil).
2. **Envoyer une notification** :
   - Le système envoie une notification au marchand via l'application ou par email.
3. **Visualiser la notification** :
   - Le marchand voit la notification dans son tableau de bord.

---

### **4.2 Notifier un client d'une promotion**

1. **Création d'une promotion** :
   - Un marchand crée une promotion sur un produit.
2. **Détection des clients concernés** :
   - Le système identifie les clients ayant acheté ce produit précédemment.
3. **Envoyer une notification** :
   - Le système envoie une notification aux clients concernés.
4. **Visualiser la notification** :
   - Le client voit la notification dans son tableau de bord.
