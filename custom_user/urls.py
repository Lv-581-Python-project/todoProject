from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('create/', views.ProfileView.as_view(), name='create'),
]
