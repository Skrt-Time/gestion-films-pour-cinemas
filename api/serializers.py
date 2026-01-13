from rest_framework import serializers
from .models import Film, Programmation, Cinema, Review

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'

class ProgrammationSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer(read_only=True)
    
    class Meta:
        model = Programmation
        fields = ['id', 'date_debut', 'date_fin', 'jours', 'heure', 'cinema']

class FilmSerializer(serializers.ModelSerializer):
    programmations = ProgrammationSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Film
        fields = '__all__'

    def get_average_rating(self, obj):
        from django.db.models import Avg
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

class ProgrammationDetailSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer(read_only=True)
    film = FilmSerializer(read_only=True)
    
    class Meta:
        model = Programmation
        fields = '__all__'
