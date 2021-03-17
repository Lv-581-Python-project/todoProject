import json
from datetime import date

from django.test import TestCase
from task.models import Task
from custom_user.models import CustomUser
from todolist.models import ToDoList



class ByListTaskView(TestCase):
    """ Test view that returns all tasks for list """

    def setUp(self):
        self.user = CustomUser.objects.create(first_name="Test",
                                              last_name="User",
                                              email="mail@mail.com",
                                              password="secret"
                                              )
        self.list = ToDoList.create(name='List',
                                    description='About list')
        self.list.update_members(members_to_add=[self.user.id])
        self.task = Task.create(title='Task',
                                description='Task',
                                deadline=date(2020, 1, 1),
                                user=self.user,
                                todolist=self.list)

    def test_get_all_by_list_id(self):
        response = self.client.generic('GET', f'/tasks/by_list/{self.list.id}/')
        self.assertEqual(response.status_code, 200)


class DeleteTaskView(TestCase):
    """ Test view for deleting an existing task """

    def setUp(self):
        self.user = CustomUser.objects.create(first_name="Test",
                                              last_name="User",
                                              email="mail@mail.com",
                                              password="secret"
                                              )
        self.list = ToDoList.create(name='List',
                                    description='About list')
        self.list.update_members(members_to_add=[self.user.id])
        self.task = Task.create(title='Task',
                                description='Task',
                                deadline=date(2020, 1, 1),
                                user=self.user,
                                todolist=self.list)

    def test_delete_task_existing(self):
        response = self.client.generic('DELETE', f'/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_task_non_existing(self):
        response = self.client.generic('DELETE', '/tasks/100/')
        self.assertEqual(response.status_code, 400)

    def test_delete_task_no_id(self):
        response = self.client.generic('DELETE', '/tasks/')
        self.assertEqual(response.status_code, 400)


class CreateTaskView(TestCase):
    """ Test view for creating new task """

    def setUp(self):
        self.user = CustomUser.objects.create(first_name="Test",
                                              last_name="User",
                                              email="mail@mail.com",
                                              password="secret")
        self.list = ToDoList.create(name='List',
                                    description='About list')
        self.list.update_members(members_to_add=[self.user.id])

    def test_create_task_data_valid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task",
            "description": "Task",
            "deadline": "2020-01-01",
            "user": self.user.id,
            "todolist": self.list.id
        }))
        self.assertEqual(response.status_code, 201)

    def test_create_task_long_title(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task name that way beyond 30 symbol limit",
            "description": "Task",
            "deadline": "2020-01-01",
            "user": self.user.id,
            "todolist": self.list.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_create_task_data_invalid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task",
            "description": "Task",
            "deadline": "May 2020",
            "user": self.user.id,
            "todolist": self.list.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_create_task_missing(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({"description": "Task"}))
        self.assertEqual(response.status_code, 400)


class UpdateTaskView(TestCase):
    """ Test view for updating existing task """

    def setUp(self):
        self.user = CustomUser.objects.create(first_name="Test",
                                              last_name="User",
                                              email="mail@mail.com",
                                              password="secret")
        self.list = ToDoList.create(name='List',
                                    description='About list')
        self.list.update_members(members_to_add=[self.user.id])
        self.task = Task.create(title='Task',
                                description='Task',
                                deadline=date(2020, 1, 1),
                                todolist=self.list,
                                user=self.user)

    def test_update_task_existing(self):
        response = self.client.generic('PUT', f'/tasks/{self.task.id}/', json.dumps({
            "title": "UPDATE!"
        }))
        self.assertEqual(response.status_code, 200)

    def test_update_task_non_existing(self):
        response = self.client.generic('PUT', '/tasks/100/', json.dumps({
            "title": "UPDATE!"
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_data_valid(self):
        response = self.client.generic('PUT', f'/tasks/{self.task.id}/', json.dumps({
            "deadline": "May 2021",
            "user": self.user.id,
            "todolist": self.list.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_data_invalid(self):
        response = self.client.generic('PUT', f'/tasks/{self.task.id}/', json.dumps({
            "deadline": "May 2021"
        }))
        self.assertEqual(response.status_code, 400)

    def test_update_task_id_missing(self):
        response = self.client.generic('PUT', '/tasks/', json.dumps({
            "deadline": "2020-01-01"
        }))
        self.assertEqual(response.status_code, 400)

