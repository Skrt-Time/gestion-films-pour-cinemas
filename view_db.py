import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Film, Programmation
from django.contrib.auth.models import User

def print_simple(title, rows):
    with open('db_dump.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n=== {title} ===\n")
        if not rows:
            f.write("(Aucune donnée)\n")
        for row in rows:
            f.write(" | ".join(str(r) for r in row) + "\n")

# Clear file
open('db_dump.txt', 'w', encoding='utf-8').close()

print("Opening Database...")
with open('db_dump.txt', 'a', encoding='utf-8') as f:
    f.write("Opening Database...\n")

# Users
users = User.objects.all()
print_simple("UTILISATEURS (ID | Username | Email)", [[u.id, u.username, u.email] for u in users])

# Films
films = Film.objects.all()
print_simple("FILMS (ID | Titre | Durée)", [[f.id, f.titre, f.duree] for f in films])

# Programmations
progs = Programmation.objects.select_related('film', 'cinema').all()
print_simple("PROGRAMMATIONS (ID | Film | Cinéma | Début | Heure)", [[p.id, p.film.titre, p.cinema.nom, p.date_debut, p.heure] for p in progs])
