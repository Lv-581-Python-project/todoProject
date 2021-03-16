import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from rest_framework.views import APIView

from .models import CustomUser


class ProfileView(APIView):

    def get(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)
        if user:
            return JsonResponse(user.to_dict())
        return HttpResponse(status=400)

    def post(self, request):
        if not request.body:
            return HttpResponse("Empty data input", status=400)
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        data = {'first_name': body.get('first_name'), 'last_name': body.get('last_name'),
                'password': body.get('password'), 'email': body.get('email')}

        new_user = CustomUser.objects.create(**data)
        if new_user:
            return JsonResponse(new_user.to_dict(), status=200)
        return HttpResponse('Something went wrong', status=400)


    def put(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)

        if not user:
            return HttpResponse(status=404)

        if not request.body:
            return HttpResponse("Empty data input", status=400)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
        updated_user = CustomUser.update(user, **body)

        if updated_user:
            return JsonResponse( user.to_dict(), status=200)
        return HttpResponse(status=400)


    def delete(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)
        if user:
            CustomUser.remove(user_id)
            return HttpResponse('User removed.', status=200)
        return HttpResponse('User not found', status=400)
