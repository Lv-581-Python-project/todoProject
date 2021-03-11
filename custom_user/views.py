from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import CustomUser


class ProfileView(View):

    def get(self, request, user_id=None):
        user = CustomUser.find_by_id(user_id)
        if user:
            return JsonResponse(user.to_dict())
        return HttpResponse(status=400)
