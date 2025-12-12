import os
import django
from datetime import date, time

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Film, Cinema, Programmation

def populate():
    print("Nettoyage de la base de données...")
    Programmation.objects.all().delete()
    Film.objects.all().delete()
    Cinema.objects.all().delete()
    
    # --- CINEMAS ---
    mk2 = Cinema.objects.create(nom="MK2 Bibliothèque", ville="Paris 13", adresse="128 Av. de France")
    ugc = Cinema.objects.create(nom="UGC Ciné Cité Les Halles", ville="Paris 01", adresse="Forum des Halles")
    gaumont = Cinema.objects.create(nom="Gaumont Alésia", ville="Paris 14", adresse="73 Av. du Général Leclerc")
    pathe = Cinema.objects.create(nom="Pathé Wepler", ville="Paris 18", adresse="140 Bd de Clichy")
    ugc_lyon = Cinema.objects.create(nom="UGC Lyon Bastille", ville="Paris 12", adresse="12 Rue de Lyon")
    
    print("Cinémas créés.")

    # --- FILMS ---
    inception = Film.objects.create(
        titre="Inception",
        realisateur="Christopher Nolan",
        acteurs="Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        duree="2h 28min",
        age_min="12+",
        description="Dom Cobb est un voleur expérimenté – le meilleur dans l'art dangereux de l'extraction : voler les secrets les plus précieux d'une personne pendant qu'elle rêve.",
        image_url="https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg"
    )

    lotr = Film.objects.create(
        titre="Le Seigneur des Anneaux",
        realisateur="Peter Jackson",
        acteurs="Elijah Wood, Ian McKellen",
        duree="2h 58min",
        age_min="Tous publics",
        description="Un jeune hobbit, Frodon Sacquet, hérite d'un anneau magique.",
        image_url="https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"
    )

    dune = Film.objects.create(
        titre="Dune",
        realisateur="Denis Villeneuve",
        acteurs="Timothée Chalamet, Rebecca Ferguson, Oscar Isaac",
        duree="2h 35min",
        age_min="Tous publics",
        description="L'histoire de Paul Atreides, jeune homme aussi doué que brillant, voué à connaître un destin hors du commun qui le dépasse totalement.",
        image_url="https://upload.wikimedia.org/wikipedia/en/8/8e/Dune_%282021_film%29.jpg"
    )

    parasite = Film.objects.create(
        titre="Parasite",
        realisateur="Bong Joon-ho",
        acteurs="Song Kang-ho, Lee Sun-kyun",
        duree="2h 12min",
        age_min="12+",
        description="Toute la famille de Ki-taek est au chômage, et s’intéresse fortement au train de vie de la richissime famille Park.",
        image_url="https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
    )

    spiderman = Film.objects.create(
        titre="Spider-Man: Across the Spider-Verse",
        realisateur="Joaquim Dos Santos",
        acteurs="Shameik Moore, Hailee Steinfeld",
        duree="2h 20min",
        age_min="Tous publics",
        description="Miles Morales traverse le Multivers et rencontre une équipe de Spider-People chargée de protéger son existence même.",
        image_url="https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg"
    )

    print("Films créés.")

    # --- PROGRAMMATIONS ---
    # Inception
    Programmation.objects.create(film=inception, cinema=mk2, date_debut=date(2025, 12, 1), date_fin=date(2025, 12, 31), jours="Lundi,Mercredi,Vendredi", heure=time(20, 0))
    
    # LOTR
    Programmation.objects.create(film=lotr, cinema=ugc, date_debut=date(2025, 12, 1), date_fin=date(2025, 12, 31), jours="Mardi,Jeudi,Samedi", heure=time(18, 0))

    # Dune
    Programmation.objects.create(film=dune, cinema=gaumont, date_debut=date(2025, 12, 1), date_fin=date(2025, 12, 31), jours="Lundi,Mardi,Dimanche", heure=time(20, 30))

    # Parasite
    Programmation.objects.create(film=parasite, cinema=pathe, date_debut=date(2025, 12, 1), date_fin=date(2025, 12, 31), jours="Vendredi,Samedi", heure=time(21, 0))

    # Spider-Man
    Programmation.objects.create(film=spiderman, cinema=ugc_lyon, date_debut=date(2025, 12, 1), date_fin=date(2025, 12, 31), jours="Mercredi,Samedi,Dimanche", heure=time(14, 0))

    print("Programmations créées.")
    print("Terminé ! La base de données est prête.")

if __name__ == '__main__':
    populate()
