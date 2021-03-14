from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from task.models import Task
from django.core.serializers import serialize
import json
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError


class TaskAPIView(APIView):

    def get(self, request, list_id):
        task = Task.objects.filter(list_id=list_id)

        task_serialized_data = serialize('python', task)

        data = {
            'tasks': task_serialized_data,
        }
        return JsonResponse(data)

    def post(self, request):
        # JSON validation
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            failure = {
                'message': f'Please provide valid json request!'
            }
            return JsonResponse(failure, status=400)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
        }

        try:
            task = Task.create(**task_data)
            task.save()

            success_message = {
                'message': f'New task object has been created with id {task.id}'
            }

            return JsonResponse(success_message, status=201)

        # Missing parameters
        except IntegrityError:
            integrity_message = {
                'message': f'Cannot create task! One or more parameters are missing'
            }
            return JsonResponse(integrity_message, status=400)

        # Invalid input
        except (DataError, ValidationError, ValueError):
            invalid_data_message = {
                'message': f'Cannot create task! One or more parameters are invalid'
            }
            return JsonResponse(invalid_data_message, status=400)

    def put(self, request):

        # JSON validation
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            failure = {
                'message': f'Please provide valid json request!'
            }
            return JsonResponse(failure, status=400)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user_id': body.get('user_id'),
            'list_id': body.get('list_id'),
            'is_completed': body.get('list_id'),
        }

        # Missing ID
        if not body.get("task_id"):
            missing_id_message = {
                'message': f'Cannot update task! Task id is missing!'
            }
            return JsonResponse(missing_id_message, status=400)

        # Invalid ID
        try:
            task = Task.get_by_id(task_id=body.get('task_id'))
        except ValueError:
            invalid_data_message = {
                'message': f'Please provide valid ID'
            }
            return JsonResponse(invalid_data_message, status=400)

        # ID of non-existing task
        if not task:
            not_exist_message = {
                'message': f'Cannot update task! Task with {body.get("task_id")} does not exist'
            }
            return JsonResponse(not_exist_message, status=400)

        try:
            task.update(**task_data)

            success_message = {
                'message': f'Task {body.get("task_id")} has been updated'
            }
            return JsonResponse(success_message, status=200)

        # Invalid input
        except (DataError, ValidationError, ValueError):
            invalid_data_message = {
                'message': f'Cannot update task! One or more parameters are invalid'
            }
            return JsonResponse(invalid_data_message, status=400)

    def delete(self, request):
        # JSON validation
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            failure = {
                'message': f'Please provide valid json request!'
            }
            return JsonResponse(failure, status=400)

        if Task.remove(task_id=body.get('task_id')):
            success = {
                'message': f'Task with id {body.get("task_id")} has been deleted'
            }
            return JsonResponse(success, status=200)
        else:
            failure = {
                'message': f'Task with id {body.get("task_id")} does not exist!'
            }
            return JsonResponse(failure, status=400)
