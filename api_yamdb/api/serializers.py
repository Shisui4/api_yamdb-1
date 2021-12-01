from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, User, Comment

NOT_ALLOWED = 'Отзыв уже оставлен.'
FORBIDDEN_NAME = 'Это имя не может быть использовано!'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(FORBIDDEN_NAME)
        return name 

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    title = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = '__all__'

        def validate(self, data):
            if self.context['request'].method == 'POST':
                user = self.context['request'].user
                title_id = self.context['view'].kwargs.get('title.id')
                if Review.objects.filter(author=user, title_id=title_id):
                    raise serializers.ValidationError(NOT_ALLOWED)
            return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
