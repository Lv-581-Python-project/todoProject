"""project_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ToDoList API",
        default_version='v1',
        description="API for CRUD",
        terms_of_service="https://todolist/policies/terms/",
        contact=openapi.Contact(email="contact@todolist.remote"),
        license=openapi.License(name="ToDoList License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('custom-user/', include('custom_user.urls')),
    path('todolist/', include('todolist.urls')),
    path('tasks/', include('task.urls')),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger-redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
