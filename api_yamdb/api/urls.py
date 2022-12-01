from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]