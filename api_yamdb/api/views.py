import uuid

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Categories, Genre, Title, Review, User
from .permissions import IsAdmin, IsSelf, IsAdminOrReadOnly, IsModerator
from .serializers import CommentSerializer, GenreSerializer, CategoriesSerializer
from .serializers import AuthenticationSerializer, ReviewSerializer, UserSerializer
from .serializers import TitleSerializer


from_email = 'from@yamdb.com'
subject = 'confirmation code'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if self.action == 'set_profile':
            return (IsSelf(),)
        return super().get_permissions()

    @action(methods=['get','patch'], detail=False, url_path='me')
    def set_profile(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user)
        if request.method == 'PATCH':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user.set_profile(**serializer.validated_data)
                user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    user, created = User.objects.get_or_create(**serializer.validated_data)
    if not created:
        user.confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
        user.save()
    send_mail(
        subject=subject,
        message=user.confirmation_code,
        from_email=from_email,
        recipient_list=[email])

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = AuthenticationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = User.objects.filter(
        username=serializer.validated_data['username'],
        confirmation_code=serializer.validated_data['confirmation_code']
    ).first()
    if not user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    return Response({'token': token}, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModerator,)

    def get_queryset(self):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = int(self.kwargs.get('title_id'))
        title = get_object_or_404(Title, id=title_id)
        user = self.request.user
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModerator,)

    def get_queryset(self):
        review_id = int(self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = int(self.kwargs.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        user = self.request.user
        serializer.save(author=user, review=review)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)