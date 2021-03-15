from datetime import datetime

from django.db import models

from custom_user.models import CustomUser
from todolist.models import ToDoList


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
    def get_by_id(cls, task_id: int):
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
    def create(cls, title: str, description: str, deadline, user_id, list_id):
        task = Task(title=title, description=description, deadline=deadline)
        user = CustomUser.get_by_id(user_id)
        task.user_id = user
        todolist = ToDoList.get_by_id(list_id)
        task.list_id = todolist
        task.save()
        return task

    def update(self, title: str,
               description: str,
               is_completed: bool,
               deadline: datetime,
               user_id: int,
               list_id: int):
        if title:
            self.title = title
        if description:
            self.description = description
        if deadline:
            self.deadline = deadline
        if is_completed:
            self.is_completed = is_completed
        if user_id:
            self.user_id = CustomUser.get_by_id(user_id)
        if list_id:
            self.list_id = ToDoList.get_by_id(list_id)
        self.save()

    @classmethod
    def remove(cls, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
        except Task.DoesNotExist:
            return False
        return True
