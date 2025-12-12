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

def get_seances_by_city(city_name):
    """
    Retourne les programmations pour une ville donnée.
    Peut être utilisé pour filtrer les films disponibles dans une ville.
    """
    return Programmation.objects.filter(cinema__ville__icontains=city_name)

def create_film(data):
    return Film.objects.create(**data)

def create_seance(data):
    return Programmation.objects.create(**data)
