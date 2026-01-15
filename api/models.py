from django.db import models

class Cinema(models.Model):
    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    adresse = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nom} - {self.ville}"

class Film(models.Model):
    titre = models.CharField(max_length=255)
    realisateur = models.CharField(max_length=255)
    acteurs = models.TextField(help_text="Liste des acteurs séparés par des virgules")
    duree = models.CharField(max_length=50, help_text="Ex: 2h 30min")
    langue = models.CharField(max_length=100, default="Français", help_text="Ex: VOSTFR, VF")
    age_min = models.CharField(max_length=50, default="Tous publics")
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, help_text="Lien vers l'affiche du film")
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Programmation(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='programmations')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='programmations')
    date_debut = models.DateField()
    date_fin = models.DateField()
    jours = models.CharField(max_length=255, help_text="Jours de la semaine (ex: Lundi,Mercredi,Vendredi)")
    heure = models.TimeField()

    def __str__(self):
        return f"{self.film.titre} à {self.cinema.nom} le {self.jours} à {self.heure}"

class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film') # Un utilisateur ne peut liker qu'une fois un film

    def __str__(self):
        return f"{self.user.username} likes {self.film.titre}"

class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5, help_text="Note de 1 à 5")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film') # Un seul avis par film par utilisateur

    def __str__(self):
        return f"{self.user.username} - {self.film.titre} ({self.rating}/5)"
