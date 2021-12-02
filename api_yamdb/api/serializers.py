import uuid

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, User


FORBIDDEN_NAME = 'Это имя не может быть использовано!'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(FORBIDDEN_NAME)
        return name 


class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации и создания нового пользователя."""
    
    class Meta:
        fields = ('email', 'username')
        model = User

    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
        User.objects.create(username=username, email=email, confirmation_code=confirmation_code)
        #send_email(from=email, message=confirmation_code)           

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    author = SlugRelatedField(
        default = serializers.CurrentUserDefault(),
        read_only = True,
        slug_field = 'username'
    )
    title = SlugRelatedField(
        read_only = True,
        slug_field = 'name'
    )

    class Meta:
        model = Review
        fields = '__all__'

        def validate(self, data):
            if self.context['request'].method == 'POST':
                user = self.context['request'].user
                title_id = self.context['view'].kwargs.get('title.id')
                if Review.objects.filter(author=user, title_id=title_id):
                    raise serializers.ValidationError('Отзыв уже оставлен')
            return data



