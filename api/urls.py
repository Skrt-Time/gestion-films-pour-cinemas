from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

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
    
    # DELETE /api/programmations/{id}
    path('api/programmations/<int:pk>/', views.CinemaProgrammationDeleteAPI.as_view(), name='programmation_delete'),

    # --- AUTH ---
    path('accounts/login/', views.login_view, name='login_view'),
    path('accounts/signup/', views.signup_view, name='signup_view'),
    path('accounts/verify/', views.verify_otp_view, name='verify_otp'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
