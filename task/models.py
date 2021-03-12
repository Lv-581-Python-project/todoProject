from django.db import models
from django.conf import settings
from todolist.models import ToDoList
from custom_user.models import CustomUser
from datetime import datetime


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=256)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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

    def update(self, new_title: str, new_description: str, is_completed: bool, new_deadline: datetime, user_id: int, list_id: int):
        task = Task(new_title, new_description, new_deadline)
        task.title = new_title
        task.description = new_description
        task.deadline = new_deadline
        task.is_completed = is_completed
        task.user_id = CustomUser.find_by_id(user_id)
        task.list_id = ToDoList.get_by_id(list_id)
        task.save()
        return task

    @classmethod
    def remove(cls, user_id):
        try:
            task = Task.objects.get(user_id=user_id)
            task.delete()
        except Task.DoesNotExist:
            return False
        return True
