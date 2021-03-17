import json
from datetime import date

from django.test import TestCase

from custom_user.models import CustomUser
from task.models import Task
from todolist.models import ToDoList


class TaskModelsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(id=1,
                                              first_name='Test',
                                              last_name='User',
                                              email='testuser@gmail.com',
                                              password='test')
        self.todolist = ToDoList.create(name="list 1", description="list1 descr")
        self.todolist.update_members(members_to_add=[self.user.pk])
        self.todolist.id = 1
        self.todolist.save()
        self.task1 = Task.create(title="Task #1",
                                 description="Task #1 Description",
                                 deadline=date(2021, 1, 1),
                                 user=self.user,
                                 todolist=self.todolist)

    def test_str(self):
        test = self.task1.__str__()
        self.assertEqual(test, "Task #1")

    def test_create(self):
        task = Task.create(title="Task #2",
                           description="Task #2 Description",
                           deadline=date(2021, 2, 2),
                           user=self.user,
                           todolist=self.todolist)
        self.assertIsInstance(task, Task)

    def test_update_task(self):
        self.task = Task.create(title="Task #3",
                                description="Task #3 Description",
                                deadline=date(2021, 3, 3),
                                user=self.user.pk,
                                todolist=self.todolist.pk)
        self.task.update("New task",
                         "new task description",
                         False,
                         date(2021, 3, 3),
                         self.user,
                         self.todolist)
        self.assertEqual(self.task.title, "New task")
        self.assertEqual(self.task.description, "new task description")
        self.assertEqual(self.task.is_completed, False)
        self.assertEqual(self.task.deadline, date(2021, 3, 3))
        self.assertEqual(self.task.user.pk, 1)
        self.assertEqual(self.task.todolist.pk, 1)
        self.assertTrue(self.task)

    def test_find_by_id(self):
        self.task = Task.create(title="Task #4",
                                description="Task #4 Description",
                                deadline=date(2021, 5, 3),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.get_by_id(self.task.pk)
        self.assertIsInstance(result, Task)

    def test_find_by_non_existent_id(self):
        task = Task.get_by_id(100)
        self.assertTrue(task is None)

    def test_remove_task(self):
        self.task = Task.create(title="Task #5",
                                description="Task #5 Description",
                                deadline=date(2021, 4, 4),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.remove(self.task.pk)
        self.assertNotIn(result, Task.get_by_list_id(self.todolist.pk))

    def test_remove_non_existed_task(self):
        result = Task.remove(100)
        self.assertEqual(result, False)

    def test_find_all_for_list(self):
        self.task = Task.create(title="Task #6",
                                description="Task #6 Description",
                                deadline=date(2021, 6, 7),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.get_by_list_id(self.todolist.pk)
        self.assertEqual(len(result), 2)


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
            "user": self.user,
            "todolist": self.list
        }))
        self.assertEqual(response.status_code, 201)

    def test_create_task_data_invalid(self):
        response = self.client.generic('POST', '/tasks/', json.dumps({
            "title": "Task name that way beyond 30 symbol limit",
            "description": "Task",
            "deadline": "2020-01-01",
            "user": self.user,
            "todolist": self.list
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
