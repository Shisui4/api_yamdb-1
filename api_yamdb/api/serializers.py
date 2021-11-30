from django.db.models import fields
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review


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




# Другой способ доступа к идентификатору объекта-это доступ к kwargs view объекту из context словаря сериализатора.
# my_view = self.context['view'] # get the 'view' object from serializer context
# object_id = my_view.kwargs.get('pk') # access the 'view' kwargs and lookup for 'pk'