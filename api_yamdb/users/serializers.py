from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


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
            raise serializers.ValidationError("Choose another name")
        return value
