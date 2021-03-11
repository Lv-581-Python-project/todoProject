from django.urls import path

from .views import TaskAPIView

urlpatterns = [
    path('by_list/<int:list_id>', TaskAPIView.as_view()),
    path('<int:task_id>', TaskAPIView.as_view()),
    path('delete/<int:task_id>', TaskAPIView.as_view()),
]