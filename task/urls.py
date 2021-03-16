from django.urls import path

from .views import TaskAPIView

urlpatterns = [
    path('by_list/<int:list_id>/', TaskAPIView.as_view()),
    path('', TaskAPIView.as_view(), name='task_api_view'),
]