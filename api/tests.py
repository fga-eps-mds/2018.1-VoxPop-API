from django.test import TestCase
from .models import SocialInformation
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from .views import SocialInformationViewset, UserViewset
# Create your tests here.


class UserTests(TestCase):

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        user_detail = UserViewset.as_view(actions={'get': 'retrieve'})
        response = user_detail(request, pk=voxpop_user.pk)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        """
        Ensure we can destroy a user object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        user_detail = UserViewset.as_view(actions={'get': 'retrieve'})
        voxpop_user.delete()
        response = user_detail(request, pk=voxpop_user.pk)
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        user_pk = voxpop_user.pk
        voxpop_user = User.objects.update(
                username='teste',
                first_name='teste',
                last_name='silverson',
                email='teste@teste.com',
                password='teste'
        )
        user_detail = UserViewset.as_view(actions={'get': 'retrieve'})
        response = user_detail(request, pk=user_pk)
        self.assertEquals(response.status_code, 200)


class SocialInformationTests(TestCase):
    def test_create_social_information(self):
        """
        Ensure we can create a new social information object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        social_information = SocialInformation.objects.create(
                        owner=voxpop_user,
                        state='AC',
                        city='Rio Branco',
                        income=1200,
                        education='EFC',
                        job='Atoa',
                        birth_date='2018-02-03'
        )
        user_detail = SocialInformationViewset.as_view(actions={'get': 'retrieve'})
        response = user_detail(request, pk=social_information.pk)
        self.assertEqual(response.status_code, 200)

    def test_delete_social_information(self):
        """
        Ensure we can destroy a social information object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        social_information = SocialInformation.objects.create(
                        owner=voxpop_user,
                        state='AC',
                        city='Rio Branco',
                        income=1200,
                        education='EFC',
                        job='Atoa',
                        birth_date='2018-02-03'
        )
        user_detail = SocialInformationViewset.as_view(actions={'get': 'retrieve'})
        response = user_detail(request, pk=social_information.pk)
        social_information.delete()
        response = user_detail(request, pk=social_information.pk)
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """
        Ensure we can update a social information object.
        """
        request = APIRequestFactory().get("")
        voxpop_user = User.objects.create(
                        username='teste',
                        first_name='teste',
                        last_name='teste',
                        email='teste@teste.com',
                        password='teste'
        )
        social_information = SocialInformation.objects.create(
                        owner=voxpop_user,
                        state='AC',
                        city='Rio Branco',
                        income=1200,
                        education='EFC',
                        job='Atoa',
                        birth_date='2018-02-03'
        )
        social_information_pk = social_information.pk
        social_information = SocialInformation.objects.update(
                owner=voxpop_user,
                state='AC',
                city='Rio Branco',
                income=120,
                education='EFC',
                job='Atoa',
                birth_date='2000-02-03'
        )
        user_detail = SocialInformationViewset.as_view(actions={'get': 'retrieve'})
        response = user_detail(request, pk=social_information_pk)
        self.assertEquals(response.status_code, 200)
