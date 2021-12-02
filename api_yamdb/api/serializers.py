import uuid

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, User

NOT_ALLOWED = 'Отзыв уже оставлен.'
FORBIDDEN_NAME = 'Это имя не может быть использовано!'
from_email = 'from@yamdb.com'
subject = 'confirmation code'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(FORBIDDEN_NAME)
        return name 


'''class SignUpSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации и создания нового пользователя."""
    
    class Meta:
        fields = ('email', 'username')
        model = User

    def create(self, validated_data):
        email = validated_data['email']
        user, status = User.objects.get_or_create(**validated_data)   
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
        send_mail(
            subject=subject,
            message=confirmation_code,
            from_email=from_email,
            recipient_list=[email])
        return user'''

class SignUpSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)


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
                    raise serializers.ValidationError(NOT_ALLOWED)
            return data



