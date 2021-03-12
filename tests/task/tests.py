from django.test import TestCase
from task.models import Task

class TaskModelsTest(TestCase):
    def setUp(self):
        self.task1 = Task.objects.create(title="Task #1",
                            description="Task #1 Description",
                            deadline=2021-1-1,
                            user_id=1,
                            list_id=1)

    def test_str(self):
        test = self.task1.__str__()
        self.assertEqual(test, "Task #1")

    def test_create(self):
        task = Task.objects.create(title="Task #2",
                                         description="Task #1 Description",
                                         deadline=2021-2-2,
                                         user_id=2,
                                         list_id=2)
        self.assertIsInstance(task, Task)

    def test_update_task(self):
        task = self.task1.update("New task", "new task description", False, 2021-3-3, 3, 3)
        self.assertEqual(task.title, "New task")
        self.assertEqual(task.description, "new task description")
        self.assertEqual(task.is_completed, False)
        self.assertEqual(task.deadline, 2021-2-2)
        self.assertEqual(task.user_id, 2)
        self.assertEqual(task.list_id, 2)
        self.assertTrue(task)

    def test_find_by_id(self):
        task = Task.find_by_id(2)
        self.assertIsInstance(task, Task)

    def test_find_by_non_existent_id(self):
        task = Task.find_by_id(4)
        self.assertTrue(task is None)

    def test_remove_task(self):
        Task.objects.create(title="Task #3",
                            description="Task #3 Description",
                            deadline=2021 - 4 - 4,
                            user_id=3,
                            list_id=2)
        task = Task.remove(3)
        self.assertIn(b"Task was deleted.", task.content)

    def test_remove_non_existed_task(self):
        task = Task.remove(4)
        self.assertEqual(task, False)

    def test_remove_all_tasks(self):
        task = Task.remove_all()
        self.assertIn(b"All tasks deleted.", task.content)

    def test_get_all_does_not_exist(self):
        task = Task.get_all()
        self.assertTrue(task is None)

    def test_get_all(self):
        task = Task.get_all()
