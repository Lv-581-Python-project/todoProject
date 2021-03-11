from django.http import JsonResponse
from django.views import View
from task.models import Task
from todolist.models import ToDoList
from django.core.serializers import serialize
import json
from custom_user.models import CustomUser


class TaskAPIView(View):

    def get(self, request, list_id):
        task = Task.objects.filter(list_id=list_id)

        task_serialized_data = serialize('python', task)

        data = {
            'tasks': task_serialized_data,
        }
        return JsonResponse(data)

    def post(self, request):
        post_body = json.loads(request.body)

        title = post_body.get('title')
        description = post_body.get('description')
        deadline = post_body.get('deadline')
        _user_id = post_body.get('user_id')
        _list_id = post_body.get('list_id')

        user_id = CustomUser.find_by_id(_user_id)
        list_id = ToDoList.objects.get(id=_list_id)


        task_data = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'user_id': user_id,
            'list_id': list_id,
        }

        task_obj = Task.objects.create(**task_data)
        task_obj.save()
        data = {
            'message': f'New task object has been created with id {task_obj.id}'
        }
        return JsonResponse(data, status=201)

    def put(self, request, task_id):
        task = Task.objects.get(id=task_id)

        put_body = json.loads(request.body)

        task.title = put_body.get('title')
        task.description = put_body.get('description')
        task.deadline = put_body.get('deadline')
        task.user_id = CustomUser.find_by_id(put_body.get('user_id'))
        task.list_id = ToDoList.objects.get(id=put_body.get('list_id'))
        task.is_completed = put_body.get('is_completed')
        task.save()

        data = {
            'message': f'Task {task_id} has been updated'
        }
        return JsonResponse(data)

    def delete(self, request, task_id):
        Task.objects.get(id=task_id).delete()

        data = {
            'message': f'Task with id {task_id} has been deleted'
        }
        return JsonResponse(data)