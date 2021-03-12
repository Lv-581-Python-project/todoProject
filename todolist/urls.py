from django.urls import path

from . import views

urlpatterns = [
    path('', views.ToDoListView.as_view(), name='all-lists'),
    path('list/<int:todo_list_pk>/', views.ToDoListView.as_view(), name='one-list'),
    path('delete-list/<int:todo_list_pk>/', views.ToDoListView.as_view(), name='delete-list'),
    path('update-list/<int:todo_list_pk>/', views.ToDoListView.as_view(), name='update-list'),
    path('create-list/', views.ToDoListView.as_view(), name='create-list')
]
