from . import dao
from django.core.exceptions import ValidationError
from datetime import datetime

"""
COUCHE SERVICE
Responsabilité : Logique (Validation, Transformation, Orchestration).
"""

def list_movies_service(city_filter=None):
    """
    Service 2: Récupération des films.
    Si une ville est spécifiée, on filtre les films.
    """
    if city_filter:
        seances = dao.get_seances_by_city(city_filter)
        # On extrait les films uniques de ces séances
        films = list({s.film for s in seances})
        return films
    else:
        return dao.get_all_films()

def get_movie_details_service(film_id):
    """
    Service 3: Détails d'un film.
    """
    film = dao.get_film_by_id(film_id)
    if not film:
        return None
    # On pourrait ajouter ici d'autres données enrichies (critiques, etc.)
    return film

def create_projection_service(data):
    """
    Service 1: Publication d'une séance par un propriétaire.
    Règle métier : Date fin > Date début.
    """
    # Validation basique
    start_date = data.get('date_debut')
    end_date = data.get('date_fin')

    if start_date and end_date and start_date > end_date:
        raise ValidationError("La date de fin doit être postérieure à la date de début.")
    
    # Règle métier : Vérifier les jours (simplifié)
    days = data.get('jours', '')
    if len(days.split(',')) > 7:
        raise ValidationError("Impossible de programmer plus de 7 jours par semaine.")

    return dao.create_seance(data)