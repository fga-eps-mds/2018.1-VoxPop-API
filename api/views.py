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

    def destroy(self, request, pk=None):
        response = super(SocialInformationViewset, self).destroy(request, pk)
        return response

    def retrieve(self, request, pk=None):
        response = super(SocialInformationViewset, self).retrieve(request, pk)
        return response

    def partial_update(self, request, pk=None, **kwargs):
        response = \
          super(SocialInformationViewset,
                self).partial_update(request, pk, **kwargs)
        return response

    def update(self, request, pk=None, **kwargs):
        response = \
          super(SocialInformationViewset, self).update(request, pk, **kwargs)
        return response


class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    class_name = User
    queryset = User.objects.all()

    def list(self, request):
        return super(UserViewset, self).list(request)

    def create(self, request):
        return super(UserViewset, self).create(request)

    def destroy(self, request, pk=None):
        response = super(UserViewset, self).destroy(request, pk)
        return response

    def retrieve(self, request, pk=None):
        response = super(UserViewset, self).retrieve(request, pk)
        return response

    def partial_update(self, request, pk=None, **kwargs):
        response = \
          super(UserViewset, self).partial_update(request, pk, **kwargs)
        return response

    def update(self, request, pk=None, **kwargs):
        response = \
          super(UserViewset, self).update(request, pk, **kwargs)
        return response
