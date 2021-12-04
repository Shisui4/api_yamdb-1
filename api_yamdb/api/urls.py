from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import sign_up, get_token, ReviewViewSet, TitleViewSet, UserViewSet
from .views import CategoriesViewSet, CommentViewSet, GenreViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoriesViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]