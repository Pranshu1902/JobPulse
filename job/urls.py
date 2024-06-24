# from .views import *
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('user', UserViewSet, basename='user')
# router.register('job', JobViewSet, basename='job')
# urlpatterns = router.urls
from django.urls import path, include
from .views import GoogleLoginView

urlpatterns = [
    path("google/", GoogleLoginView.as_view(), name="Google"),
]
