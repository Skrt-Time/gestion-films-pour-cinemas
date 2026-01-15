import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Cinema, Film, Programmation

def populate():
    print("Populating database...")

    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'password123')
        print("Superuser 'admin' created (password: password123)")

    # Create Cinemas
    cinemas = [
        Cinema(nom="Le Grand Rex", ville="Paris", adresse="1 Bd Poissonnière"),
        Cinema(nom="UGC Ciné Cité", ville="Paris", adresse="Les Halles"),
        Cinema(nom="Pathé Bellecour", ville="Lyon", adresse="Rue de la République"),
    ]
    for c in cinemas:
        c.save()
    print(f"{len(cinemas)} cinemas created.")

    # Create Films
    films = [
        Film(titre="Inception", realisateur="Christopher Nolan", acteurs="Leonardo DiCaprio, Elliot Page", duree="2h 28min", description="Un voleur vole des secrets dans les rêves."),
        Film(titre="The Dark Knight", realisateur="Christopher Nolan", acteurs="Christian Bale, Heath Ledger", duree="2h 32min", description="Batman affronte le Joker."),
        Film(titre="Parasite", realisateur="Bong Joon-ho", acteurs="Song Kang-ho, Lee Sun-kyun", duree="2h 12min", description="Une famille pauvre s'infiltre chez une famille riche."),
    ]
    for f in films:
        f.save()
    print(f"{len(films)} films created.")

    # Create Programmations
    progs = [
        Programmation(film=films[0], cinema=cinemas[0], date_debut=date.today(), date_fin=date.today() + timedelta(days=7), jours="Lundi,Mardi", heure=time(20, 0)),
        Programmation(film=films[1], cinema=cinemas[0], date_debut=date.today(), date_fin=date.today() + timedelta(days=7), jours="Mercredi,Jeudi", heure=time(21, 0)),
        Programmation(film=films[2], cinema=cinemas[1], date_debut=date.today(), date_fin=date.today() + timedelta(days=7), jours="Vendredi,Samedi", heure=time(18, 30)),
    ]
    for p in progs:
        p.save()
    print(f"{len(progs)} programmations created.")

    print("Database population completed.")

if __name__ == "__main__":
    populate()
