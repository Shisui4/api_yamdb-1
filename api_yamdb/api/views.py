from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .serializers import ReviewSerializer
from reviews.models import Title


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

