import datetime
from django.test import Client
from django.contrib.auth.models import User
from .models import SocialInformation, ContactUs
from django.urls import include, path, reverse
from rest_framework.test import APIRequestFactory, APITestCase
from .views import SocialInformationViewset, UserViewset, ContactUsViewset
from  rest_framework import serializers, status
from django.utils.translation import ugettext_lazy as _
# Create your tests here.


class UserTests(APITestCase):

    def setUp(self):
        """
        This method will run before any test.
        """
        self.superuser = User.objects.create_superuser(
            username='flyer user',
            email='flye@user.com',
            password='idontneedthisshit'
        )
        self.user = User.objects.create(
            username='teste',
            first_name='teste',
            last_name='teste',
            email='teste@teste.com',
            password='teste'
        )
        self.social_information = SocialInformation.objects.create(
            owner=self.user
        )
        self.url = '/api/users/'
        # self.client.force_login(self.user)
        self.client.force_authenticate(self.superuser)

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.user.delete()
        self.social_information.delete()

    def test_create_user(self):
        """
        Ensure we can create a user object.
        """
        response = self.client.get(self.url + str(self.user.pk) + '/')
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
        self.client.force_authenticate(self.user)
        self.assertEqual(self.user.username, 'teste')
        data = {
            'username':'teste',
            'first_name':'updated',
            'last_name':'teste',
            'email':'teste@teste.com',
            'password':'teste'
        }
        response = self.client.put(self.url + str(self.user.pk) + '/', data)
        new_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_user.first_name, data['first_name'])

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
        self.client.force_authenticate(self.user)
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

class SocialInformationTests(APITestCase):

    def setUp(self):
        """
        This method will run before any test.
        """
        self.superuser = User.objects.create_superuser(
            username='flyer user',
            email='flye@user.com',
            password='idontneedthisshit'
        )
        self.user = User.objects.create(
            username='teste',
            first_name='teste',
            last_name='teste',
            email='teste@teste.com',
            password='teste'
        )
        self.social = SocialInformation.objects.create(owner=self.user)
        self.url = '/api/social_informations/'
        self.client.force_authenticate(self.superuser)

    def tearDown(self):
        """
        This method will run after any test.
        """
        self.user.delete()

    def test_create_social(self):
        """
        Ensure we can create a social information object.
        """
        response = self.client.get(self.url + str(self.social.pk) + '/')
        new_social = SocialInformation.objects.get(pk=self.social.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_invalid_create_social(self):
        """
        Ensure we can't create a social information object because
        SocialInformationViewset doesn't have a create method.
        """
        data = {
            "owner": self.user,
            "region": "",
            "income": "",
            "education": "",
            "race": "",
            "gender": "",
            "birth_date": ""
        }
        response = None

        try:
            response = self.client.post(self.url, data)
        except AttributeError:
            pass

        self.assertIsNone(response)

    def test_update_social(self):
        """
        Ensure we can update a new social information object.
        """
        self.assertEqual(self.social.region, None)
        data = {
            "owner": self.user.pk,
            "region": "N",
            "income": "",
            "education": "",
            "race": "",
            "gender": "",
            "birth_date": ""
        }
        response = self.client.put(self.url + str(self.social.pk) + '/', data)

        new_social = SocialInformation.objects.get(pk=self.social.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_social.region, 'N')

    def test_invalid_update_social(self):
        """
        Ensure we can't update a social object with invalid fields.
        """
        self.assertEqual(self.social.birth_date, None)
        data = {
            "owner": self.user.pk,
            "region": "",
            "income": "",
            "education": "",
            "race": "",
            "gender": "",
            "birth_date": "20180-43-213"
        }
        response = self.client.put(self.url + str(self.social.pk) + '/', data)

        new_social = SocialInformation.objects.get(pk=self.social.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {"birth_date": [
                "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."
            ]}
        )

    def test_partial_update_social(self):
        """
        Ensure we can partially update a social object.
        """
        self.assertEqual(self.social.region, None)
        data = {
            'region': 'N',
        }
        response = self.client.patch(self.url + str(self.social.pk) + '/', data)
        new_social = SocialInformation.objects.get(pk=self.social.pk)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(new_social.region, 'N')

    def test_invalid_partial_update_social(self):
        """
        Ensure we can't partially update invalid information on a valid social
        object.
        """
        self.assertEqual(self.social.region, None)
        data = {
            'birth_date': '20180-56-89',
        }
        response = self.client.patch(self.url + str(self.social.pk) + '/', data)
        new_social = SocialInformation.objects.get(pk=self.social.pk)
        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data,
            {"birth_date": [
                "Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]]."
            ]}
        )
