from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import services
from .serializers import FilmSerializer

# --- VUES HTML (Frontend) ---

def public_search_view(request):
    """ Service 2: Page publique de recherche """
    return render(request, 'api/index.html')

def movie_details_view(request, film_id):
    """ Service 3: Page de détails """
    return render(request, 'api/details.html', {'film_id': film_id})

def owner_dashboard_view(request):
    """ Service 1: Page Propriétaire """
    return render(request, 'api/owner.html')


# --- VUES API REST (Controller) ---

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
    Permet à un cinéma d'ajouter un film (Concept: Le film est créé dans la base globale).
    Permissions: Un cinéma ne devrait créer que "ses" films, mais un film est global.
    Interprétation: Le cinéma propose un film. S'il n'existe pas, il le crée.
    """
    def post(self, request, cinema_id):
        # Vérification simple permission (Mock)
        # if request.user.cinema_id != cinema_id: return 403
        
        # On crée le film sans le lier immédiatement au cinéma (car lien via Programmation)
        # Mais l'endpoint est contextuel.
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            film = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CinemaProgrammationCreateAPI(APIView):
    """
    POST /api/cinemas/{id}/films/{filmId}/programmations
    Ajoute une programmation pour un film donné dans ce cinéma.
    """
    def post(self, request, cinema_id, film_id):
        # On injecte les IDs dans les données pour la création
        data = request.data.copy()
        data['cinema'] = cinema_id
        data['film'] = film_id
        
        # On utilise le serializer de Programmation
        from .serializers import ProgrammationSerializer
        serializer = ProgrammationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
