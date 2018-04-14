from rest_framework import permissions


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

            if(request.method != 'DELETE' and request.method != 'POST' and \
                    authorized_user):
                return True

        return permission
