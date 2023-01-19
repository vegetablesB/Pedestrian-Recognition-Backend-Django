""" Urls mapping for recipe app """
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recognition import views

router = DefaultRouter()
router.register('recognition', views.RecognitionViewSet)

app_name = 'recognition'

urlpatterns = [
    path('', include(router.urls)),
]
