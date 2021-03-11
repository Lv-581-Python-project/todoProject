from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=256)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField()

    def __str__(self):
        return self.title
