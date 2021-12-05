import uuid
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User
import datetime as dt

NOT_ALLOWED = 'Отзыв уже оставлен.'
FORBIDDEN_NAME = 'Это имя не может быть использовано!'
MISSING_EMAIL = 'Для авторизации требуется ввести электронную почту'
MISSING_USERNAME = 'Для аутентификации требуется ввести имя пользователя'
MISSING_CODE = 'Для аутентификации требуется ввести код подтверждения'
from_email = 'from@yamdb.com'
subject = 'confirmation code'


class UserSerializer(serializers.ModelSerializer):
    #role = serializers.CharField(read_only=True, default='user')
   
    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User
        lookup_field = 'username'

    def create(self, validated_data):
        email = validated_data['email']
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
        user = User.objects.create(**validated_data, confirmation_code=confirmation_code)
        return user

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(FORBIDDEN_NAME)
        elif name is None or name == "":
            raise serializers.ValidationError(MISSING_USERNAME)
        return name

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError(MISSING_EMAIL)
        return email


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError(MISSING_USERNAME)
        if confirmation_code is None:
            raise serializers.ValidationError(MISSING_CODE)
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    #rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            TitleGenre.objects.create(
                title=title, genre=genre)
        return title 

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Год не может быть больше текущего')
        return value

    def validate_genre(self, value):
        genre = Genre.objects.all()
        if value not in genre:
            raise serializers.ValidationError(
                'Выбраный жанр не входит в представленный список')
        return value

    def validate_category(self, value):
        category = Category.objects.all()
        if value not in category:
            raise serializers.ValidationError(
                'Выбранная категория не входит в представленный список')
        return value

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
   class CurrentTitleDafault:
        requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.HiddenField(default=CurrentTitleDafault())
    # title = serializers.SlugRelatedField(
    #     slug_field='id',
    #     required=False,
    #     queryset=Titles.objects.all()
    # )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
      
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
   
    class Meta:
        model = Review
        fields = '__all__'

        def validate(self, data):
            if self.context['request'].method == 'POST':
                user = self.context['request'].user
                title_id = self.context['view'].kwargs.get('title_id')
                if Review.objects.filter(author=user, title_id=title_id).exists():
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
