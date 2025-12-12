# Gestion de Programmation Cinéma (REST API)

Application Web REST pour la gestion des projections de films dans les cinémas parisiens.
Projet académique respectant une architecture stricte en couches.

## 🏗 Structure du Projet

Voici l'organisation des fichiers respectant la séparation des responsabilités :

```text
gestion-films-pour-cinemas/       <-- Racine
├── .github/workflows/            <-- CI/CD (Tests automatiques)
├── api/                          <-- Application Cœur
│   ├── dao.py                    <-- COUCHE ACCÈS DONNÉES (Requêtes BDD)
│   ├── services.py               <-- COUCHE SERVICE (Logique métier / Règles)
│   ├── views.py                  <-- COUCHE CONTROLLER (Endpoints HTTP)
│   ├── models.py                 <-- Modèles de données (Tables SQL)
│   └── serializers.py            <-- Transformation JSON
├── config/                       <-- Configuration globale Django
├── venv/                         <-- Environnement Virtuel (Bibliothèques)
├── db.sqlite3                    <-- Base de données
└── manage.py                     <-- Script de gestion
```

[cite_start]Ce projet est une application Web orientée services REST permettant la gestion des projections de films dans les cinémas parisiens[cite: 3].
[cite_start]Il respecte une architecture stricte en couches (Base de données + Accès + Service + Controller).

## 🏗 Architecture Technique

Le projet utilise **Django** et **Django REST Framework**.
L'architecture logicielle est divisée en couches distinctes pour respecter les principes de séparation des responsabilités :

1.  **Base de Données** : SQLite (Stockage physique).
2.  **Couche Accès (DAO)** : `api/dao.py` et `models.py` (Interactions directes avec la BDD).
3.  [cite_start]**Couche Service** : `api/services.py` (Logique métier, ex: règle des créneaux de 3 jours [cite: 7]).
4.  **Couche Controller** : `api/views.py` (Gestion des requêtes HTTP et réponses JSON).
5.  **Front-end** : Interface Web consommant l'API (HTML/JS/CSS).

## 🚀 Fonctionnalités (Services REST)

[cite_start]L'application expose trois services principaux[cite: 2]:

* [cite_start]**Service 1 (Propriétaires)** : Publication des films et programmation (Titre, durée, créneaux)[cite: 5, 6].
    * [cite_start]*Note :* Un film est programmé pour une période donnée, 3 jours par semaine[cite: 7].
* [cite_start]**Service 2 (Public)** : Recherche de films par ville via une page en accès libre[cite: 9, 10].
* [cite_start]**Service 3 (Détails)** : Consultation des détails d'un film spécifique (Réalisateur, acteurs, âge requis)[cite: 11].

## 🛠 Installation et Lancement

1.  **Cloner le projet :**
    ```bash
    git clone [https://github.com/VOTRE-USER/gestion-films-pour-cinemas.git](https://github.com/VOTRE-USER/gestion-films-pour-cinemas.git)
    cd gestion-films-pour-cinemas
    ```

2.  **Préparer l'environnement :**
    ```bash
    # Créer l'environnement virtuel
    python -m venv venv
    
    # Activer (Windows)
    .\venv\Scripts\Activate
    
    # Activer (Mac/Linux)
    source venv/bin/activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Lancer le serveur :**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## ✅ Qualité et CI/CD

Ce projet intègre **GitHub Actions** pour l'intégration continue.
À chaque `push` sur la branche `main`, les tests unitaires (`python manage.py test`) sont exécutés automatiquement pour garantir la non-régression.