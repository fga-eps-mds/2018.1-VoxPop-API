from .models import SocialInformation
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }


class SocialInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialInformation
        fields = [
            'id',
            'owner',
            'state',
            'city',
            'income',
            'education',
            'job',
            'birth_date',
        ]
