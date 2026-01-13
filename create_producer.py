import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def create_producer():
    username = 'producteur'
    password = 'producteur_pass_2024'
    email = 'producteur@cineparis.com'

    if User.objects.filter(username=username).exists():
        print(f"L'utilisateur {username} existe déjà.")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_user(username=username, password=password, email=email)
        print(f"Utilisateur {username} créé.")

    # Give staff rights to access /proprietaire
    user.is_staff = True
    user.save()
    print(f"Droits 'Staff' (Producteur) attribués à {username}.")

if __name__ == '__main__':
    create_producer()
