# 🎬 Rapport de Projet : Gestion Films pour Cinémas (CinéParis)

## 📌 Résumé

Ce projet est une application web complète de gestion de cinéma, permettant la publication de films par les propriétaires et la consultation/réservation par le grand public. Il respecte une architecture stricte en couches (DAO / Service / Controller) et intègre des fonctionnalités avancées de sécurité et de qualité logicielle (CI/CD, Tests).

---

## 🚀 Fonctionnalités Implémentées

### 1. Espace Public (Utilisateurs)

- **Catalogue** : Liste des films à l'affiche avec filtrage par **Ville** (ex: `?ville=Paris`).
- **Détails** : Page dédiée avec synopsis, casting, horaires, et moyenne des notes.
- **Communauté** :
  - **Inscription/Connexion** membre.
  - **Favoris** : Ajouter/Retirer des films de sa liste de cœur.
  - **Avis** : Noter (⭐ 1-5) et commenter les films.
- **Sécurité** : Protection contre les injections XSS sur les affichages de commentaires/titres.

### 2. Espace Propriétaire (Back-Office)

- **Tableau de Bord** : Réservé aux utilisateurs Staff/Admin.
- **Gestion des Programmations** :
  - Formulaire de création unifié (Film + Séance).
  - **Dédoublonnage intelligent** : Réutilisation des fiches films existantes.
  - Édition et Suppression (CRUD) des séances.
  - **Sécurité** : Validation stricte des données (Dates, Durée, XSS).

### 3. Administration & Modération

- Interface Django Admin pour la gestion globale.
- **Modération** : Suppression des commentaires inappropriés (gardant la note) par les admins.

---

## 🛠️ Architecture Technique

Le projet suit scrupuleusement le modèle **M-V-T (Model-View-Template)** Django adapté en architecture 3-tiers :

1.  **Modèles (Data Layer)** : `api/models.py` (Cinema, Film, Programmation, Review, Favorite).
2.  **DAO (Data Access Object)** : `api/dao.py` (Accès brut à la BDD, aucune logique métier).
3.  **Services (Business Layer)** : `api/services.py` (Règles métier, validation date, orchestration).
4.  **Contrôleurs (Views)** : `api/views.py` (Gestion des requêtes HTTP, permissions, appels services).
5.  **Présentation (Templates)** : HTML5 + CSS3 (Dark Mode) + JS Vanilla (AJAX).

---

## 🔐 Qualité et Sécurité (DevOps)

Une attention particulière a été portée à la robustesse du code :

- **Intégration Continue (CI)** : Workflow GitHub Actions (`.github/workflows/ci.yml`) exécutant les tests à chaque push.
- **Tests Automatisés** : Suite de tests (`api/tests.py`) validant :
  - La sécurité des API (Accès interdit aux anonymes).
  - La création de films.
  - Le filtrage public.
- **Audit de Code (Lint & Vulnérabilités)** :
  - ✅ **Bandit** : Audit de sécurité statique (Aucune faille critique détectée).
  - ✅ **Safety** : Vérification des dépendances (Pip mis à jour v25.3 pour corriger CVE-2025-8869).
  - ✅ **Flake8** : Respect des conventions de style PEP8.
  - 🛡️ **Patch XSS** : Désinfection des entrées utilisateurs (Titres, Commentaires) côté Front.

---

## 🏁 Guide de Démarrage

### Pré-requis

- Python 3.11+
- Virtualenv

### Installation

```bash
# 1. Cloner et installer les dépendances
git clone <repo>
pip install -r requirements.txt

# 2. Lancer les migrations
python manage.py migrate

# 3. (Optionnel) Peupler la base de données
python populate_db.py

# 4. Lancer le serveur
python manage.py runserver
```

### Comptes de Démonstration

- **Admin Team** : `admin` / `admin123` (Accès complet)
- **Producteur** : `producteur` / `producteur_pass_2024` (Espace Propriétaire)
- **Visiteur** : `cinephile` / `cinephile_pass_2024` (Espace Public)

---

_Généré par Antigravity Agent - Janvier 2026_
