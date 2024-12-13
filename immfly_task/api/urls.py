from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ChannelViewSet, ContentViewSet, GroupViewSet

router = DefaultRouter()
router.register('channels', ChannelViewSet, basename='channel')
router.register('contents', ContentViewSet, basename='content')
router.register('groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]
