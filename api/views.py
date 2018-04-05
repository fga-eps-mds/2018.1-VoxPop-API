# # from django.shortcuts import render
from .models import SocialInformation
from .serializers import UserSerializer, SocialInformationSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User


class SocialInformationViewset(ModelViewSet):
    serializer_class = SocialInformationSerializer
    class_name = SocialInformation
    queryset = SocialInformation.objects.all()

    def list(self, request):
        return super(SocialInformationViewset, self).list(request)

    def create(self, request):
        return super(SocialInformationViewset, self).create(request)

    def destroy(self, request, id=None):
        response = super(SocialInformationViewset, self).destroy(request, id)
        return response

    def retrieve(self, request, id=None):
        response = super(SocialInformationViewset, self).retrieve(request, id)
        return response


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    class_name = User
    queryset = User.objects.all()

    def list(self, request):
        return super(UserViewset, self).list(request)

    def create(self, request):
        return super(UserViewset, self).create(request)

    def destroy(self, request, id=None):
        response = super(UserViewset, self).destroy(request, id)
        return response

    def retrieve(self, request, id=None):
        response = super(UserViewset, self).retrieve(request, id)
        return response
