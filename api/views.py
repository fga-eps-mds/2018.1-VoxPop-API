# # from django.shortcuts import render
from .models import SocialInformation
from .serializers import (
                            UserSerializer,
                            SocialInformationSerializer,
                        )
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import UserPermissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


class SocialInformationViewset(ModelViewSet):
    """Description: SocialInformationViewset.
    API endpoint that allows social information
     to be viewed, created, deleted or edited.
    """
    # permission_classes = (UserPermissions,)
    serializer_class = SocialInformationSerializer
    class_name = SocialInformation
    queryset = SocialInformation.objects.all()

    def list(self, request):
        """
          API endpoint that allows all social information to be viewed.
          ---
          Response example:
          ```
            [
                {
                    "id": 3,
                    "owner": 1,
                    "federal_unit": "AC",
                    "city": "Rio Branco",
                    "income": "1200.00",
                    "education": "EFC",
                    "job": "Student",
                    "birth_date": "2000-04-06"
                },
                {
                    "id": 4,
                    "owner": 2,
                    "federal_unit": "AC",
                    "city": "Rio Branco",
                    "income": "3400.00",
                    "education": "EFC",
                    "job": "Software Engineer",
                    "birth_date": "1980-04-06"
                }
            ]
          ```
        """
        return super(SocialInformationViewset, self).list(request)

    def create(self, request):
        """
          API endpoint that allows all social information to be created.
          ---
          Body example:
          ```
          {
            "owner": 2,
            "federal_unit": "AC",
            "city": "Rio Branco",
            "income": "3400.00",
            "education": "EFC",
            "job": "Software Engineer",
            "birth_date": "1980-04-06"
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "owner": 2,
            "federal_unit": "AC",
            "city": "Rio Branco",
            "income": "3400.00",
            "education": "EFC",
            "job": "Software Engineer",
            "birth_date": "1980-04-06"
          }
          ```
        """
        return super(SocialInformationViewset, self).create(request)

    def destroy(self, request, pk=None):
        """
        API endpoint that allows social information to be deleted.
        """
        response = super(SocialInformationViewset, self).destroy(request, pk)
        return response

    def retrieve(self, request, pk=None):
        """
        API endpoint that allows a specific social information to be viewed.
        ---
        Response example:
        ```
        {
          "id": 1,
          "owner": 2,
          "federal_unit": "AC",
          "city": "Rio Branco",
          "income": "3400.00",
          "education": "EFC",
          "job": "Software Engineer",
          "birth_date": "1980-04-06"
        }
        ```
        """
        response = super(SocialInformationViewset, self).retrieve(request, pk)
        return response

    def partial_update(self, request, pk=None, **kwargs):
        """
          API endpoint that allows a social information to be partial edited.
          ---
          Body example:
          ```
          {
            "income": "3700.00",
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "owner": 2,
            "federal_unit": "AC",
            "city": "Rio Branco",
            "income": "3700.00",
            "education": "EFC",
            "job": "Software Engineer",
            "birth_date": "1980-04-06"
          }
          ```
        """
        response = super(SocialInformationViewset, self).partial_update(
            request,
            pk,
            **kwargs)
        return response

    def update(self, request, pk=None, **kwargs):
        """
          API endpoint that allows a social information to be edited.
          ---
          Body example:
          ```
          {
            "owner": 2,
            "federal_unit": "GO",
            "city": "Luziânia",
            "income": "3700.00",
            "education": "ESC",
            "job": "Software Engineer",
            "birth_date": "1989-04-06"
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "owner": 2,
            "federal_unit": "GO",
            "city": "Luziânia",
            "income": "3700.00",
            "education": "ESC",
            "job": "Software Engineer",
            "birth_date": "1989-04-06"
          }
          ```
        """
        response = super(SocialInformationViewset, self).update(
            request,
            pk,
            **kwargs)
        return response


class UserViewset(ModelViewSet):
    """Description: UserViewset.
    API endpoint that allows user
     to be viewed, created, deleted or edited.
    """
    permission_classes = (UserPermissions,)
    serializer_class = UserSerializer
    class_name = User
    queryset = User.objects.all()

    def list(self, request):
        """
          API endpoint that allows all user to be viewed.
          ---
          Response example:
          ```
            {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                  "id": 1,
                  "username": "string",
                  "first_name": "string",
                  "last_name": "string",
                  "email": "string@teste.com",
                  "social_information": {
                    "id": 3,
                    "owner": 1,
                    "federal_unit": "AC",
                    "city": "Rio Branco",
                    "income": "1200.00",
                    "education": "EFC",
                    "job": "Student",
                    "birth_date": "2000-04-06"
                  }
                },
                {
                  "id": 2,
                  "username": "test",
                  "first_name": "test",
                  "last_name": "test",
                  "email": "teste@teste.com",
                  "social_information": {
                    "id": 4,
                    "owner": 2,
                    "federal_unit": "AC",
                    "city": "34",
                    "income": "34.00",
                    "education": "EFC",
                    "job": "34",
                    "birth_date": "2018-04-06"
                  }
                },
            ]
        }
        ```
        """
        return super(UserViewset, self).list(request)

    def create(self, request):
        """
          API endpoint that allows all user to be created.
          ---
          Body example:
          ```
          {
            "username": "topperson",
            "first_name": "top",
            "last_name": "silva",
            "email": "teste@teste.com"
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "username": "topperson",
            "first_name": "top",
            "last_name": "silva",
            "email": "teste@teste.com",
            "social_information": null
          }
          ```
        """
        return super(UserViewset, self).create(request)

    def destroy(self, request, pk=None):
        """
        API endpoint that allows user to be deleted.
        """
        response = super(UserViewset, self).destroy(request, pk)
        return response

    def retrieve(self, request, pk=None):
        """
        API endpoint that allows a specific user to be viewed.
        ---
        Response example:
        ```
        {
          "id": 1,
          "username": "string",
          "first_name": "string",
          "last_name": "string",
          "email": "string@trs.com",
          "social_information": {
            "id": 4,
            "owner": 2,
            "federal_unit": "AC",
            "city": "34",
            "income": "34.00",
            "education": "EFC",
            "job": "34",
            "birth_date": "2018-04-06"
          }
        }
        ```
        """
        response = super(UserViewset, self).retrieve(request, pk)
        return response

    def partial_update(self, request, pk=None, **kwargs):
        """
          API endpoint that allows a user to be partial edited.
          ---
          Body example:
          ```
          {
            "username": "vrum vrum",
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "username": "vrum vrum",
            "first_name": "string",
            "last_name": "string",
            "email": "string@trs.com",
            "social_information": {
              "id": 4,
              "owner": 2,
              "federal_unit": "AC",
              "city": "34",
              "income": "34.00",
              "education": "EFC",
              "job": "34",
              "birth_date": "2018-04-06"
            }
          }
          ```
        """
        response = super(UserViewset, self).partial_update(
            request,
            pk,
            **kwargs)
        return response

    def update(self, request, pk=None, **kwargs):
        """
          API endpoint that allows a social information to be edited.
          ---
          Body example:
          ```
          {
            "username": "vrum vrum",
            "first_name": "andre",
            "last_name": "string",
            "email": "string@trs.com"
          }
          ```
          Response example:
          ```
          {
            "id": 1,
            "username": "vrum vrum",
            "first_name": "andre",
            "last_name": "string",
            "email": "string@trs.com",
            "social_information": {
              "id": 4,
              "owner": 2,
              "federal_unit": "AC",
              "city": "34",
              "income": "34.00",
              "education": "EFC",
              "job": "34",
              "birth_date": "2018-04-06"
            }
          }
          ```
        """
        response = super(UserViewset, self).update(
            request,
            pk,
            **kwargs)
        return response
