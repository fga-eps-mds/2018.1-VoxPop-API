from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view

from api.views import UserViewset, SocialInformationViewset
from rest_framework.authtoken import views

schema_view = get_swagger_view(title='VoxPop API')

router = routers.DefaultRouter()
router.register(r'users', UserViewset)
router.register(r'social_informations', SocialInformationViewset)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token_auth/', views.obtain_auth_token),
    url(r'^$', schema_view),
]
