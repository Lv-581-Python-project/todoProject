from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views import View

from .models import CustomUser, ToDoList


class ToDoListView(View):

    def get(self, request, todo_list_pk=None):

        if todo_list_pk is None:
            todo_lists = ToDoList.get_all()
            todo_lists_dict={}
            for i,todo_list in enumerate(todo_lists):
                todo_lists_dict[i]=todo_list.to_dict()
            return JsonResponse(todo_lists_dict)
        todo_list = ToDoList.get_by_id(todo_list_pk=todo_list_pk)

        if todo_list:
            return JsonResponse(todo_list.to_dict())

        return HttpResponse(status=400)

    def post(self, request, member_pk, name, description=None):
        user = CustomUser.find_by_id(member_pk)
        if user:
            todo_list = ToDoList.create(name=name, description=description, member_pk=member_pk)
            return redirect('one-list',todo_list.to_dict())
        return HttpResponse(status=400)

    def delete(self, request, todo_list_pk=None):
        todo_list = ToDoList.get_by_id(todo_list_pk=todo_list_pk)
        if todo_list:
            todo_list.remove(todo_list_pk=todo_list_pk)
            return redirect('all-lists')
        return HttpResponse(status=400)

    def put(self, request, todo_list_pk, member_pk=None, name=None, description=None):
        todo_list = ToDoList.get_by_id(todo_list_pk=todo_list_pk)
        if todo_list:
            list_values = {'member': member_pk,
                           'name': name,
                           'description': description}
            for field, value in list_values.items():
                if value is None:
                    del list_values[field]
            todo_list.update(todo_list_pk=todo_list_pk, data=list_values)
            return JsonResponse(todo_list.to_dict())
        return HttpResponse(status=400)
