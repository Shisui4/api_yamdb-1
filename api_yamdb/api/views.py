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

from_email = 'from@yamdb.com'
subject = 'confirmation code'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


"""@api_view(['POST'])
def sign_up(request):
    serializer =SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
"""
@api_view(['POST'])
def sign_up(request):
    serializer =SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user, status = User.objects.get_or_create(**validated_data)
    if status and user.confirmation_code == True:
        raise  
    if not User.objects.filter(email=email).exists():
        user = User.objects.create(**validated_data, confirmation_code=True)   
    confirmation_code = str(uuid.uuid3(uuid.NAMESPACE_X500, email))
    send_mail(
        subject=subject,
        message=confirmation_code,
        from_email=from_email,
        recipient_list=[email])
    return Response(serializer.data, status=status.HTTP_200_OK)


