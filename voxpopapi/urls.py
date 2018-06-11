from api.views import (
    CustomObtainToken, LoaderViewSet, ParliamentaryViewset, PropositionViewset,
    SocialInformationViewset, StatisticViewset, UserFollowingViewset,
    UserViewset, UserVoteViewset, ContactUsViewset
)

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='VoxPop API')

router = routers.DefaultRouter()
router.register(r'contact_us', ContactUsViewset)
router.register(r'users', UserViewset)
router.register(r'social_informations', SocialInformationViewset)
router.register(r'loader', LoaderViewSet, 'loader')
router.register(r'parliamentarians', ParliamentaryViewset, 'parliamentarians')
router.register(r'propositions', PropositionViewset, 'propositions')
router.register(r'user_votes', UserVoteViewset, 'user_votes')
router.register(r'user_following', UserFollowingViewset, 'user_following')
router.register(r'statistics', StatisticViewset, 'statistics')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token_auth/', CustomObtainToken.as_view()),
    url(r'^$', schema_view),
    url(r'^api/oauth/', include('rest_framework_social_oauth2.urls')),
]
