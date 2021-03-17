from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from .models import CustomUser


class ProfileView(APIView):

    def get(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)
        if user:
            return JsonResponse(user.to_dict())
        return HttpResponsestatus=400)

    def post(self, request):
        if not request.body:
            return HttpResponse("Empty data input", status=400)

        body = request.body

        data = {'first_name': body.get('first_name'),
                'last_name': body.get('last_name'),
                'password': body.get('password'),
                'email': body.get('email')}

        new_user = CustomUser.create(**data)
        if new_user:
            return JsonResponse(new_user.to_dict(), status=200)
        return HttpResponse('Something went wrong', status=400)

    def put(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)

        if not user:
            return HttpResponse(status=404)

        if not request.body:
            return HttpResponse("Empty data input", status=400)

        body = request.body

        updated_user = CustomUser.update(user, **body)

        if updated_user:
            return JsonResponse(user.to_dict(), status=200)
        return HttpResponse(status=400)

    def delete(self, request, user_id=None):
        user = CustomUser.get_by_id(user_id)
        if user:
            CustomUser.remove(user_id)
            return HttpResponse('User removed.', status=200)
        return HttpResponse('User not found', status=400)
