import json
from base64 import b64encode

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Parliamentary, Proposition, SocialInformation, UserVote
from .permissions import SocialInformationPermissions, UserPermissions
from .serializers import (
    ParliamentarySerializer, PropositionSerializer,
    SocialInformationSerializer, UserSerializer, UserVoteSerializer
)
from .utils import propositions_filter


class SocialInformationViewset(mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    """Description: SocialInformationViewset.
    API endpoint that allows social information
     to be viewed, created, deleted or edited.
    """
    permission_classes = (SocialInformationPermissions,)
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


class UserViewset(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
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
        response = super(UserViewset, self).create(request)

        user = User.objects.get(username=request.data['username'])

        try:
            social_information_data = request.data['social_information']
        except KeyError:
            social_information_data = {}

        social_information_data['owner'] = user

        social_information = \
            SocialInformation.objects.create(**social_information_data)
        social_information.save()

        social_information_serializer = \
            SocialInformationSerializer(social_information)

        response.data['social_information'] = \
            social_information_serializer.data

        return response

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


class LoaderViewSet(ViewSet):
    """
    A viewset that provides VoxPopLoader actions
    """

    @classmethod
    def __get_credentials(cls):
        with open('.loader_credentials.json', 'r') as f:
            read_data = f.read()

        read_data = json.loads(read_data)
        username = read_data['username']
        password = read_data['password']

        utf_8_authorization = "{username}:{password}".format(
            username=username, password=password
        ).encode()

        return "Basic " + b64encode(utf_8_authorization).decode("ascii")

    @list_route(methods=['get'])
    def get_parliamentarians(self, request):
        if request.query_params.get('key') == \
                LoaderViewSet.__get_credentials():
            parliamentary_ids = []
            for parliamentary in Parliamentary.objects.all():
                parliamentary_ids.append(parliamentary.parliamentary_id)

            response = Response(parliamentary_ids, status=status.HTTP_200_OK)

        else:
            response = Response(
                {'status': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response

    @list_route(methods=['post'])
    def create_parliamentary(self, request):
        if request.query_params.get('key') == \
                LoaderViewSet.__get_credentials():
            parliamentary_dict = request.data.dict()
            Parliamentary.objects.create(**parliamentary_dict)

            response = Response({"status": "OK"}, status=status.HTTP_200_OK)

        else:
            response = Response(
                {'status': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response

    @list_route(methods=['get'])
    def get_propositions(self, request):
        if request.query_params.get('key') == \
                LoaderViewSet.__get_credentials():
            native_ids = []
            for proposition in Proposition.objects.all():
                native_ids.append(proposition.native_id)

            response = Response(native_ids, status=status.HTTP_200_OK)

        else:
            response = Response(
                {'status': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response

    @list_route(methods=['post'])
    def create_proposition(self, request):
        if request.query_params.get('key') == \
                LoaderViewSet.__get_credentials():
            proposition_dict = request.data.dict()
            Proposition.objects.create(**proposition_dict)

            response = Response({"status": "OK"}, status=status.HTTP_200_OK)

        else:
            response = Response(
                {'status': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response


class ParliamentaryViewset(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = ParliamentarySerializer
    queryset = Parliamentary.objects.all()


class PropositionViewset(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = PropositionSerializer
    queryset = Proposition.objects.all().order_by('-year')

    def get_queryset(self):
        return propositions_filter(self)

    @list_route(methods=['get'])
    def non_voted(self, request):
        user = request.user
        proposition_voted = []

        try:
            for vote in user.votes.all():
                proposition_voted.append(vote.proposition)

            all_propositions = Proposition.objects.all().order_by('-year')

            response = Response(
                {'status': 'No Content'},
                status=status.HTTP_204_NO_CONTENT
            )

            for proposition in all_propositions:
                if proposition not in proposition_voted:
                    proposition_serialized = PropositionSerializer(proposition)
                    response = Response(
                        proposition_serialized.data,
                        status=status.HTTP_200_OK
                    )
                    break

        except AttributeError:
            return Response(
                {'status': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response


class UserVoteViewset(viewsets.ModelViewSet):

    serializer_class = UserVoteSerializer
    queryset = UserVote.objects.all()

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            user = self.request.user
            queryset = UserVote.objects.filter(user=user)
        else:
            queryset = UserVote.objects.none()

        return queryset

    def list(self, request):
        response = super(UserVoteViewset, self).list(request)

        for vote in response.data['results']:
            proposition = Proposition.objects.get(pk=vote['proposition'])
            proposition_serializer = PropositionSerializer(proposition)
            vote['proposition'] = proposition_serializer.data

        return response

    def create(self, request):
        user_id = request.user.id
        request.data['user'] = user_id

        response = super(UserVoteViewset, self).create(request)

        proposition = Proposition.objects.get(pk=response.data['proposition'])
        proposition_serializer = PropositionSerializer(proposition)
        response.data['proposition'] = proposition_serializer.data

        return response

    def destroy(self, request, pk=None):
        response = super(UserVoteViewset, self).destroy(request, pk)
        return response

    def retrieve(self, request, pk=None):
        response = super(UserVoteViewset, self).retrieve(request, pk)

        proposition = Proposition.objects.get(pk=response.data['proposition'])
        proposition_serializer = PropositionSerializer(proposition)
        response.data['proposition'] = proposition_serializer.data

        return response

    def partial_update(self, request, pk=None, **kwargs):
        user_id = request.user.id
        request.data['user'] = user_id

        response = super(UserVoteViewset, self).partial_update(
            request,
            pk,
            **kwargs)
        return response

    def update(self, request, pk=None, **kwargs):
        user_id = request.user.id
        request.data['user'] = user_id

        response = super(UserVoteViewset, self).update(
            request,
            pk,
            **kwargs)

        proposition = Proposition.objects.get(pk=response.data['proposition'])
        proposition_serializer = PropositionSerializer(proposition)
        response.data['proposition'] = proposition_serializer.data

        return response


class CustomObtainToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = \
            super(CustomObtainToken, self).post(request, *args, **kwargs)

        user = User.objects.get(username=request.data['username'])
        response.data['id'] = user.id
        response.data['username'] = user.username
        response.data['first_name'] = user.first_name
        response.data['last_name'] = user.last_name

        return response
