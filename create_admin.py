import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = "admin"
    password = "admin123"
    email = "admin@example.com"
    
    if User.objects.filter(username=username).exists():
        print(f"L'utilisateur '{username}' existe déjà.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"Superutilisateur '{username}' créé avec succès !")
        print(f"Mot de passe : {password}")

if __name__ == '__main__':
    create_admin()
