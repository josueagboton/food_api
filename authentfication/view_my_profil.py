from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def my_profil(request):
    if request.method == 'GET':
        user = request.user
        # Maintenant, vous pouvez utiliser les attributs de l'utilisateur, par exemple :
        username = user.username
        email = user.email
        # Autres attributs selon votre modèle User personnalisé
        # ...
        return Response({'user': user})
