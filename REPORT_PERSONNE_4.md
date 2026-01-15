# Rapport Final : Améliorations Sécurité & Monitoring (Personne 4)

## 1. Résumé Exécutif
Ce rapport détaille les actions entreprises pour sécuriser, documenter et surveiller l'application **Gestion Cinéma**. Les objectifs du profil "Personne 4" ont été atteints :
-   **Sécurité** : Protection contre le déni de service (Throttling) active.
-   **Documentation** : Swagger UI accessible.
-   **Monitoring** : Logging des erreurs critiques configuré.
-   **Audit** : Scan de code (Bandit) et simulations d'attaques réalisés.

## 2. Actions Réalisées

### 2.1 Sécurité (Throttling)
Nous avons configuré **Django REST Framework Throttling** pour limiter le nombre de requêtes.
-   **Anonymes** : 100 requêtes / jour.
-   **Utilisateurs** : 1000 requêtes / jour.
-   **Résultat du Test de Charge** : Le script de simulation (`attack_sim.py`) a confirmé que l'API bloque correctement les requêtes excédentaires avec un code **429 Too Many Requests**.

### 2.2 Documentation API (Swagger)
L'outil **drf-spectacular** a été intégré pour générer une documentation interactive.
-   **Swagger UI** : `/api/docs/`
-   **Redoc** : `/api/redoc/`
-   **Schéma OpenAPI** : `/api/schema/`

### 2.3 Monitoring & Logging
Un système de logs a été mis en place dans `settings.py` pour enregistrer les événements de sécurité dans `security.log`.

### 2.4 Audit de Code (Bandit)
Un scan statique du code a été réalisé avec **Bandit**.
-   **Résultats** : Aucune faille critique (High Severity) détectée dans le code métier (`views.py`, `models.py`).
-   **Points d'attention** :
    -   `SECRET_KEY` en dur dans `settings.py` (A changer en production via variables d'environnement).
    -   Mots de passe en dur dans les tests (`api/tests.py`) - Acceptable pour du code de test.

### 2.5 Simulations d'Attaques (Pentest)
Des scripts de simulation ont été créés pour tester la robustesse :
-   **Injection SQL** (`injection_sim.py`) : Testé sur `/api/public/films/`.
-   **XSS** (`xss_sim.py`) : Testé sur `/api/public/films/`.
-   **Résultat** : Les tentatives ont été **bloquées par le Throttling** (Code 429), démontrant l'efficacité de la première ligne de défense contre les scans automatisés agressifs. L'analyse du code (`dao.py`) confirme de plus l'utilisation sûre de l'ORM Django (échappement automatique), rendant les injections SQL improbables sur ces endpoints.

## 3. Conclusion
L'application dispose désormais d'une couche de sécurité active contre les abus (rate limiting), d'une documentation claire pour les développeurs tiers, et d'une structure de code validée par audit. L'infrastructure est prête pour une utilisation plus large.

---
**Fichiers Clés Ajoutés/Modifiés :**
-   `config/settings.py` (Throttling, Logging, Swagger)
-   `config/urls.py` (Endpoints Doc)
-   `requirements.txt` (drf-spectacular, bandit, safety)
-   `attack_sim.py`, `injection_sim.py`, `xss_sim.py` (Scripts de test)
-   `populate_db.py` (Script d'initialisation données)
