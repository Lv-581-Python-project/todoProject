from django.db import models
# from user.models import User

class List(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    # user_id = models.ForeignKey(User)
