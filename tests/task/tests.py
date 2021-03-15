import json
from django.test import TestCase
from task.models import Task
from custom_user.models import CustomUser
from todolist.models import ToDoList

from datetime import date


class TaskModelsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(id=1,
                                              first_name='Test',
                                              last_name='User',
                                              email='testuser@gmail.com',
                                              password='test')
        self.todolist = ToDoList.create(name="list 1", description="list1 descr", member_pk=self.user.pk)
        self.todolist.id = 1
        self.todolist.save()
        self.task1 = Task.create(title="Task #1",
                                 description="Task #1 Description",
                                 deadline=date(2021, 1, 1),
                                 user_id=self.user.pk,
                                 list_id=self.todolist.pk)

    def test_str(self):
        test = self.task1.__str__()
        self.assertEqual(test, "Task #1")

    def test_create(self):
        task = Task.create(title="Task #2",
                           description="Task #2 Description",
                           deadline=date(2021, 2, 2),
                           user_id=self.user.pk,
                           list_id=self.todolist.pk)
        self.assertIsInstance(task, Task)

    def test_update_task(self):
        self.task = Task.create(title="Task #3",
                                description="Task #3 Description",
                                deadline=date(2021, 3, 3),
                                user_id=self.user.pk,
                                list_id=self.todolist.pk)
        result = self.task.update("New task", "new task description", False, date(2021, 3, 3),
                                  self.user.pk, self.todolist.pk)
        self.assertEqual(result.title, "New task")
        self.assertEqual(result.description, "new task description")
        self.assertEqual(result.is_completed, False)
        self.assertEqual(result.deadline, date(2021, 3, 3))
        print(result.list_id.pk)
        self.assertEqual(result.user_id.pk, 1)
        self.assertEqual(result.list_id.pk, 1)
        self.assertTrue(result)

    def test_find_by_id(self):
        self.task = Task.create(title="Task #4",
                                description="Task #4 Description",
                                deadline=date(2021, 5, 3),
                                user_id=self.user.pk,
                                list_id=self.todolist.pk)
        result = Task.find_by_id(self.task.pk)
        self.assertIsInstance(result, Task)

    def test_find_by_non_existent_id(self):
        task = Task.get_by_id(100)
        self.assertTrue(task is None)

    def test_remove_task(self):
        self.task = Task.create(title="Task #5",
                                description="Task #5 Description",
                                deadline=date(2021, 4, 4),
                                user_id=self.user.pk,
                                list_id=self.todolist.pk)
        result = Task.remove(self.task.pk)
        self.assertNotIn(result, Task.find_all_for_list(self.todolist.pk))

    def test_remove_non_existed_task(self):
        result = Task.remove(100)
        self.assertEqual(result, False)

    def test_find_all_for_list(self):
        self.task = Task.create(title="Task #6",
                                description="Task #6 Description",
                                deadline=date(2021, 6, 7),
                                user_id=self.user.pk,
                                list_id=self.todolist.pk)
        result = Task.find_all_for_list(self.todolist.pk)
        self.assertEqual(len(result), 2)


class DeleteTaskView(TestCase):
    """ Test view for deleting an existing task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(first_name="Test",
                                                   last_name="User",
                                                   email="mail@mail.com",
                                                   password="secret"
                                                   )
        self.list = ToDoList.create(name='List',
                                    description='About list',
                                    member_pk=self.user.id)
        self.task = Task.create(title='Task',
                                description='Task',
                                deadline='2020-01-01',
                                list_id=self.list.id,
                                user_id=self.user.id)

    def test_delete_task_existing(self):
        response = self.client.generic('DELETE', '/tasks/', json.dumps({'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_task_non_existing(self):
        response = self.client.generic('DELETE', '/tasks/', json.dumps({'task_id': 10}))
        self.assertEqual(response.status_code, 400)


class CreateTaskView(TestCase):
    """ Test view for creating new task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(first_name="Test",
                                                   last_name="User",
                                                   email="mail@mail.com",
                                                   password="secret")
        self.list = ToDoList.create(name='List',
                                    description='About list',
                                    member_pk=self.user.id)

    def test_create_task_data_valid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task",
            "description": "Task",
            "deadline": "2020-01-01",
            "user_id": self.user.id,
            "list_id": self.list.id
        }))
        self.assertEqual(response.status_code, 201)

    def test_create_task_data_invalid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task name that way beyond 30 symbol limit",
            "description": "Task",
            "deadline": "2020-01-01",
            "user_id": self.user.id,
            "list_id": self.list.id
        }))
        self.assertEqual(response.status_code, 400)

    def test_create_task_missing(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({"description": "Task"}))
        self.assertEqual(response.status_code, 400)


class UpdateTaskView(TestCase):
    """ Test view for updating existing task """

    def setUp(self):
        self.user = CustomUser.objects.create_user(first_name="Test",
                                                   last_name="User",
                                                   email="mail@mail.com",
                                                   password="secret")
        self.list = ToDoList.create(name='List',
                                    description='About list',
                                    member_pk=self.user.id)
        self.task = Task.create(title='Task',
                                description='Task',
                                deadline='2020-01-01',
                                list_id=self.list.id,
                                user_id=self.user.id)

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
