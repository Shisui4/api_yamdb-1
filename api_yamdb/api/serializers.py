from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Это имя не может быть использовано!')
        return name 