from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken


from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .permissions import Admin, Superuser
from .serializers import UserSerializer, UserSelfSerializer
from .services import generate_token, check_token

User = get_user_model()


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        username = request.data['username']
        email = request.data['email']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = serializer.save()
        token = generate_token(user)
        send_mail(
            'Yamdb confirmation code',
            f'{token}',
            'auth@yamdb.com',
            [f'{email}']
        )

        return Response(
            {
                "username": username,
                "email": email
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def retrieve_token(request):
    if (
        'username' in request.data
        and 'confirmation_code' in request.data
    ):
        user = get_object_or_404(User, username=request.data['username'])
        if check_token(user, request.data['confirmation_code']):
            access = AccessToken.for_user(user)
            return Response(
                {
                        'token': str(access)
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [Admin | Superuser]
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer_class = UserSelfSerializer

        if request.method == 'GET':
            serializer = serializer_class(user)
            return Response(serializer.data)

        serializer = serializer_class(
                user,
                partial=True,
                data=request.data
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
