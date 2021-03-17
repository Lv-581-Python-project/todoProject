from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.utils import IntegrityError, DataError
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from task.models import Task
from todolist.models import ToDoList
from custom_user.models import CustomUser


class TaskAPIView(APIView):

    def get(self, request, list_id):
        todolist = ToDoList.get_by_id(list_id)
        task = Task.get_by_list_id(todolist)

        task_serialized_data = serialize('python', task)

        data = {
            'tasks': task_serialized_data,
        }
        return JsonResponse(data)

    def post(self, request):
        body = request.body

        list_id = body.get('todolist')
        user_id = body.get('user')

        todolist = ToDoList.get_by_id(list_id)
        user = CustomUser.get_by_id(user_id)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user': user,
            'todolist': todolist,
        }

        try:
            task = Task.create(**task_data)
            task.save()

            success_message = {
                'message': f'New task object has been created with ID {task.id}'
            }

            return JsonResponse(success_message, status=201)

        # Missing parameters
        except (IntegrityError, AttributeError):
            integrity_message = {
                'message': 'Cannot create task! One or more parameters are missing'
            }
            return JsonResponse(integrity_message, status=400)

        # Invalid input
        except (DataError, ValidationError, ValueError):
            invalid_data_message = {
                'message': 'Cannot create task! One or more parameters are invalid'
            }
            return JsonResponse(invalid_data_message, status=400)

    def put(self, request, task_id=None):
        body = request.body
        user = None
        todolist = None

        if body.get('todolist'):
            list_id = body.get('todolist')
            todolist = ToDoList.get_by_id(list_id)
        if body.get('user'):
            user_id = body.get('user')
            user = CustomUser.get_by_id(user_id)

        task_data = {
            'title': body.get('title'),
            'description': body.get('description'),
            'deadline': body.get('deadline'),
            'user': user,
            'todolist': todolist,
            'is_completed': body.get('list_id'),
        }

        # Missing ID
        if not task_id:
            missing_id_message = {
                'message': 'Cannot update task! Task ID is missing!'
            }
            return JsonResponse(missing_id_message, status=400)

        task = Task.get_by_id(pk=task_id)

        # ID of non-existing task
        if not task:
            not_exist_message = {
                'message': f'Cannot update task! Task with ID {task_id} does not exist'
            }
            return JsonResponse(not_exist_message, status=400)

        # Update
        try:
            task.update(**task_data)

            success_message = {
                'message': f'Task with ID {task_id} has been updated'
            }
            return JsonResponse(success_message, status=200)

        # Invalid input
        except (DataError, ValidationError, ValueError):
            invalid_data_message = {
                'message': 'Cannot update task! One or more parameters are invalid'
            }
            return JsonResponse(invalid_data_message, status=400)

    def delete(self, request, task_id=None):
        # Missing ID
        if not task_id:
            missing_id_message = {
                'message': 'Cannot delete task! Task ID is missing!'
            }
            return JsonResponse(missing_id_message, status=400)

        if Task.remove(pk=task_id):
            success = {
                'message': f'Task with ID {task_id} has been deleted'
            }
            return JsonResponse(success, status=200)
        else:
            failure = {
                'message': f'Task with ID {task_id} does not exist!'
            }
            return JsonResponse(failure, status=400)
