import uuid

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reviews.models import User
from .serializers import SignUpSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def create(self, validated_data):
        email = validated_data['email']
        confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
        user = User.objects.create(**validated_data, confirmation_code=confirmation_code)
        return user


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid:
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, status = User.objects.get_or_create(**serializer.validated_data)
        send_mail(message=user.confirmation_code, recipient_list=[email])           
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

