"""
URL configuration for jobpulse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from job.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views
from job.views import index

router = routers.SimpleRouter(trailing_slash=True)

# router.register("users", UserViewSet, basename="users")
router.register("jobs", JobViewSet, basename="jobs")
router.register("status", JobStatusUpdateViewSet, basename="status")
router.register("comments", JobCommentViewSet, basename="comments")
router.register("company", CompanyViewSet, basename="company")

schema_view = get_schema_view(
    openapi.Info(
        title="JobPulse",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    # path("current-user/", get_current_user),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/social/login/", include("job.urls")),
]

urlpatterns += router.urls
