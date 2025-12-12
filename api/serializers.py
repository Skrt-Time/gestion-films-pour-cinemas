from rest_framework import serializers
from .models import Film, Programmation, Cinema

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
    
    class Meta:
        model = Film
        fields = '__all__'
