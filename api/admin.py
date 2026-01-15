from django.contrib import admin
from .models import Cinema, Film, Programmation

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'id')
    search_fields = ('nom', 'ville')

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('titre', 'realisateur', 'duree', 'age_min', 'id')
    search_fields = ('titre', 'realisateur')
    list_filter = ('age_min',)

@admin.register(Programmation)
class ProgrammationAdmin(admin.ModelAdmin):
    list_display = ('film', 'cinema', 'jours', 'heure', 'date_debut', 'date_fin')
    list_filter = ('cinema', 'film', 'date_debut')
    search_fields = ('film__titre', 'cinema__nom')
