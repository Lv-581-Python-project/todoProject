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
        body = json.loads(request.body)


        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
        }

        task = Task.create(**task_data)
        task.save()

        data = {
            'message': f'New task object has been created with id {task.id}'
        }
        return JsonResponse(data, status=201)

    def put(self, request):

        body = json.loads(request.body)

        task = Task.objects.get(id=body.get('task_id'))

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
            'is_completed': body.get('list_id'),
        }

        task.update(**task_data)

        data = {
            'message': f'Task {body.get("task_id")} has been updated'
        }
        return JsonResponse(data)

    def delete(self, request):

        body = json.loads(request.body)

        success = {
            'message': f'Task with id {body.get("task_id")} has been deleted'
        }

        failure = {
            'message': f'Task with id {body.get("task_id")} does not exist!'
        }

        if Task.remove(task_id=body.get('task_id')):
            return JsonResponse(success)
        else:
            return JsonResponse(failure)
