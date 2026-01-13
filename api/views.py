from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from .serializers import FilmSerializer

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# --- VUES HTML (Frontend) ---

def login_view(request):
    """ Page de connexion """
    from django.contrib.auth.forms import AuthenticationForm
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('owner_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'api/login.html', {'form': form})

def logout_view(request):
    """ Déconnexion """
    logout(request)
    return redirect('home')

def signup_view(request):
    """ Page d'inscription """
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth import login
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Connexion automatique après inscription
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'api/signup.html', {'form': form})

def public_search_view(request):
    """ Service 2: Page publique de recherche """
    return render(request, 'api/index.html')

def movie_details_view(request, film_id):
    """ Service 3: Page de détails """
    is_favorite = False
    if request.user.is_authenticated:
        from .models import Favorite, Film
        # On check si le favori existe
        is_favorite = Favorite.objects.filter(user=request.user, film_id=film_id).exists()
    return render(request, 'api/details.html', {'film_id': film_id, 'is_favorite': is_favorite})

@login_required(login_url='login')
def owner_dashboard_view(request):
    """ Service 1: Page Propriétaire """
    if not request.user.is_staff:
        # Rediriger les non-admins vers l'accueil ou afficher une erreur
        return redirect('home')

    from .models import Cinema
    cinemas = Cinema.objects.all()
    return render(request, 'api/owner.html', {'cinemas': cinemas})

@login_required(login_url='login')
def favorites_view(request):
    """ Page des favoris de l'utilisateur """
    # Récupérer les favoris de l'user courant
    # On optimise en chargeant 'film' et 'film__programmations__cinema' pour éviter N+1 requêtes
    favorites = request.user.favorites.select_related('film').all()
    return render(request, 'api/favorites.html', {'favorites': favorites})

class ToggleFavoriteAPI(APIView):
    """
    POST /api/favorites/toggle/
    Ajoute ou retire un film des favoris.
    Body: { "film_id": 123 }
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Connexion requise"}, status=status.HTTP_401_UNAUTHORIZED)
            
        film_id = request.data.get('film_id')
        from .models import Film, Favorite
        from django.shortcuts import get_object_or_404
        
        film = get_object_or_404(Film, pk=film_id)
        
        fav = Favorite.objects.filter(user=request.user, film=film).first()
        if fav:
            fav.delete()
            return Response({"status": "removed"})
        else:
            Favorite.objects.create(user=request.user, film=film)
            return Response({"status": "added"})

class ReviewCreateAPI(APIView):
    """
    POST /api/reviews/
    Ajoute un avis pour un film.
    Body: { "film_id": 123, "rating": 5, "comment": "Top !" }
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Connexion requise"}, status=status.HTTP_401_UNAUTHORIZED)
            
        data = request.data
        film_id = data.get('film_id')
        from .models import Film, Review
        from .serializers import ReviewSerializer
        from django.shortcuts import get_object_or_404
        
        film = get_object_or_404(Film, pk=film_id)
        
        # Vérifier si l'avis existe déjà
        existing_review = Review.objects.filter(user=request.user, film=film).first()
        if existing_review:
            # Update
            serializer = ReviewSerializer(existing_review, data=data, partial=True)
        else:
            # Create
            serializer = ReviewSerializer(data=data)
            
        if serializer.is_valid():
            if not existing_review:
                serializer.save(user=request.user, film=film)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- VUES API REST (Controller) ---

class ReviewModerateAPI(APIView):
    """
    POST /api/reviews/{id}/moderate/
    Permet à un admin de supprimer le texte d'un avis (mais garder la note).
    """
    def post(self, request, pk):
        if not request.user.is_staff: # Admin ou Staff seulement
            return Response({"error": "Non autorisé"}, status=status.HTTP_403_FORBIDDEN)
            
        from .models import Review
        from django.shortcuts import get_object_or_404
        
        review = get_object_or_404(Review, pk=pk)
        review.comment = "[Modéré par l'administrateur]" # On remplace le commentaire
        review.save()
        
        return Response({"status": "moderated"})

# --- VUES API REST (Personne 2) ---

class PublicFilmListAPI(APIView):
    """
    GET /api/public/films/?ville=Paris
    Affiche tous les films proposés dans une ville donnée (ou tous si pas de filtre).
    """
    def get(self, request):
        city = request.query_params.get('ville')
        films = services.list_movies_service(city_filter=city)
        # Note: On utilise le serializer de film qui inclut les programmations
        # Mais pour la liste, peut-être voudrait-on une version allégée.
        # Ici on garde le standard.
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)

class PublicFilmDetailAPI(APIView):
    """
    GET /api/public/films/{id}
    Affiche les détails d'un film.
    """
    def get(self, request, pk):
        film = services.get_movie_details_service(pk)
        if film:
            serializer = FilmSerializer(film)
            return Response(serializer.data)
        return Response({"error": "Film introuvable"}, status=status.HTTP_404_NOT_FOUND)

class CinemaFilmCreateAPI(APIView):
    """
    POST /api/cinemas/{id}/films
    Permet à un cinéma d'ajouter un film.
    AVEC DÉDOUBLONNAGE : Si le film existe déjà (même titre), on le réutilise.
    """
    def post(self, request, cinema_id):
        from .models import Film
        
        data = request.data
        titre = data.get('titre')
        # On peut imaginer qu'un même film a plusieurs versions (VF, VO)
        # Mais pour simplifier, on dédoublonne par titre UNIQUEMENT comme avant ?
        # Non, si on a "Avatar" en VF et "Avatar" en VO, ce sont deux entrées différentes logiquement pour l'affichage ?
        # Le cahier des charges dit "Langue". 
        # Si on considère que c'est le même film (entité) mais projeté différemment, la langue devrait être dans la Programmation et non le Film.
        # MAIS le cahier des charges met "Langue" dans les détails du film (Service 1).
        # Donc "Avatar (VF)" et "Avatar (VO)" sont deux objets Films différents ou le même avec un champ langue ?
        # Si c'est dans Film, alors (Titre + Langue) = Clé unique.
        
        langue = data.get('langue', 'Français')
        existing_film = Film.objects.filter(titre__iexact=titre, langue__iexact=langue).first()
        
        if existing_film:
            # On met à jour les infos si nécessaire ou on renvoie juste l'existant
            # Ici on renvoie l'existant pour qu'il soit utilisé par la programmation
            serializer = FilmSerializer(existing_film)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Création nouveau film
            serializer = FilmSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CinemaProgrammationCreateAPI(APIView):
    """
    POST /api/cinemas/{id}/films/{filmId}/programmations
    Ajoute une programmation pour un film donné dans ce cinéma.
    """
    def post(self, request, cinema_id, film_id):
        from django.shortcuts import get_object_or_404
        from .models import Cinema, Film
        from .serializers import ProgrammationSerializer

        # Récupération des objets liés pour éviter les erreurs d'intégrité
        cinema = get_object_or_404(Cinema, pk=cinema_id)
        film = get_object_or_404(Film, pk=film_id)
        
        serializer = ProgrammationSerializer(data=request.data)
        if serializer.is_valid():
            # On injecte manuellement les instances Cinema et Film lors de la sauvegarde
            serializer.save(cinema=cinema, film=film)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CinemaProgrammationListAPI(APIView):
    """
    GET /api/cinemas/{id}/programmations/
    Liste toutes les programmations actives pour un cinéma donné.
    """
    def get(self, request, cinema_id):
        from .models import Programmation
        from .serializers import ProgrammationDetailSerializer
        
        # On peut filtrer par date >= aujourd'hui si on veut
        progs = Programmation.objects.filter(cinema_id=cinema_id).order_by('-date_debut')
        
        serializer = ProgrammationDetailSerializer(progs, many=True)
        return Response(serializer.data)

class ProgrammationRetrieveUpdateDestroyAPI(APIView):
    """
    GET, PUT, DELETE /api/programmations/{pk}/
    Gère une programmation spécifique.
    """
    def get_object(self, pk):
        from django.shortcuts import get_object_or_404
        from .models import Programmation
        return get_object_or_404(Programmation, pk=pk)

    def delete(self, request, pk):
        prog = self.get_object(pk)
        film = prog.film # On garde une référence au film avant de supprimer la séance
        prog.delete()
        
        # NETTOYAGE INTELLIGENT : Si le film n'a plus aucune séance, on le supprime aussi
        # pour éviter les "fantômes" sur la page d'accueil.
        if film.programmations.count() == 0:
            film.delete()
            
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        prog = self.get_object(pk)
        from .serializers import ProgrammationSerializer
        # On utilise le serializer ne créant pas de film, juste update de la prog
        # Mais si l'utilisateur veut update le film lié ?
        # Pour l'instant on se concentre sur la séance (date, heure)
        serializer = ProgrammationSerializer(prog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilmRetrieveUpdateDestroyAPI(APIView):
    """
    PUT /api/films/{pk}/
    Permet de mettre à jour les infos du film (Titre, Image, etc.)
    """
    def put(self, request, pk):
        from .models import Film
        from django.shortcuts import get_object_or_404
        film = get_object_or_404(Film, pk=pk)
        
        serializer = FilmSerializer(film, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
