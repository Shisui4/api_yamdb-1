from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ReviewViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register(
     r'titles/(?P<title_id>\d+)/reviews',
     ReviewViewSet, basename='review'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]



