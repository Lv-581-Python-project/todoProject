from django.db import models
# from User.models import CustomUser

class List(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    # Change custom user on user table name
    # user_id = models.ForeignKey(CustomUser)
