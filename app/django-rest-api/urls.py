"""
URL configuration for django-rest-api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Miinventory API",
        default_version="v1",
        description="Miinventory API built in Django REST API",
    ),
    public=True,
)

urlpatterns = [
    # Admin - Optional
    path("admin/", admin.site.urls),
    # API
    path("api/", include("api.urls")),
    # Documentation
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
