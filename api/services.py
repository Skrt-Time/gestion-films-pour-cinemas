from . import dao
from django.core.exceptions import ValidationError

"""
COUCHE SERVICE
Responsabilité : Contient toute la logique métier et les règles de gestion.
Exemple : Vérifier que la date de fin est après la date de début.
C'est ici qu'on appelle le DAO.
"""

# Exemple :
# def create_projection(data):
#     if data['start_date'] > data['end_date']:
#         raise ValidationError("Erreur de dates")
#     return dao.create_projection(data)