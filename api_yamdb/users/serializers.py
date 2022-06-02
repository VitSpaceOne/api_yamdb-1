from django.contrib.auth import get_user_model


User = get_user_model()


class UserSerializer:

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
