# Marketplace Management System

Application CLI complète de gestion de marché avec système multi-rôles, base de données MongoDB et tableau de bord de visualisation.

## Fonctionnalités

- Trois rôles : Admin (gestion des marchés sur grille 2D), Marchand (inventaire, promotions), Client (panier, historique)
- Authentification bcrypt avec gestion des sessions
- Interface terminal enrichie avec Rich (couleurs, tableaux, menus)
- Dashboard interactif Dash/Plotly : positions des marchands, stocks, revenus, séries temporelles

## Stack technique

- Python, MongoDB, MongoEngine
- Rich (interface terminal)
- Plotly, Dash (visualisation)
- Docker, bcrypt

## Installation

```bash
pip install -r requirements.txt
python main.py
```
