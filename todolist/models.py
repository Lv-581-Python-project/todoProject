from django.db import models

from custom_user.models import CustomUser


class ToDoList(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default='No description for now.')

    members = models.ManyToManyField(CustomUser, related_name='todo_lists')
