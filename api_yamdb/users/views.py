from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .permissions import Admin
from .serializers import UserSerializer
from .services import generate_confirmation_code

User = get_user_model()


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = generate_confirmation_code()
        serializer.save(confirmation_code=confirmation_code)
        send_mail(
            'Yamdb confirmation code',
            f'{confirmation_code}',
            'auth@yamdb.com',
            [f'{serializer.data["email"]}']
        )
        return Response(
            {
                "username": serializer.data['username'],
                "email": serializer.data['email']
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors)


@api_view(['POST'])
def retrieve_token(request):
    pass


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (Admin,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = User.objects.get(user=request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
