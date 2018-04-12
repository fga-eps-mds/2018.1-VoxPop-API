from .models import SocialInformation
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import models


class SocialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialInformation
        fields = [
            'id',
            'owner',
            'federal_unit',
            'city',
            'income',
            'education',
            'job',
            'birth_date',
        ]


class UserSerializer(serializers.ModelSerializer):
    social_information = SocialInformationSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'social_information',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }


class UserLoginSerializer(serializers.ModelSerializer):
    username = models.CharField()
    email = models.EmailField()
    token = models.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }
