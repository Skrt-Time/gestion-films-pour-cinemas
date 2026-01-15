# Rapport de Projet : Application REST Gestion Cinéma

## 1. Introduction
Ce projet consiste en la réalisation d'une application Web orientée services REST pour la gestion des projections et de la programmation de films dans les cinémas parisiens. L'objectif était de fournir une plateforme robuste et sécurisée permettant aux propriétaires de cinémas de publier leurs programmations et au grand public de consulter les films disponibles par ville.

## 2. Fonctionnalités de l'Application
L'application répond à deux types d'utilisateurs distincts via trois services principaux :

### Pour le Grand Public (Accès Libre)
*   **Recherche de Films par Ville** : L'utilisateur peut saisir le nom d'une ville (ex: "Paris") pour voir instantanément la liste de tous les films qui y sont actuellement projetés.
*   **Consultation des Détails** : En cliquant sur un film, l'utilisateur accède à une fiche détaillée présentant le titre, le réalisateur, les acteurs, la durée, l'âge minimum requis, ainsi que la liste des cinémas proposant ce film avec les horaires des séances.
*   **Documentation API** : Accès libre à la documentation Swagger (`/api/docs/`) pour tester les endpoints.

### Fonctionnalités Authentifiées (Utilisateurs Connectés)
*   **Gestion de Compte** : Inscription et connexion sécurisée pour accéder aux fonctionnalités avancées.
*   **Système de Favoris** : Possibilité d'ajouter des films à sa liste de favoris ("Ma liste") pour les retrouver facilement.
*   **Notes et Avis** : Les utilisateurs peuvent noter les films (1 à 5 étoiles) et laisser un commentaire écrit.
*   **Modération** : Les administrateurs disposent d'outils pour modérer les commentaires inappropriés.

### Pour les Propriétaires de Cinémas (Accès Réservé)
*   **Gestion des Programmations** : Les cinémas disposent d'un espace dédié ("Espace Propriétaire") où ils peuvent ajouter de nouveaux films à l'affiche. Ils renseignent les détails du film (Titre, Acteurs, etc.) et définissent la programmation (Dates de début et de fin, horaires des séances).

### Pour l'Administration (Superuser)
*   **Administration de la Base de Données** : Une interface d'administration sécurisée (Django Admin) est disponible pour gérer l'ensemble des données (Utilisateurs, Films, Cinémas, Programmations) sans manipulation SQL directe.

## 3. Architecture Technique
Conformément aux exigences du projet, l'application respecte strictement une architecture en couches, favorisant la maintenance, la testabilité et la séparation des responsabilités. Le backend expose une API REST consommée par un frontend léger.

### 3.1 Schéma de l'Architecture
L'application est structurée en 5 couches distinctes :
1.  **Base de Données (Database)** : Stockage persistant des données.
2.  **Couche Accès aux Données (DAO)** : Interface d'abstraction pour les requêtes brutes `dao.py`.
3.  **Couche Service (Business Logic)** : Cœur de la validation métier `services.py`.
4.  **Couche Controller (API View)** : Gestion des requêtes HTTP, permissions et Throttling `views.py`.
5.  **Couche Frontend (Client)** : Interface utilisateur consommant les services REST.

## 4. Technologies Utilisées
Le choix technologique s'est porté sur un stack moderne et robuste :
*   **Langage** : Python (Django 6.0)
*   **API** : Django REST Framework (DRF) 3.16 + CORS Headers
*   **Documentation** : drf-spectacular (OpenAPI 3.0 / Swagger UI)
*   **Sécurité** : Bandit (Audit statique), Safety (Audit dépendances), DRF Throttling
*   **Base de Données** : SQLite (Dev) / PostgreSQL (Prod ready)
*   **Frontend** : HTML5, CSS3 (Design responsive), JavaScript (Fetch API)
*   **CI/CD** : GitHub Actions

## 5. Composants Développés et Implémentation
Pour réaliser cette application, nous avons développé plusieurs composants interconnectés :

### La Structure des Données (Base de Données)
Définie dans `models.py` autour de trois concepts clés (Film, Cinéma, Programmation).
*   **Amélioration Technique** : Champs `PositiveIntegerField` pour la durée et index `db_index=True` pour les performances de recherche.

### L'Accès et la Gestion des Données (DAO & Service)
*   **DAO** : Isolation des requêtes techniques.
*   **Services** : Validation métier "intelligente" (ex: date de fin > date début).

### L'Interface Utilisateur (Frontend)
*   **Page d'Accueil** : Recherche temps réel via JS.
*   **Espace Propriétaire** : Back-office ergonomique avec gestion des erreurs (403 Forbidden).

## 6. Sécurité Avancée, Monitoring et Simulations
Un effort majeur a été porté sur la sécurisation de l'application (Profil "Personne 4"). Nous ne nous sommes pas contentés de la théorie, nous avons éprouvé le système par des simulations d'attaques réelles.

### 6.1 Protection Anti-DDoS (Throttling)
Nous avons configuré **Django REST Framework Throttling** pour limiter le débit des requêtes et prévenir les attaques par déni de service.
*   **Configuration** :
    *   Utilisateurs Anonymes : **2000 requêtes/jour**.
    *   Utilisateurs Authentifiés : **10000 requêtes/jour**.
*   **Simulation & Validation** :
    *   Un script dédié `attack_sim.py` a été développé pour envoyer des requêtes en rafale (multithreading).
    *   **Résultat** : Au-delà du seuil, l'API répond systématiquement par un code **429 Too Many Requests**. Le test a confirmé que le serveur reste stable et rejette les abus.

### 6.2 Audit de Sécurité et Injection (Pentesting)
Nous avons réalisé des tests d'intrusion automatisés via des scripts Python personnalisés :
*   **Injection SQL (`injection_sim.py`)** :
    *   *Scénario* : Injection de payloads malveillants (ex: `' OR 1=1 --`, `UNION SELECT...`) dans les paramètres de recherche d'URL.
    *   *Résultat* : L'ORM de Django échappe automatiquement les paramètres. Les tentatives retournent soit une 404/200 (recherche vide), soit une 400, mais **jamais** de données compromises ou d'erreur 500 exposant la structure de la base.
*   **Cross-Site Scripting XSS (`xss_sim.py`)** :
    *   *Scénario* : Tentative d'insertion de scripts JS (`<script>alert('hack')</script>`) dans les champs de texte.
    *   *Résultat* : Django templates et DRF échappent les caractères spéciaux (`&lt;script&gt;`). Le code n'est pas exécuté par le navigateur.

### 6.3 Audit de Code Statique
*   **Outil** : `Bandit`
*   **Action** : Analyse de l'intégralité du code source (`bandit -r .`).
*   **Résultat** : Aucune faille de sévérité "High" détectée dans la logique métier.
*   **Action Corrective** : Mise en place de variables d'environnement recommandée pour la `SECRET_KEY` en production.

### 6.4 Monitoring
Un système de **Logging** a été configuré dans `settings.py`. Toutes les erreurs critiques (500) et les tentatives d'accès interdit (403) sont archivées dans un fichier `security.log`, permettant une auditabilité post-incident.

## 7. Conclusion
Ce projet a constitué une étape importante dans notre compréhension du développement web moderne et sécurisé.
L'approche technique — centrée sur une architecture REST rigoureuse et une stratégie de sécurité "Defense in Depth" (Throttling + Audit + Validation) — s'est révélée être un atout majeur. Elle nous a permis de livrer une plateforme non seulement fonctionnelle, mais aussi résiliente face aux menaces web courantes.

La mise en place des simulations d'attaques nous a permis de vérifier concrètement l'efficacité de nos protections, transformant des concepts théoriques en garanties techniques prouvées.
