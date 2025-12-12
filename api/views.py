from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='login_view')
def owner_dashboard_view(request):
    """ Service 1: Page Propriétaire """
    # UTILISATEUR RÉEL : On utilise request.user
    # Pour l'instant, on garde le filtre cinema_id=1 pour la démo, ou on peut lier au user plus tard.
    # Ici on sécurise juste l'accès.
    from .models import Programmation
    programmations = Programmation.objects.filter(cinema_id=1).select_related('film').order_by('-date_debut')
    return render(request, 'api/owner.html', {'programmations': programmations, 'user': request.user})


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
        # On utilise le serializer de Programmation
        from .serializers import ProgrammationSerializer
        serializer = ProgrammationSerializer(data=request.data)
        if serializer.is_valid():
            # Correction: On passe les IDs directement au save() car ils sont read_only dans le serializer
            serializer.save(cinema_id=cinema_id, film_id=film_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CinemaProgrammationDeleteAPI(APIView):
    """
    DELETE /api/programmations/{id}/
    Supprime une programmation (retire le film de l'affiche du cinéma).
    """
    def delete(self, request, pk):
        from .models import Programmation
        try:
            prog = Programmation.objects.get(pk=pk)
            prog.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Programmation.DoesNotExist:
            return Response({"error": "Programmation introuvable"}, status=status.HTTP_404_NOT_FOUND)

# --- AUTHENTICATION VIEWS ---

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
import random
from django.core.mail import send_mail

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('owner_dashboard')
        else:
            return render(request, 'api/login.html', {'error': 'Identifiants invalides'})
    return render(request, 'api/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email') # TODO: Should check unique email
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check existing
        if User.objects.filter(username=username).exists():
            return render(request, 'api/login.html', {'error': "Ce nom d'utilisateur est déjà pris."})

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Store in session for verification
        request.session['signup_data'] = {
            'username': username,
            'email': email,
            'password': password, # Note: In prod, password should be hashed or handled more securely even in session
            'otp': otp
        }

        # Mock Email Send (Console)
        print(f"--------------------------------------------------")
        print(f"EMAIL SIMULATION - TO: {email}")
        print(f"SUBJECT: Votre code de vérification CinéParis")
        print(f"BODY: Bonjour, votre code est : {otp}")
        print(f"--------------------------------------------------")
        
        # Real send (configured to console backend in settings ideally)
        # send_mail(...) 

        return redirect('verify_otp')
    
    return redirect('login_view')

def verify_otp_view(request):
    signup_data = request.session.get('signup_data')
    if not signup_data:
        return redirect('login_view')
    
    if request.method == 'POST':
        code = request.POST.get('otp_code')
        if code == signup_data['otp']:
            # Success! Create User
            user = User.objects.create_user(
                username=signup_data['username'],
                email=signup_data['email'],
                password=signup_data['password']
            )
            # Login
            login(request, user)
            # Clear session
            del request.session['signup_data']
            return redirect('owner_dashboard')
        else:
            return render(request, 'api/verify_otp.html', {'email': signup_data['email'], 'error': 'Code incorrect'})

    return render(request, 'api/verify_otp.html', {'email': signup_data['email'], 'dev_code': signup_data['otp']})
