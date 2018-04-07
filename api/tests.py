from django.test import Client
from .models import SocialInformation
from django.urls import include, path, reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from .views import SocialInformationViewset, UserViewset
from  rest_framework import serializers, status
from django.utils.translation import ugettext_lazy as _
# Create your tests here.


class UserTests(APITestCase):

    def setUp(self):
        """
        This method will run before any test.
        """

        self.user = User.objects.create(
            username='teste',
            first_name='teste',
            last_name='teste',
            email='teste@teste.com',
            password='teste'
        )
        self.url = '/api/users/'

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.user.delete()

    def test_create_user(self):
        """
        Ensure we can create a user object.
        """
        response = self.client.get(self.url + str(self.user.pk) + '/')
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_invalid_create_user(self):
        """
        Ensure we can't create a invalid user object.
        """
        data = {
        'username':'updated',
        'first_name':'teste',
        'last_name':'teste',
        'email':'erro',
        'password':'teste'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        """
        Ensure we can create a new user object.
        """
        self.assertEqual(self.user.username, 'teste')
        data = {
            'username':'updated',
            'first_name':'teste',
            'last_name':'teste',
            'email':'teste@teste.com',
            'password':'teste'
        }
        response = self.client.put(self.url + str(self.user.pk) + '/', data)


        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_user.username, 'updated')

    def test_invalid_update_user(self):
        """
        Ensure we can't update a user object with invalid fields.
        """
        self.assertEqual(self.user.username, 'teste')
        data = {
            'username':'updated',
            'first_name':'teste',
            'last_name':'teste',
            'email':'erro',
            'password':'teste'
        }
        response = self.client.put(self.url + str(self.user.pk) + '/', data)


        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'email': [_('Enter a valid email address.')]}
        )

    def test_partial_update_user(self):
        """
        Ensure we can partially update a user object.
        """
        self.assertEqual(self.user.email, 'teste@teste.com')
        data = {
            'email':'silverson@teste.com',
        }
        response = self.client.patch(self.url + str(self.user.pk) + '/', data)
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_user.email, 'silverson@teste.com')

    def test_invalid_partial_update_user(self):
        """
        Ensure we can't partially update invalid information on a valid user
        object.
        """
        self.assertEqual(self.user.email, 'teste@teste.com')
        data = {
            'email':'silverson',
        }
        response = self.client.patch(self.url + str(self.user.pk) + '/', data)
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {'email': [_('Enter a valid email address.')]}
        )
