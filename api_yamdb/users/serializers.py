from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(

    )
    username = serializers.CharField

    def validate_email(self, value):
        pass

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Выберите другое имя")
        return value


class UserSerializer(serializers.ModelSerializer):
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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Выберите другое имя")
        return value
