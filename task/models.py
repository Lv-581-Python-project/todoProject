from django.db import models
from todolist.models import ToDoList
from custom_user.models import CustomUser
from datetime import date
from django.http import HttpResponse



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
    def find_all_for_list(cls, list_id):
        tasks = Task.objects.filter(list_id=list_id)
        return tasks

    @classmethod
    def create(cls, title: str, description: str, deadline: date, user_id, list_id):
        task = Task(title=title, description=description, deadline=deadline)
        user = CustomUser.get_by_id(user_id)
        task.user_id = user
        list = ToDoList.get_by_id(list_id)
        task.list_id = list
        task.save()
        return task

    def update(self, title: str, description: str, is_completed: bool, deadline: date, user_id: int, list_id: int):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.is_completed = is_completed
        self.user_id = CustomUser.get_by_id(user_id)
        self.list_id = ToDoList.get_by_id(list_id)
        self.save()
        return self.find_by_id(self.pk)

    @classmethod
    def remove(cls, task_id):
        task = Task.find_by_id(task_id)
        if task:
            task.delete()
            return HttpResponse("Task was deleted.")
        else:
                return False
