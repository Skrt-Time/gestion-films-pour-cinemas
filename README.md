# Résumé des Modifications du Projet

Ce fichier recense l'ensemble des fichiers créés ou modifiés pour répondre aux objectifs de sécurité, de documentation et d'amélioration fonctionnelle ("Personne 4" + Fixes).

## 1. Sécurité & Configuration
*   **`config/settings.py`** :
    *   Activation du **Throttling** (Limitation de débit) pour l'API.
    *   Configuration du **Logging** (Fichier `security.log` pour les erreurs critiques).
    *   Ajout de `drf-spectacular` aux applications installées.
    *   *Ajustement* : Augmentation des limites de throttling (2000/jour) pour éviter les blocages lors des tests.
*   **`requirements.txt`** :
    *   Ajout des bibliothèques : `drf-spectacular`, `bandit`, `safety`.

## 2. Documentation API (Swagger)
*   **`config/urls.py`** :
    *   Ajout des routes `/api/docs/` (Swagger UI) et `/api/schema/`.

## 3. Fonctionnalités & Améliorations
*   **Recherche Polyvalente (Ville + Titre)** :
    *   **`api/dao.py`** : Création de `get_seances_by_search` utilisant des filtres `Q` (OR) pour chercher par ville OU titre.
    *   **`api/services.py`** : Mise à jour du service pour utiliser la nouvelle méthode DAO.
    *   **`api/views.py`** : Mise à jour de `PublicFilmListAPI` pour lire le paramètre `?search=`.
    *   **`api/templates/api/index.html`** : Mise à jour du placeholder de la barre de recherche.
    *   **`api/static/api/js/main.js`** : Adaptation du fetch JS pour envoyer le paramètre `search`.
*   **Correction Bug Création Film** :
    *   **`api/views.py`** : Modification de la logique de création (`CinemaFilmCreateAPI`) pour **mettre à jour** les films existants (ex: ajout d'image URL) au lieu de les ignorer.

## 4. Scripts Utilitaires & Tests (Nouveaux Fichiers)
Ces fichiers ont été ajoutés à la racine pour l'audit et l'initialisation :
*   **`attack_sim.py`** : Script de simulation d'attaque DDoS (Test du Throttling).
*   **`injection_sim.py`** : Script de test de résistance aux injections SQL.
*   **`xss_sim.py`** : Script de test d'injection XSS.
*   **`populate_db.py`** : Script pour remplir la base de données avec des données de test.

## 5. Documentation & Rapports (Nouveaux Fichiers)
*   **`RAPPORT_PROJET.md`** : Rapport final complet fusionnant la présentation générale et les détails de sécurité.
*   **`REPORT_PERSONNE_4.md`** : (Intermédiaire) Rapport spécifique aux tâches de sécurité.
*   **`GUIDE_TESTS_MANUELS.md`** : Guide pas-à-pas pour tester la sécurité manuellement.
