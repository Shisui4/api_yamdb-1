import uuid

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from reviews.models import Categories, Genre, Title, Review, User
from .serializers import CommentSerializer, GenreSerializer, CategoriesSerializer
from .serializers import ReviewSerializer, SignUpSerializer, UserSerializer


from_email = 'from@yamdb.com'
subject = 'confirmation code'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


    @action(methods=['get', 'patch'], detail=True, url_path='me')
    def set_profile(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
    send_mail(
        subject=subject,
        message=confirmation_code,
        from_email=from_email,
        recipient_list=[email])
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(author=user, review=review)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)