from django.db import models
from django.conf import settings


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=30,
                             required=True)
    description = models.TextField(max_length=256)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField(required=True)

    def __str__(self):
        return self.title
