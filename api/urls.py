from django.urls import path
from . import views

urlpatterns = [
    # Service 2 : Accueil / Recherche public
    path('', views.public_search_view, name='home'),
    
    # Service 3 : Détails d'un film
    path('film/<int:film_id>/', views.movie_details_view, name='movie_details'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # Service 1 : Espace Propriétaire (Protégé)
    path('proprietaire/', views.owner_dashboard_view, name='owner_dashboard'),
    
    # Espace Membre
    path('mes-favoris/', views.favorites_view, name='favorites'),
    path('api/favorites/toggle/', views.ToggleFavoriteAPI.as_view(), name='toggle_favorite'),
    path('api/reviews/', views.ReviewCreateAPI.as_view(), name='create_review'),
    path('api/reviews/<int:pk>/moderate/', views.ReviewModerateAPI.as_view(), name='moderate_review'),

    # --- API REST ENDPOINTS (Personne 2) ---
    # GET /api/public/films?ville=Paris
    path('api/public/films/', views.PublicFilmListAPI.as_view(), name='public_films'),
    # GET /api/public/films/{id}
    path('api/public/films/<int:pk>/', views.PublicFilmDetailAPI.as_view(), name='public_film_detail'),

    # POST /api/cinemas/{id}/films (Création film pour un cinéma)
    # POST /api/cinemas/{id}/films/{film_id}/programmations (Ajout programmation)
    path('api/cinemas/<int:cinema_id>/films/', views.CinemaFilmCreateAPI.as_view(), name='cinema_film_create'),
    path('api/cinemas/<int:cinema_id>/films/<int:film_id>/programmations/', views.CinemaProgrammationCreateAPI.as_view(), name='cinema_programmation_create'),
    
    # GET /api/cinemas/{id}/programmations/ (Liste des films du cinéma)
    path('api/cinemas/<int:cinema_id>/programmations/', views.CinemaProgrammationListAPI.as_view(), name='cinema_programmation_list'),

    # GET, PUT, DELETE /api/programmations/{pk}/
    path('api/programmations/<int:pk>/', views.ProgrammationRetrieveUpdateDestroyAPI.as_view(), name='programmation_detail'),

    # PUT /api/films/{pk}/
    path('api/films/<int:pk>/', views.FilmRetrieveUpdateDestroyAPI.as_view(), name='film_update'),
]
