from django.urls import include, path
from rest_framework import routers

from .views import (ReviewViewSet, UserViewSet, get_jwt_token,
                    send_confirmation_code)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email/', send_confirmation_code),
    path('v1/auth/token/', get_jwt_token)
]
