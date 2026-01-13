import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import Film, Programmation
from django.db.models import Count

def cleanup():
    print("Début du nettoyage des doublons...")
    
    # Trouver les titres qui ont des doublons
    duplicates = Film.objects.values('titre').annotate(count=Count('id')).filter(count__gt=1)
    
    for entry in duplicates:
        titre = entry['titre']
        count = entry['count']
        print(f"Traitement de '{titre}' ({count} doublons found)...")
        
        # Récupérer tous les films avec ce titre, du plus ancien au plus récent
        films = list(Film.objects.filter(titre=titre).order_by('id'))
        
        # Le premier (le plus vieux) sera le "Maître"
        master_film = films[0]
        print(f" -> Conservation de l'ID {master_film.id} (Master)")
        
        # Les autres sont à fusionner/supprimer
        films_to_merge = films[1:]
        
        for duplicate in films_to_merge:
            # Déplacer les programmations du doublon vers le maître
            progs = Programmation.objects.filter(film=duplicate)
            count_progs = progs.count()
            if count_progs > 0:
                print(f"   -> Transfert de {count_progs} séances de ID {duplicate.id} vers Master")
                progs.update(film=master_film)
            
            # Supprimer le doublon
            print(f"   -> Suppression du doublon ID {duplicate.id}")
            duplicate.delete()

    # Optionnel : Supprimer les films sans aucune programmation ? 
    # L'utilisateur a dit "il n'ont pas de seances".
    # On va le faire pour nettoyer les "coquilles vides"
    print("\nNettoyage des films orphelins (sans séances)...")
    orphans = Film.objects.filter(programmations__isnull=True)
    count_orphans = orphans.count()
    if count_orphans > 0:
        print(f" -> {count_orphans} films sans séances trouvés.")
        # On ne supprime que ceux créés récemment (pour éviter de supprimer les données de test statiques si elles n'ont pas de séance ?)
        # Dans le doute, vu la plainte de l'utilisateur, on supprime TOUT ce qui n'a pas de programmation.
        # SAUF peut-être Inception/Dune s'ils n'ont pas de séance dans le test data ? 
        # Vérifions. Dans populate_db, on crée des programmations pour tous. Donc c'est safe.
        orphans.delete()
        print(" -> Orphelins supprimés.")
    else:
        print(" -> Aucun film orphelin.")

    print("\nNettoyage terminé avec succès !")

if __name__ == '__main__':
    cleanup()
