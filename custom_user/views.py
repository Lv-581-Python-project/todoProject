from django.views import View
from django.http import JsonResponse

from .models import CustomUser
from todolist.models import ToDoList


class ProfileView(View):

    def get(self, request, id=None):
        user = CustomUser.find_by_id(id)
        if user:
            return JsonResponse(user.to_dict())
        return JsonResponse(status=400)
