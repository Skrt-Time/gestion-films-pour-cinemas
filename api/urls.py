from django.urls import path
from . import views

urlpatterns = [
    # Service 2 : Accueil / Recherche public
    path('', views.public_search_view, name='home'),
    
    # Service 3 : Détails d'un film
    path('film/<int:film_id>/', views.movie_details_view, name='movie_details'),
    
    # Service 1 : Espace Propriétaire
    path('proprietaire/', views.owner_dashboard_view, name='owner_dashboard'),

    # --- API REST ENDPOINTS (Personne 2) ---
    # GET /api/public/films?ville=Paris
    path('api/public/films/', views.PublicFilmListAPI.as_view(), name='public_films'),
    # GET /api/public/films/{id}
    path('api/public/films/<int:pk>/', views.PublicFilmDetailAPI.as_view(), name='public_film_detail'),

    # POST /api/cinemas/{id}/films (Création film pour un cinéma)
    # POST /api/cinemas/{id}/films/{film_id}/programmations (Ajout programmation)
    path('api/cinemas/<int:cinema_id>/films/', views.CinemaFilmCreateAPI.as_view(), name='cinema_film_create'),
    path('api/cinemas/<int:cinema_id>/films/<int:film_id>/programmations/', views.CinemaProgrammationCreateAPI.as_view(), name='cinema_programmation_create'),
]
