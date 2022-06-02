from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .permissions import Admin
from .serializers import UserSerializer

User = get_user_model()


@api_view(['POST'])
def sign_up(request):
    pass


@api_view(['POST'])
def retrieve_token(request):
    pass


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (Admin,)

    @action(methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(user=request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
