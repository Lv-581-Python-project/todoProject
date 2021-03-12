from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import CustomUser


class ProfileView(View):

    def get(self, request, user_id=None):
        user = CustomUser.find_by_id(user_id)
        if user:
            return JsonResponse(user.to_dict())
        return HttpResponse(status=400)

    def put(self, request, user_id=None, first_name=None, last_name=None, email=None):
        user = CustomUser.find_by_id(user_id)
        if user:
            if first_name == None:
                first_name = user.first_name
            if last_name == None:
                last_name = user.last_name
            if email == None:
                email = user.email
            data = {'first_name' : first_name, 'last_name' : last_name, 'email' : email}
            CustomUser.update_user(user_id, data)
            return redirect('profile', user_id=user.id)
        return HttpResponse(status=400)

    def delete(self, request, user_id=None):
        user = CustomUser.find_by_id(user_id)
        if user:
            user = CustomUser.delete_user(user_id)
            return HttpResponse("User was deleted")
        return HttpResponse(status=400)

    def post(self, first_name=None, last_name=None, email=None):
        if first_name == None:
            return HttpResponse('Please, add first name')
        if last_name == None:
            return HttpResponse('Please add last name')
        user = CustomUser.objects.create_user(first_name, last_name, email)
        return redirect('profile', user_id=user.id)

