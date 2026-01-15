from .models import Film, Programmation, Cinema

"""
COUCHE DAO (Data Access Object)
Responsabilité : Accès direct à la base de données.
Aucune logique métier complexe ici, juste du CRUD.
"""

def get_all_films():
    return Film.objects.all().order_by('-date_publication')

def get_film_by_id(film_id):
    try:
        return Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        return None

from django.db.models import Q

def get_seances_by_search(query):
    """
    Retourne les programmations qui correspondent soit à la ville du cinéma,
    soit au titre du film.
    """
    return Programmation.objects.filter(
        Q(cinema__ville__icontains=query) | 
        Q(film__titre__icontains=query)
    )

def create_film(data):
    return Film.objects.create(**data)

def create_seance(data):
    return Programmation.objects.create(**data)
