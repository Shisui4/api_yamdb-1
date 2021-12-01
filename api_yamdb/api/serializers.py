from rest_framework import serializers

from reviews.models import User, Categories, Genre, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(
                'Это имя не может быть использовано!')
        return name


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleViewSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'release', 'description',
                  'genre', 'category')
        meta = Title


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
