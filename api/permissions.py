from rest_framework import permissions
from .models import SocialInformation

class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        permission = False
        authorized_user = False

        if request.user.is_superuser:
            return True

        elif (request.user.is_anonymous and request.method == 'POST'):
            return True

        elif 'users' in request.path:
            url_id = request.path.split('/users/')[1][:-1]
            user_id = str(request.user.id)

            if(url_id == user_id):
                authorized_user = True

            if(request.method != 'DELETE' and request.method != 'POST' and
                    authorized_user):
                return True

        else:
            permission = True

        return permission



class SocialInformationPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        permission = False
        authorized_user = False

        if request.user.is_superuser:
            return True

        elif request.user.is_anonymous:
            return False

        elif (request.method == 'POST' and \
                SocialInformation.objects.filter(owner=request.user).count() \
                == 0):
            return True

        elif 'socialInformation' in request.path:

            social_information = \
                SocialInformation.objects.filter(owner=request.user)
            if(social_information):
                social_information = social_information.first().id
            url_id = request.path.split('/socialInformation/')[1][:-1]

            if(url_id == social_information):
                authorized_user = True

            if(request.method != 'DELETE' and authorized_user):
                return True

        else:
            permission = True

        return permission
