import json

from django.test import TestCase

from custom_user.models import CustomUser
from task.models import Task
from todolist.models import ToDoList


class DeleteTaskView(TestCase):
    """ Test view for deleting an existing task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            first_name="Test", last_name="User", email="mail@mail.com", password="secret")
        self.list = ToDoList.create(name='List', description='About list', member_pk=self.user.id)
        self.task = Task.create(
            title='Task', description='Task', deadline='2020-01-01', list_id=self.list.id, user_id=self.user.id)

    def test_delete_task_existing(self):
        response = self.client.generic('DELETE', '/tasks/', json.dumps({'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_non_existing(self):
        response = self.client.generic('DELETE', '/tasks/', json.dumps({'task_id': 10}))
        self.assertEqual(response.status_code, 400)


class CreateTaskView(TestCase):
    """ Test view for creating new task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            first_name="Test", last_name="User", email="mail@mail.com", password="secret")
        self.list = ToDoList.create(name='List', description='About list', member_pk=self.user.id)

    def test_create_task_data_valid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task", "description": "Task", "deadline": "2020-01-01", "user_id": self.user.id,
            "list_id": self.list.id
        }))
        self.assertEqual(response.status_code, 201)

    def test_create_task_data_invalid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task name that way beyond 30 symbol limit",
            "description": "Task", "deadline": "2020-01-01", "user_id": self.user.id, "list_id": self.list.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_create_task_missing(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({"description": "Task"}))
        self.assertEqual(response.status_code, 400)


class UpdateTaskView(TestCase):
    """ Test view for updating existing task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            first_name="Test", last_name="User", email="mail@mail.com", password="secret")
        self.list = ToDoList.create(name='List', description='About list', member_pk=self.user.id)
        self.task = Task.create(
            title='Task', description='Task', deadline='2020-01-01', list_id=self.list.id, user_id=self.user.id)

    def test_update_task_existing(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "title": "UPDATE!", "task_id": self.task.id
        }))
        self.assertEqual(response.status_code, 200)

    def test_update_task_non_existing(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "title": "UPDATE!", "task_id": 10
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_data_invalid(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "deadline": "May 2021", "task_id": self.task.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_id_invalid(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "deadline": "2020-01-01", "task_id": 'one'
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_id_missing(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "deadline": "2020-01-01"
        }))
        self.assertEqual(response.status_code, 400)
