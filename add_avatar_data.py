import os
import django
from datetime import datetime, time, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Film, Cinema, Programmation

def add_avatar_data():
    # 1. Données du Film
    film_data = {
        "titre": "Avatar: Fire and Ash",
        "realisateur": "James Cameron",
        "acteurs": "Sam Worthington, Zoe Saldaña, Sigourney Weaver, Stephen Lang, Oona Chaplin",
        "duree": "3h 17min",
        "age_min": "12+",
        "description": (
            "Jake Sully et Neytiri sont confrontés à une nouvelle tribu Na'vi agressive, "
            "le peuple des cendres (Ash People), mené par la redoutable Varang. "
            "Alors qu'ils pleurent la perte de Neteyam, ils doivent protéger leur famille "
            "contre cette nouvelle menace volcanique."
        ),
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYEtHEQJ8hI73Tq3ArV2DH4LGttg1aVUw2JwM3daLQefWXnQCdP3bC7PsmwEhF1Z7UNQ_CWDlFnW1CHt8OmiCpm2yGHEykNV6C5TI8Oa4z&s=10"
    }

    # Création ou Récupération du Film
    film, created = Film.objects.get_or_create(
        titre__iexact=film_data["titre"],
        defaults=film_data
    )
    
    if created:
        print(f"[SUCCESS] Film '{film.titre}' créé.")
    else:
        print(f"[INFO] Le film '{film.titre}' existait déjà. Mise à jour des données...")
        for key, value in film_data.items():
            setattr(film, key, value)
        film.save()

    # 2. Liaison à un Cinéma (On prend le premier dispo, généralement MK2)
    cinema = Cinema.objects.first()
    if not cinema:
        print("[ERROR] Aucun cinéma trouvé pour programmer la séance.")
        return

    # 3. Création d'une séance (Programmation)
    # On crée une séance pour la semaine prochaine
    prog_data = {
        "film": film,
        "cinema": cinema,
        "date_debut": date(2025, 12, 20),
        "date_fin": date(2025, 12, 30),
        "jours": "Mercredi, Vendredi, Samedi",
        "heure": time(20, 30)
    }

    # On vérifie si une séance identique existe déjà pour ne pas spammer
    prog, p_created = Programmation.objects.get_or_create(
        film=film,
        cinema=cinema,
        date_debut=prog_data["date_debut"],
        heure=prog_data["heure"],
        defaults=prog_data
    )

    if p_created:
        print(f"[SUCCESS] Séance ajoutée au cinéma '{cinema.nom}' (ville: {cinema.ville}).")
    else:
        print(f"[INFO] Une séance existe déjà pour ce film au '{cinema.nom}'.")

if __name__ == '__main__':
    add_avatar_data()
