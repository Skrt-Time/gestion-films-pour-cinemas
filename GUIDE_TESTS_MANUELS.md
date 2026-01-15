# Guide de Tests de Sécurité Manuels

Ce guide vous explique comment vérifier vous-même la sécurité de l'application via le navigateur.

## 1. Test de Protection Anti-Surcharge (Throttling)
**Objectif** : Vérifier que l'API bloque les requêtes excessives.

1.  Ouvrez la page d'accueil de l'application : [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
2.  Assurez-vous d'être **Déconnecté** (pour utiliser la limite "Anonyme").
3.  Rafraîchissez la page (`F5` ou `Ctrl+R`) très rapidement et en continu (environ 50-100 fois).
4.  **Résultat attendu** :
    *   Au bout d'un moment, les films ne s'affichent plus.
    *   Si vous ouvrez la console du navigateur (`F12` > Console), vous verrez des erreurs rouges : `429 Too Many Requests`.
    *   C'est la preuve que le serveur a bloqué votre adresse IP temporairement.

## 2. Test d'Injection XSS (Cross-Site Scripting)
**Objectif** : Vérifier qu'un attaquant ne peut pas exécuter de Javascript malveillant via les champs de saisie.

1.  Connectez-vous à l'application.
2.  Allez sur la page de détails d'un film.
3.  Cherchez la section des **Commentaires/Avis** (si disponible) ou utilisez la **Barre de Recherche** sur l'accueil.
4.  Entrez le texte suivant : `<script>alert('PIRATÉ')</script>`
5.  Validez.
6.  **Résultat attendu** :
    *   Le texte doit s'afficher tel quel à l'écran : `<script>alert('PIRATÉ')</script>`.
    *   **Aucune** fenêtre d'alerte (pop-up) ne doit apparaître.
    *   Cela prouve que Django a bien "échappé" les caractères spéciaux et les traite comme du texte inoffensif.

## 3. Test d'Injection SQL
**Objectif** : Vérifier qu'on ne peut pas manipuler la base de données via l'URL.

1.  Ouvrez la documentation API Swagger : [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/).
2.  Cherchez le endpoint `GET /api/public/films/`.
3.  Cliquez sur "Try it out".
4.  Dans le champ `ville`, entrez : `' OR 1=1 --`
5.  Cliquez sur "Execute".
6.  **Résultat attendu** :
    *   Code réponse **200** avec une liste vide `[]` OU une liste normale filtrée littéralement sur cette chaîne bizarre.
    *   Code réponse **400 Bad Request**.
    *   **Jamais** de code **500 Internal Server Error** (ce qui indiquerait un crash SQL).
    *   Cela prouve que l'ORM Django protège les requêtes.

## 4. Test d'Accès Non Autorisé (Permissions)
**Objectif** : Vérifier que l'interface administrateur est protégée.

1.  Déconnectez-vous.
2.  Essayez d'accéder directement au Dashboard Propriétaire : [http://127.0.0.1:8000/proprietaire/](http://127.0.0.1:8000/proprietaire/).
3.  **Résultat attendu** :
    *   Vous devez être redirigé automatiquement vers la page de Login (`/login/?next=/proprietaire/`).
    *   L'accès direct est impossible.

## 5. Vérification des Logs
1.  Après avoir fait ces tests, ouvrez le fichier `security.log` à la racine du projet.
2.  Vous devriez y voir des traces des accès (selon la config de logging), confirmant que le système surveille l'activité.
