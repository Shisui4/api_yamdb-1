from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import sign_up, get_token, CommentViewSet, ReviewViewSet, UserViewSet
from .views import CategoriesViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
#router.register('titles', GenreViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router.register(
     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
     CommentViewSet, basename='comment'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token,  name='token'),
]