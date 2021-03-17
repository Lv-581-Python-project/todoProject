import json

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from utils.validators import is_integer
from .models import CustomUser, ToDoList


class ToDoListView(APIView):

    def get(self, request, todo_list_pk=None):
        if todo_list_pk:
            if not is_integer(todo_list_pk):
                return HttpResponse(status=404)
            todo_list = ToDoList.get_by_id(todo_list_pk)
            if not todo_list:
                return HttpResponse(status=404)
            return JsonResponse(todo_list.to_dict(), status=200)

        todo_lists = ToDoList.get_all()
        todo_lists = json.dumps([todo_list.to_dict() for todo_list in todo_lists])
        return HttpResponse(todo_lists, status=200, content_type="application/json")

    def post(self, request):
        data = request.body

        data = {
            'name': data.get('name'),
            'description': data.get('description') if data.get('description') else '',
            'members': [CustomUser.get_by_id(pk=user_id) for user_id in data.get('members')]
            if data.get('members') else None
        }

        todo_list = ToDoList.create(**data)
        if todo_list:
            return JsonResponse(todo_list.to_dict(), status=201)
        return HttpResponse(status=400)

    def put(self, request, todo_list_pk=None):
        if todo_list_pk and not is_integer(todo_list_pk):
            return HttpResponse(status=404)
        todo_list = ToDoList.get_by_id(todo_list_pk)
        if not todo_list:
            return HttpResponse(status=404)
        data = request.body

        members_to_add = data.get('members_to_add')
        members_to_delete = data.get('members_to_delete')
        if members_to_add or members_to_delete:
            todo_list = todo_list.update_members(members_to_add, members_to_delete)
            if not todo_list:
                return HttpResponse(status=400)
        data = {'name': data.get('name') if data.get('name') else None,
                'description': data.get('description') if data.get('description') else None}

        todo_list = todo_list.update(**data)
        if not todo_list:
            return HttpResponse(status=400)
        return HttpResponse(status=200)

    def delete(self, request, todo_list_pk=None):
        if todo_list_pk and not is_integer(todo_list_pk):
            return HttpResponse(status=404)
        todo_list = ToDoList.get_by_id(todo_list_pk)
        if not todo_list:
            return HttpResponse(status=404)

        ToDoList.remove(pk=todo_list_pk)
        return HttpResponse(status=200)
