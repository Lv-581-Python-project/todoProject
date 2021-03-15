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

    @staticmethod
    def put(request, user_id=None):
        user = CustomUser.get_by_id(user_id)

        if not user:
            return HttpResponse(status=404)

        if not request.body:
            return HttpResponse("Empty data input", status=400)

        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)

        data = {}

        if not body.get('first_name'):
            data['first_name'] = user.first_name
        else:
            data['first_name'] = body.get('first_name')
        if not body.get('last_name'):
            data['last_name'] = user.last_name
        else:
            data['last_name'] = body.get('last_name')
        if not body.get('email'):
            data['email'] = user.email
        else:
            data['email'] = body.get('email')

        updated_user = CustomUser.update(user,data)

        if updated_user:
            return JsonResponse( user.to_dict(), status=200)
        return HttpResponse(status= 400)

    @staticmethod
    def delete(request, user_id=None):
        user = CustomUser.get_by_id(user_id)
        if user:
            CustomUser.remove(user_id)
            return HttpResponse('User removed.', status=200)
        return HttpResponse('User not found', status=400)
