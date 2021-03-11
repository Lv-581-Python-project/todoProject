from django.urls import path

from . import views

urlpatterns = [
    path('', views.ToDoListView.as_view(), name='all-lists'),
    path('list/<int:todo_list_pk>/', views.ToDoListView.as_view(), name='one-list'),
    path('<int:todo_list_pk>/delete/', views.ToDoListView.as_view(), name='delete-list'),
    path('<int:todo_list_pk>/update/', views.ToDoListView.as_view(), name='update-list'),
    path('create/', views.ToDoListView.as_view(), name='create-list')
]
