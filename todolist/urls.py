from django.urls import path

from .views import ToDoListView

urlpatterns = [
    path('', ToDoListView.as_view()),
    path('<todo_list_pk>/', ToDoListView.as_view()),
]
