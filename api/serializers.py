from .models import Parliamentary, Proposition, SocialInformation, UserVote
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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

    def create(self, validated_data):
        voxpopuser = User(**validated_data)
        password = validated_data['password']
        voxpopuser.set_password(password)
        voxpopuser.save()
        token = Token.objects.create(user=voxpopuser)
        token.save()
        return voxpopuser


    def update(self, instance, validated_data):
        updatedUser = vars(instance)
        del(updatedUser['_state'])
        print('\n\n\n\n{}\n\n\n\n'.format(updatedUser))
        for field, value in validated_data.items():
            updatedUser[field] = value
        print('\n\n\n\n{}\n\n\n\n'.format(updatedUser))
        updated = User(**updatedUser)
        if 'password' in validated_data:
            updated.set_password(validated_data['password'])
        
        return updated
        # updated = User(**validated_data)
        # toptop = vars(updated)
        # print('\n\n\n\n{}\n\n\n\n'.format(toptop))
        # updated.id = instance.id
        # password = validated_data['password']
        # updated.set_password(password)
        # return instance


class ParliamentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Parliamentary
        fields = [
            'parliamentary_id',
            'name',
            'gender',
            'federal_unit',
            'photo'
        ]


class PropositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposition
        fields = [
            'id',
            'native_id',
            'proposition_type',
            'proposition_type_initials',
            'number',
            'year',
            'abstract',
            'processing',
            'situation',
            'url_full'
        ]


class UserVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVote
        fields = [
            'id',
            'user',
            'proposition',
            'option'
        ]
