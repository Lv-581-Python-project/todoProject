from django.db import models
from django.conf import settings
from todolist.models import ToDoList
from custom_user.models import CustomUser


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=256)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_id = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @classmethod
    def find_by_id(cls, task_id: int):
        try:
            task = Task.objects.get(pk=task_id)
            return task
        except Task.DoesNotExist:
            return None

    @classmethod
    def get_all(cls):
        try:
            task = Task.objects.all()
            return task
        except Task.DoesNotExist:
            return None

    @classmethod
    def find_all_for_list(cls, list_id):
        tasks = Task.objects.filter(list_id=list_id)
        return tasks

    @classmethod
    def create(cls, title: str, description: str, deadline, user_id, task_id):
        task = Task(title=title, description=description, deadline=deadline)
        user = CustomUser.find_by_id(user_id)
        task.user_id = user
        list = ToDoList.get_by_id(task_id)
        task.list_id = list
        task.save()
        return task

    @classmethod
    def update(cls, task_id: int, data: dict):
        task = cls.find_by_id(task_id)
        if task:
            for field, value in data.items():
                if hasattr(task, field):
                    setattr(task, field, value)
                else:
                    raise KeyError("Failed to update non existing attribute {}.{}".format(
                        task.__class__.__name__, field))
            task.save()
            return cls.find_by_id(task_id=task_id)
        return None

    @classmethod
    def remove(cls, task_id: int):
        task = cls.find_by_id(task_id=task_id)
        if task:
            task.delete()
        return not cls.find_by_id(task_id=task_id)

