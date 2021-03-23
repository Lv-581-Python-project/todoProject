import json
from datetime import date

from django.test import TestCase
from task.models import Task
from custom_user.models import CustomUser
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

    def test_create_invalid(self):
        task = Task.create(title="gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg",
                           description="Task #2 Description",
                           deadline=date(2021, 2, 2),
                           user=self.user,
                           todolist=self.todolist)
        self.assertEqual(task, None)

    def test_update_task(self):
        self.task = Task.create(title="Task #3",
                                description="Task #3 Description",
                                deadline=date(2021, 3, 3),
                                user=self.user,
                                todolist=self.todolist)
        self.task.update("New task",
                               "new task description",
                               True,
                               date(2021, 3, 3),
                               self.user,
                               self.todolist)
        self.assertEqual(self.task.title, "New task")
        self.assertEqual(self.task.description, "new task description")
        self.assertEqual(self.task.is_completed, True)
        self.assertEqual(self.task.deadline, date(2021, 3, 3))
        self.assertEqual(self.task.user.pk, 1)
        self.assertEqual(self.task.todolist.pk, 1)
        self.assertTrue(self.task)

    def test_update_invalid(self):
        self.task = Task.create(title="Task #3",
                                description="Task #3 Description",
                                deadline=date(2021, 3, 3),
                                user=self.user,
                                todolist=self.todolist)
        res = self.task.update("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                               "new task description",
                               True,
                               date(2021, 3, 3),
                               self.user,
                               self.todolist)
        self.assertEqual(res, None)

    def test_get_by_id(self):
        self.task = Task.create(title="Task #4",
                                description="Task #4 Description",
                                deadline=date(2021, 5, 3),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.get_by_id(self.task.pk)
        self.assertIsInstance(result, Task)

    def test_get_by_non_existent_id(self):
        task = Task.get_by_id(100)
        self.assertTrue(task is None)

    def test_remove_task(self):
        self.task = Task.create(title="Task #5",
                                description="Task #5 Description",
                                deadline=date(2021, 4, 4),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.remove(self.task.pk)
        self.assertNotIn(result, Task.get_by_list_id(self.todolist))

    def test_remove_non_existed_task(self):
        result = Task.remove(100)
        self.assertEqual(result, False)

    def test_find_all_for_list(self):
        self.task = Task.create(title="Task #6",
                                description="Task #6 Description",
                                deadline=date(2021, 6, 7),
                                user=self.user,
                                todolist=self.todolist)
        result = Task.get_by_list_id(self.todolist)
        self.assertEqual(len(result), 2)
