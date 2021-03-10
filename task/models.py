from django.db import models
from django.conf import settings
from list.models import ToDoList

# Create your models here.
class Task(models.Model):
    title = models.CharField(
        max_length=30,
        required=True
    )
    description = models.TextField(
        max_length=256
    )
    is_completed = models.BooleanField(
        default=False
    )
    deadline = models.DateField(
        required=True
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    list_id = models.ForeignKey(
        ToDoList,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
